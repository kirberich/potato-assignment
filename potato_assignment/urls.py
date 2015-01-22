from django.conf.urls import patterns, include, url
from django.contrib.sitemaps.views import sitemap

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

from blog.sitemap import BlogStaticViewsSitemap
from blog.sitemap import PostsSitemap
from blog.sitemap import TagsSitemap
from contacts.sitemap import ContactsStaticViewsSitemap

sitemaps = {"blog": BlogStaticViewsSitemap, "posts": PostsSitemap,
            "tags": TagsSitemap, "contacts": ContactsStaticViewsSitemap}

urlpatterns = patterns(
    '',
    url(r'^_ah/', include('djangae.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^contact-us/', include('contacts.urls')),
    url(r'^sitemap\.xml$', sitemap, {"sitemaps": sitemaps},
        name='django.contrib.sitemaps.views.sitemap'),
    url(r'^gauth/', include('djangae.contrib.gauth.urls')),
    url(r'^', include('blog.urls')),
)
