from django.test import TestCase
from blog.models import Post


class PostTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Test post",
                            text="<a href='http://www.google.com'>google</a>")

    def test_post_autoslug(self):
        """Test the autoslug field has the right automatic value"""
        test_post = Post.objects.get(title="Test post")
        self.assertEqual(test_post.slug, "test-post")
