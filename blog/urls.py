# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
#from django.utils.translation import ugettext_lazy as _

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.HomepageView.as_view(), name="homepage"),
    url(r'^(?P<slug>[-\w]+)$', views.PostView.as_view(), name="post"),
)
