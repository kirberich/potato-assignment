# -*- coding: utf-8 -*-
import operator

from django.db.models import signals

from whoosh import fields, qparser, sorting, query, formats
from whoosh.filedb.gae import DatastoreStorage
from whoosh.writing import AsyncWriter
from whoosh.analysis.tokenizers import Tokenizer
from whoosh.analysis.acore import Token
from whoosh.compat import text_type
from whoosh.analysis.filters import LowercaseFilter

from .models import Post
from .models import Tag


class SplitTokenizer(Tokenizer):
    """Yields the entire input string as a single token. For use in indexed but
    untokenized fields, such as a document's path.

    >>> idt = IDTokenizer()
    >>> [token.text for token in idt("/a/b 123 alpha")]
    ["/a/b 123 alpha"]
    """

    def __init__(self, separator=None, gaps=False):
        """
        :param expression: A regular expression object or string. Each match
            of the expression equals a token. Group 0 (the entire matched text)
            is used as the text of the token. If you require more complicated
            handling of the expression match, simply write your own tokenizer.
        :param gaps: If True, the tokenizer *splits* on the expression, rather
            than matching on the expression.
        """

        self.separator = separator
        self.gaps = gaps

    def __call__(self, value, positions=False, chars=False,
                 keeporiginal=False, removestops=True,
                 start_pos=0, start_char=0, mode='', **kwargs):
        assert isinstance(value, text_type), "%r is not unicode" % value
        t = Token(positions, chars, removestops=removestops, mode=mode,
                  **kwargs)
        for pos, match in enumerate(value.split(self.separator)):
            t.text = match
            t.boost = 1.0
            if keeporiginal:
                t.original = t.text
            t.stopped = False
            if positions:
                t.pos = start_pos + pos
            if chars:
                t.startchar = start_char + match.start()
                t.endchar = start_char + match.end()
            yield t


def SplitAnalyzer(separator=None):
    """Parses whitespace- or comma-separated tokens.

    >>> ana = KeywordAnalyzer()
    >>> [token.text for token in ana("Hello there, this is a TEST")]
    ["Hello", "there,", "this", "is", "a", "TEST"]

    :param lowercase: whether to lowercase the tokens.
    :param commas: if True, items are separated by commas rather than
        whitespace.
    """
    return SplitTokenizer(separator) | LowercaseFilter()


class SPLITTEDIDLIST(fields.IDLIST):
    """Configured field type for fields containing IDs separated by whitespace
    and/or punctuation (or anything else, using the expression param).
    """

    __inittypes__ = dict(stored=bool, unique=bool, separator=bool,
                         field_boost=float)

    def __init__(self, stored=False, unique=False, separator=None,
                 field_boost=1.0, spelling=False):
        """
        :param stored: Whether the value of this field is stored with the
            document.
        :param unique: Whether the value of this field is unique per-document.
        :param expression: The regular expression object to use to extract
            tokens. The default expression breaks tokens on CRs, LFs, tabs,
            spaces, commas, and semicolons.
        """
        super(SPLITTEDIDLIST, self).__init__(stored, unique, separator,
                                             field_boost, spelling)
        self.analyzer = SplitAnalyzer(separator="\t")
        self.format = formats.Existence(field_boost=field_boost)
        self.stored = stored
        self.unique = unique
        self.spelling = spelling

schema = {"pk": fields.ID(stored=True, unique=True),
          "text": fields.TEXT(analyzer=SplitAnalyzer()),
          "tags": SPLITTEDIDLIST(stored=True),
          }

WHOOSH_SCHEMA = fields.Schema(**schema)
storage = DatastoreStorage()


def get_or_create_index(sender=None, **kwargs):
    try:
        return storage.open_index(schema=WHOOSH_SCHEMA)
    except:
        return storage.create_index(WHOOSH_SCHEMA)


def create_index(sender=None, **kwargs):
    """ Creates the index schema (no data at this point)
    """
    get_or_create_index()


def delete_index(sender=None, **kwargs):
    """ Deletes the index schema and eventually the contained data
    """
    ix = get_or_create_index()
    ix.storage.destroy()


def recreate_index(sender=None, **kwargs):
    """ Deletes the index schema and eventually the contained data
        and rebuilds the index schema (no data at this point)
    """
    delete_index(sender=sender, **kwargs)
    create_index(sender=sender, **kwargs)


def update_index(sender, **kwargs):
    """ Adds/updates an entry in the index. It's connected with
        the post_save signal of the Object objects so will automatically
        index every new or modified Object
    """
    ix = get_or_create_index()
    writer = AsyncWriter(ix)
    obj = kwargs['instance']
    if "created" in kwargs and kwargs['created']:
        writer.add_document(**obj.index())
    else:
        writer.update_document(**obj.index())
    writer.commit()


def recreate_data(sender=None, **kwargs):
    """ Readds all the Object in the index. If they already exists
        will be duplicated
    """
    ix = get_or_create_index()
    writer = AsyncWriter(ix)
    for obj in Post.objects.all():
        writer.add_document(**obj.index())
    writer.commit()


def recreate_all(sender=None, **kwargs):
    """ Deletes the schema, creates it back and recreate all the data
        Good to create from scratch or for schema/data modification
    """
    recreate_index(sender=sender, **kwargs)
    recreate_data(sender=sender, **kwargs)

signals.post_syncdb.connect(recreate_all)
signals.post_save.connect(update_index, sender=Post)
signals.m2m_changed.connect(update_index, sender=Post.tags)


def search(q, filters, query_string, max_facets=5):
    """ Search for a query term and a set o filters
        Returns a list of hits and the representation of the facets
    """
    ix = get_or_create_index()
    hits = []
    facets = [sorting.FieldFacet("tags", allow_overlap=True,
                                 maptype=sorting.Count)]
    tags = Tag.objects.values('slug', 'title',)
    parser = qparser.QueryParser("text", schema=ix.schema)  # , group=og)
    try:
        q = parser.parse("*" + q + "*")
    except:
        q = None
    if q or filters:
        searcher = ix.searcher()
        for filter_value in filters:
            filter_name = "tags"
            q = q & query.Term(filter_name, filter_value)
        hits = searcher.search(q.normalize(), groupedby=facets)
        active_facets = []
        sorted_facets = sorted(hits.groups("tags").items(),
                               key=operator.itemgetter(1, 0),
                               reverse=True)
        facets = []
        for facet_slug, facet_value in sorted_facets:
            if not facet_slug:
                continue
            qs = query_string.copy()
            qs["page"] = "1"
            if facet_slug in filters:
                qs.setlist('f', [f for f in filters if f != facet_slug])
                state = "active"
            else:
                qs.appendlist('f', facet_slug)
                state = "available"
            obj = tags.get(slug=facet_slug)
            facet_dict = {'slug': facet_slug,
                          'title': obj.get("title", ""),
                          'count': facet_value,
                          'qs': qs.urlencode(),
                          }

            if state == 'active':
                active_facets.append(facet_dict)
            else:
                facets.append(facet_dict)
        return {"hits": hits, "facets": facets, "active_facets": active_facets}
