# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from blog.models import Post


class PostModelTestCase(TestCase):

    def setUp(self):
        self.post_1 = Post.objects.create(title=u"Test post")
        self.post_2 = Post.objects.create(title=u"Test post")

    def tearDown(self):
        del(self.post_1)
        del(self.post_2)

    def test_post_autoslug(self):
        """Test the autoslug field has the right automatic value"""
        self.assertEqual(self.post_1.slug, "test-post")
        self.assertEqual(self.post_2.slug, "test-post-1")


class PostViewsTestCase(TestCase):

    def setUp(self):
        self.posts = []
        for count in range(6):
            self.posts.append(Post.objects.create(title=u"Test post %d" % count,
                                                  subtitle=u"sub %d" % count,))
        self.posts.reverse()
        self.hp_url = reverse('homepage')
        self.post_url = self.posts[0].get_absolute_url()
        self.posts_url = reverse('posts')
        self.search_url = reverse('posts-search')
        self.c = Client()

    def tearDown(self):
        for post in self.posts:
            del(post)

    def test_homepage(self):
        """ Test that the homepage returns 200 code using the right template
        """
        response = self.c.get(self.hp_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/homepage.html')

    def test_homepage_content(self):
        """ Check only last 5 posts in hp (others are in second page)
        """
        response = self.c.get(self.hp_url)
        self.assertEquals(list(response.context['posts']),
                          self.posts[:5])
        for c in range(5):
            self.assertIn(self.posts[c].title, response.content)
            self.assertIn(self.posts[c].get_absolute_url(), response.content)

        self.assertNotIn(self.posts[5].title, response.content)
        self.assertNotIn(self.posts[5].get_absolute_url(), response.content)

    def test_posts_page(self):
        """ Test that the post page returns 200 code using the same template
        """
        response = self.c.get(self.posts_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/posts.html')

    def test_posts_content(self):
        """ Check only last 5 posts in hp (others are in second page)
        """
        response = self.c.get(self.hp_url)
        self.assertEquals(list(response.context['posts']),
                          self.posts[:5])
        for c in range(5):
            self.assertIn(self.posts[c].title, response.content)
            self.assertIn(self.posts[c].get_absolute_url(), response.content)

        self.assertNotIn(self.posts[5].title, response.content)
        self.assertNotIn(self.posts[5].get_absolute_url(), response.content)

    def test_post_page(self):
        """ Test that the post page returns 200 code using the same template
        """
        response = self.c.get(self.post_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post.html')

    def test_post_content(self):
        """ Check some of the content and context of the post
        """
        response = self.c.get(self.post_url)
        self.assertEquals(response.context['post'], self.posts[0])
        self.assertIn(self.posts[0].title, response.content)
        self.assertIn(self.posts[0].subtitle, response.content)


class ImageValidatorTestCase(TestCase):

    def setUp(self):
        from .validators import ImageSize
        import Image
        size = (200,200)
        color = (255,0,0,0)
        img = Image.new("RGBA",size,color)
        validator = ImageSize()