from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

from blog.models import Post


class PostModelTestCase(TestCase):

    def setUp(self):
        self.post = Post.objects.create(title="Test post")

    def tearDown(self):
        del(self.post)

    def test_post_autoslug(self):
        """Test the autoslug field has the right automatic value"""
        self.assertEqual(self.post.slug, "test-post")


class postViewTestCase(TestCase):

    def setUp(self):
        self.posts = [Post.objects.create(title="Test post1", subtitle="one"),
                      Post.objects.create(title="Test post2", subtitle="two"),
                      Post.objects.create(title="Test post3", subtitle="thre"),
                      Post.objects.create(title="Test post4", subtitle="four"),
                      Post.objects.create(title="Test post5", subtitle="five"),
                      ]
        self.hp_url = reverse('homepage')
        self.post_url = self.posts[0].get_absolute_url()
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
        """ Check some of the content and context of the homepage
        """
        response = self.c.get(self.hp_url)
        self.assertEquals(list(response.context['posts']),
                          self.posts[::-1][:3])
        self.assertIn(self.posts[4].title, response.content)
        self.assertIn(self.posts[3].title, response.content)
        self.assertIn(self.posts[2].title, response.content)
        self.assertNotIn(self.posts[1].title, response.content)
        self.assertNotIn(self.posts[0].title, response.content)
        self.assertIn(self.posts[4].get_absolute_url(), response.content)
        self.assertIn(self.posts[3].get_absolute_url(), response.content)
        self.assertIn(self.posts[2].get_absolute_url(), response.content)
        self.assertNotIn(self.posts[1].get_absolute_url(), response.content)
        self.assertNotIn(self.posts[0].get_absolute_url(), response.content)

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
