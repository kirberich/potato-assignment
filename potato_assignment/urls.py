from django.conf.urls import patterns, include, url

import session_csrf
session_csrf.monkeypatch()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'potato_assignment .views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^_ah/', include('djangae.urls')),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^contact-us/', include('contacts.urls')),
    url(r'^gauth/', include('djangae.contrib.gauth.urls')),
    url(r'^', include('blog.urls')),
)
