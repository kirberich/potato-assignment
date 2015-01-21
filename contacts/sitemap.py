from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


class ContactsStaticViewsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['contact-form']

    def location(self, item):
        return reverse(item)
