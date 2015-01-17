# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
# from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomepageView.as_view(), name="homepage"),
    url(r'^posts$', views.PostsView.as_view(), name="posts"),
    url(r'^posts/(?P<slug>[-\w]+)$', views.PostView.as_view(), name="post"),
    url(r'^tags$', views.TagsView.as_view(), name="tags"),
    url(r'^tags/(?P<slug>[-\w]+)$', views.TagView.as_view(), name="tag")
)
