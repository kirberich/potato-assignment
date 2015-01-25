# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from blog.models import Post
from blog.models import Tag


class SitemapViewsTestCase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title=u"Test post")
        self.tag = Tag.objects.create(title=u"Test tag")
        self.sitemap_url = reverse('sitemap')
        self.urls = [
            reverse('homepage'),
            reverse('posts'),
            reverse('tags'),
            self.post.get_absolute_url(),
            self.tag.get_absolute_url(),
            reverse('contact-form'),
        ]
        self.c = Client()

    def tearDown(self):
        del(self.post)

    def test_sitemap_page(self):
        """ Test that the post page returns 200 code using the same template
        """
        response = self.c.get(self.sitemap_url)
        self.assertEqual(response.status_code, 200)
        for url in self.urls:
            self. assertIn("http://testserver" + url, response.content)
