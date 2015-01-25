# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile

import Image
import StringIO

from .models import Post
from .models import Tag
from .forms import CommentForm
from . import search


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
        # On edit dont change slug (and url)
        self.post_1.title = "Something different"
        self.post_1.save()
        self.assertEqual(self.post_1.slug, "test-post")


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
        self.assertEqual(response.status_code, 200)
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
        """ Check only last 5 posts in posts page (others are in second page)
        """
        response = self.c.get(self.posts_url)
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


class TagModelTestCase(TestCase):

    def setUp(self):
        self.tag_1 = Tag.objects.create(title=u"Test tag")
        self.tag_2 = Tag.objects.create(title=u"Test tag")

    def tearDown(self):
        del(self.tag_1)
        del(self.tag_2)

    def test_tag_autoslug(self):
        """Test the autoslug field has the right automatic value"""
        self.assertEqual(self.tag_1.slug, "test-tag")
        self.assertEqual(self.tag_2.slug, "test-tag-1")
        # On edit dont change slug (and url)
        self.tag_1.title = "Something different"
        self.tag_1.save()
        self.assertEqual(self.tag_1.slug, "test-tag")


class TagViewsTestCase(TestCase):

    def setUp(self):
        self.tags = []
        for count in range(6):
            self.tags.append(Tag.objects.create(title=u"Test tag %d" % count))
        self.tag_url = self.tags[0].get_absolute_url()
        self.tags_url = reverse('tags')
        self.c = Client()

    def tearDown(self):
        for tag in self.tags:
            del(tag)

    def test_tags_page(self):
        """ Test that the tags page returns 200 code using the same template
        """
        response = self.c.get(self.tags_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tags.html')

    def test_tags_content(self):
        """ Check only last 5 tags in tags page (others are in second page)
        """
        response = self.c.get(self.tags_url)
        self.assertEquals(list(response.context['tags']),
                          self.tags[:5])
        for c in range(5):
            self.assertIn(self.tags[c].title, response.content)
            self.assertIn(self.tags[c].get_absolute_url(), response.content)

        self.assertNotIn(self.tags[5].title, response.content)
        self.assertNotIn(self.tags[5].get_absolute_url(), response.content)

    def test_tag_page(self):
        """ Test that the tag page returns 200 code using the same template
        """
        response = self.c.get(self.tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/tag.html')

    def test_tag_content(self):
        """ Check some of the content and context of the tag
        """
        response = self.c.get(self.tag_url)
        self.assertEqual(response.status_code, 200)
        self.assertEquals(response.context['tag'], self.tags[0])
        self.assertIn(self.tags[0].title, response.content)


class SearchViewsTestCase(TestCase):
    def setUp(self):
        self.tags = []
        self.posts = []
        for count in range(6):
            self.tags.append(Tag.objects.create(title=u"Test tag %d" % count))
            post = Post.objects.create(title=u"Test post %d" % count,
                                       subtitle=u"sub %d" % count)
            for tag in self.tags:
                post.tags.add(tag)
            self.posts.append(post)
        self.tags.reverse()
        self.posts.reverse()
        self.posts[0].title = "Find me"
        self.posts[0].save()
        search.recreate_all()
        self.c = Client()
        self.search_url = reverse('posts-search')

    def tearDown(self):
        for tag in self.tags:
            del(tag)
        for post in self.posts:
            del(post)

    def test_search_results_for_query(self):
        response = self.c.get(self.search_url, {'q': 'find me'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.posts[0].title, response.content)
        self.assertIn(self.posts[0].get_absolute_url(), response.content)
        for p in self.posts[1:]:
            self.assertNotIn(p.title, response.content)
            self.assertNotIn(p.get_absolute_url(), response.content)

    def test_search_results_for_filter(self):
        response = self.c.get(self.search_url, {'f': 'test-tag-0'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.posts[0].title, response.content)
        self.assertIn(self.posts[0].get_absolute_url(), response.content)
        for p in self.posts[1:]:
            self.assertNotIn(p.title, response.content)
            self.assertNotIn(p.get_absolute_url(), response.content)


class CommentViewsTestCase(TestCase):
    def setUp(self):
        self.post = Post.objects.create(title=u"Test post")
        self.add_comment_url = reverse("add-comment")
        self.c = Client()
        self.post_url = self.post.get_absolute_url()
        self.comment_params = {'title': "How are you?",
                               'author': "John Doe",
                               'text': "Hi there",
                               'post': self.post.pk}

    def tearDown(self):
        del(self.post)

    def test_form_valid_data(self):
        form = CommentForm(self.comment_params)
        self.assertTrue(form.is_valid())

    def test_form_blank_data(self):
        form = CommentForm({})
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)
        self.assertIn("author", form.errors)
        self.assertIn("text", form.errors)

    def test_add_comment(self):
        response = self.c.post(self.add_comment_url, self.comment_params)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('"success": true' in response.content)
        del(self.comment_params["post"])
        for value in self.comment_params.values():
            self.assertIn(value, response.content)
        response = self.c.get(self.post_url)
        self.assertEqual(response.status_code, 200)
        for value in self.comment_params.values():
            self.assertIn(value, response.content)


class ImageValidatorTestCase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title=u"Test post", subtitle="aaa",
                                        text="text")
        self. color = (255, 0, 0, 0)
        self.sizes = [((200, 250), False),
                      ((2000, 250), False),
                      ((200, 90), False),
                      ((2000, 90), False),
                      ((200, 600), False),
                      ((2000, 600), False),
                      ((1900, 90), False),
                      ((1900, 600), False),
                      ((1900, 250), True)]

    def test_image_sizes(self):
        for size in self.sizes:
            img = Image.new("RGBA", size[0], self.color)
            img_io = StringIO.StringIO()
            img.save(img_io, format='JPEG')
            img_file = InMemoryUploadedFile(img_io, None, 'foo.jpg',
                                            'image/jpeg', img_io.len, None)
            self.post.image = img_file
            if not size[1]:
                with self.assertRaises(ValidationError):
                    self.post.full_clean()
                    self.post.save()
            else:
                self.post.full_clean()
                self.post.save()
