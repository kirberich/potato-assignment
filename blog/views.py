from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Post

import logging
logging.basicConfig()
logger = logging.getLogger("blog.console")


class HomepageView(ListView):
    """ Homepage view that get the 3 latest creat posts
    """
    context_object_name = "posts"
    template_name = "blog/homepage.html"
    queryset = Post.objects.order_by('created')[:3]


class PostView(DetailView):
    """ The detail view of a single post
    """
    context_object_name = "post"
    template_name = "blog/post.html"
    model = Post
