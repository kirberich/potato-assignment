# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
# from django.utils.translation import ugettext_lazy as _

from .views import HomepageView
from .views import PostsView
from .views import PostView
from .views import PostEdit
from .views import PostAdd
from .views import TagsView
from .views import TagView
from .views import JsonTagsView

urlpatterns = patterns(
    '',
    url(r'^$', HomepageView.as_view(), name="homepage"),
    url(r'^posts/$', PostsView.as_view(), name="posts"),
    url(r'^posts/add-new/$', PostAdd.as_view(), name="post-add"),
    url(r'^posts/(?P<slug>[-\w]+)/$', PostView.as_view(), name="post"),
    url(r'^posts/(?P<slug>[-\w]+)/edit/$',
        PostEdit.as_view(),
        name="post-edit"),
    url(r'^tags/$', TagsView.as_view(), name="tags"),
    url(r'^tags-json/$', JsonTagsView.as_view(), name="tags-json"),
    url(r'^tags/(?P<slug>[-\w]+)/$', TagView.as_view(), name="tag")
)
