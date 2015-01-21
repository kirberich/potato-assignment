from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse

from .models import Post
from .models import Tag


class PostsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Post.objects.filter()

    def lastmod(self, obj):
        return obj.modified


class TagsSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return Tag.objects.filter()

    def lastmod(self, obj):
        return obj.created


class BlogStaticViewsSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['posts', 'tags', 'homepage']

    def location(self, item):
        return reverse(item)
