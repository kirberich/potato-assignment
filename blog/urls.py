# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url

from .views import HomepageView
from .views import PostsView
from .views import PostView
from .views import PostEdit
from .views import PostDelete
from .views import PostAdd
from .views import TagsView
from .views import TagView
from .views import JSONCommentAdd
from .views import JSONTagsView
from .views import JSONSearchView

urlpatterns = patterns(
    '',
    url(r'^$', HomepageView.as_view(), name="homepage"),
    url(r'^posts/$', PostsView.as_view(), name="posts"),
    url(r'^posts/search/$', JSONSearchView.as_view(), name="posts-search"),
    url(r'^posts/add-new/$', PostAdd.as_view(), name="add-post"),
    url(r'^posts/(?P<slug>[-\w]+)/$', PostView.as_view(), name="post"),
    url(r'^posts/(?P<slug>[-\w]+)/edit/$',
        PostEdit.as_view(),
        name="post-edit"),
    url(r'^posts/(?P<slug>[-\w]+)/delete/$',
        PostDelete.as_view(),
        name="post-delete"),
    url(r'^tags/$', TagsView.as_view(), name="tags"),
    url(r'^tags/(?P<slug>[-\w]+)/$', TagView.as_view(), name="tag"),
    url(r'^tags-json/$', JSONTagsView.as_view(), name="tags-json"),
    #url(r'^posts-json/$', JSONPostsView.as_view(), name="posts-json"),
    url(r'^comments/add-new/$', JSONCommentAdd.as_view(), name="add-comment"),
)
