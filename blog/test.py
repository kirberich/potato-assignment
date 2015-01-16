from django.test import TestCase
from blog.models import Post


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Test post",
                            text="<a href='http://www.google.com'>google</a>",
                            tags="foo,bar")

    def test_post_autoslug(self):
        """Test the autoslug field has the right automatic value"""
        test_post = Post.objects.get(title="Test post")
        self.assertEqual(test_post.slug, "test-post")

    def test_tags(self):
        test_post = Post.objects.get(title="Test post")
        import ipdb; ipdb.set_trace()
        self.assertIn("foo", test_post.tags)
        self.assertIn("bar", test_post.tags)
        self.assertNotIn("baz", test_post.tags)
