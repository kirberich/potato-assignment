import json

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.list import BaseListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .models import Post
from .models import Tag
from .forms import PostForm

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


class PostEdit(UpdateView):
    """ Edit a single post
    """
    template_name = "blog/post_edit.html"
    form_class = PostForm
    model = Post

    @method_decorator(requires_csrf_token)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostEdit, self).dispatch(*args, **kwargs)


class PostAdd(CreateView):
    """ Add a single post
    """
    template_name = "blog/post_add.html"
    form_class = PostForm

    @method_decorator(requires_csrf_token)
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PostAdd, self).dispatch(*args, **kwargs)


class TagsView(ListView):
    """ View that shows all the tags
    """
    model = Tag
    context_object_name = "tags"
    template_name = "blog/tags.html"
    paginate_by = 2


class JSONResponseMixin(object):
    def render_to_response(self, context):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context))

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class JsonTagsView(JSONResponseMixin, BaseListView):

    model = Tag

    def get_context_data(self, **kwargs):
        import pdb; pdb.set_trace()
        queryset = kwargs.pop('object_list', self.object_list)
        return [(tag.pk, tag.title) for tag in queryset]


class TagView(DetailView):
    """ The detail view of a single tag
    """
    model = Tag
    context_object_name = "tag"
    template_name = "blog/tag.html"
