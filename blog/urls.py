# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HomepageView
from .views import PostsView
from .views import PostView
from .views import PostEdit
from .views import JSONPostDelete
from .views import PostAdd
from .views import TagsView
from .views import TagView
from .views import JSONCommentAdd
from .views import JSONTagsView

urlpatterns = patterns(
    '',
    url(r'^$', HomepageView.as_view(), name="homepage"),
    url(r'^posts/$', PostsView.as_view(), name="posts"),
    url(r'^posts/add-post/$', PostAdd.as_view(), name="add-post"),
    url(r'^posts/(?P<slug>[-\w]+)/$', PostView.as_view(), name="post"),
    url(r'^posts/(?P<slug>[-\w]+)/edit/$',
        PostEdit.as_view(),
        name="post-edit"),
    url(r'^posts/(?P<slug>[-\w]+)/edit/$',
        JSONPostDelete.as_view(),
        name="post-delete"),
    url(r'^tags/$', TagsView.as_view(), name="tags"),
    url(r'^tags/(?P<slug>[-\w]+)/$', TagView.as_view(), name="tag"),
    url(r'^tags-json/$', JSONTagsView.as_view(), name="tags-json"),
    url(r'^add-comment/$', JSONCommentAdd.as_view(), name="add-comment"),
)
