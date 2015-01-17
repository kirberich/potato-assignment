from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from .models import Post
from .models import Tag

import logging
logging.basicConfig()
logger = logging.getLogger("blog.console")


class HomepageView(ListView):
    """ Homepage view that get the 3 latest created posts
    """
    context_object_name = "posts"
    template_name = "blog/homepage.html"
    queryset = Post.objects.all()[:3]


class PostsView(ListView):
    """ View that shows all the posts sorted by creation and paginated
    """
    model = Post
    context_object_name = "posts"
    template_name = "blog/posts.html"
    paginate_by = 2


class PostView(DetailView):
    """ The detail view of a single post
    """
    context_object_name = "post"
    template_name = "blog/post.html"
    model = Post


class TagsView(ListView):
    """ View that shows all the tags
    """
    model = Tag
    context_object_name = "tags"
    template_name = "blog/tags.html"
    paginate_by = 2


class TagView(DetailView):
    """ The detail view of a single tag
    """
    model = Tag
    context_object_name = "tag"
    template_name = "blog/tag.html"
