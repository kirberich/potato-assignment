# -*- coding: utf-8 -*-
import re
import operator

from django.db.models import signals

from whoosh import fields, qparser, sorting, query
from whoosh.filedb.gae import DatastoreStorage
from whoosh.writing import AsyncWriter

from .models import Post
from .models import Tag

schema = {"pk": fields.ID(stored=True, unique=True),
          "text": fields.TEXT(),
          "tags": fields.IDLIST(stored=True, expression=re.compile(r"[^\t]+")),
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

# signals.post_save.connect(update_index, sender=Post)
# signals.m2m_changed.connect(update_index, sender=Post.tags)


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
