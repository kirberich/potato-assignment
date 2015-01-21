# -*- coding: utf-8 -*-
from django.db.models import signals

from whoosh import fields, qparser, sorting, query
from whoosh.filedb.gae import DatastoreStorage

from .models import Post

schema = {"pk": fields.ID(stored=True, unique=True),
          "text": fields.TEXT(),
          "tags": fields.IDLIST(stored=True),
          }

WHOOSH_SCHEMA = fields.Schema(**schema)
storage = DatastoreStorage()


def get_or_create_index(sender=None, **kwargs):
    try:
        return storage.open_index()
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
    ix.delete()


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
    writer = ix.writer()
    obj = kwargs['instance']
    if "created" in kwargs and kwargs['created']:
            writer.add_document(**obj.index())
    else:
        writer.update_document(**obj.index())
    writer.commit()

signals.post_save.connect(update_index, sender=Post)
signals.m2m_changed.connect(update_index, sender=Post.tags)


def recreate_data(sender=None, **kwargs):
    """ Readds all the Object in the index. If they already exists
        will be duplicated
    """
    ix = get_or_create_index()
    writer = ix.writer()
    for obj in Post.objects.all():
        writer.add_document(**obj.index_features())
        writer.commit()


def recreate_all(sender=None, **kwargs):
    """ Deletes the schema, creates it back and recreate all the data
        Good to create from scratch or for schema/data modification
    """
    recreate_index(sender=sender, **kwargs)
    recreate_data(sender=sender, **kwargs)

signals.post_syncdb.connect(recreate_all)


def search(q, filters, query_string, max_facets=5):
    """ Search for a query term and a set o filters
        Returns a list of hits and the representation of the facets
    """
    ix = get_or_create_index()
    hits = []

    facets = [sorting.FieldFacet("tag", allow_overlap=True,
                                 maptype=sorting.Count)]
    parser = qparser.QueryParser("text", schema=ix.schema)  # , group=og)
    parser.add_plugin(qparser.FuzzyTermPlugin())
    # Adds fuzzy search of distance 1 and prefix 0 to all search terms
    if q not in ("", "*"):
        q = "".join([item + "~" for item in q.split()])
    try:
        q = parser.parse(q)
    except:
        q = None
    if q or filters:
        searcher = ix.searcher()
        for filter in filters:
            filter_name, filter_value = filter.split(":", 1)
            q = q & query.Term(filter_name, filter_value)
        hits = searcher.search(q.normalize(), groupedby=facets)
        import pdb; pdb.set_trace()
        active_facets = []
        return hits, facets, active_facets
