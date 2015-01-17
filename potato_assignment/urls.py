from django.conf.urls import patterns, include, url

import session_csrf
session_csrf.monkeypatch()

import autocomplete_light
autocomplete_light.autodiscover()

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    # Examples:
    # url(r'^$', 'potato_assignment .views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    # url(r'^_ah/', include('djangae.urls')),

    # Note that by default this is also locked down with login:admin in app.yaml
    url(r'^admin/', include(admin.site.urls)),
    url(r'^ckeditor/', include('ckeditor.urls')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^contact-us/', include('contacts.urls')),
    url(r'^', include('blog.urls')),
)
