# -*- coding: utf-8 -*-
import json

from django.core.urlresolvers import reverse
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.list import BaseListView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import CreateView
from django.views.generic.edit import BaseCreateView
from django.views.generic.edit import DeleteView
from django.views.generic.base import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import requires_csrf_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponse

from .models import Post
from .models import Tag
from .models import Comment
from .forms import PostForm
from .forms import CommentForm
from .search import search

import logging
logging.basicConfig()
logger = logging.getLogger("blog.console")


class HomepageView(ListView):
    """ Homepage view
    """
    context_object_name = "posts"
    template_name = "blog/homepage.html"
    model = Post
    paginate_by = 5


class PostsView(ListView):
    """ Search view, which accepts search queries via url, like google.
    accepts 2 params:
    * q is the full text query
    * f is the list of active filters narrowing the search
    """
    context_object_name = "posts"
    template_name = "blog/posts.html"
    paginate_by = 5
    search_results = {}

    def get_queryset(self):
        query = self.request.GET.get('q', "").strip()
        filters = self.request.GET.getlist('f', [])
        self.search_results["q"] = query
        self.search_results["f"] = filters
        self.search_results.update(search(q=query, filters=filters,
                                   query_string=self.request.GET,))
        hits = self.search_results.pop("hits")
        return Post.objects.filter(pk__in=[h['pk'] for h in hits])

    def get_context_data(self, **kwargs):
        context = super(PostsView, self).get_context_data(**kwargs)
        context.update(self.search_results)
        return context

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(PostsView, self).dispatch(*args, **kwargs)


class PostView(DetailView):
    """ The detail view of a single post
    """
    context_object_name = "post"
    template_name = "blog/post.html"
    model = Post

    def get_context_data(self, **kwargs):
        queryset = super(PostView, self).get_context_data(**kwargs)
        comments = Comment.objects.filter(post=queryset['post'])
        queryset.update({"comments": comments,
                         "form": CommentForm()})
        return queryset


class PostEdit(UpdateView):
    """ Edit a single post
    """
    template_name = "blog/post_edit.html"
    model = Post
    form_class = PostForm

    @method_decorator(requires_csrf_token)
    @method_decorator(login_required)
    @method_decorator(permission_required("blog.post_edit"))
    def dispatch(self, *args, **kwargs):
        return super(PostEdit, self).dispatch(*args, **kwargs)


class PostAdd(CreateView):
    """ Add a single post
    """
    template_name = "blog/post_add.html"
    form_class = PostForm

    @method_decorator(requires_csrf_token)
    @method_decorator(login_required)
    @method_decorator(permission_required('blog.post_add'))
    def dispatch(self, *args, **kwargs):
        return super(PostAdd, self).dispatch(*args, **kwargs)


class TagsView(ListView):
    """ View that shows all the tags
    """
    model = Tag
    context_object_name = "tags"
    template_name = "blog/tags.html"
    paginate_by = 5


class TagView(DetailView):
    """ The detail view of a single tag
    """
    model = Tag
    context_object_name = "tag"
    template_name = "blog/tag.html"


class PostDelete(DeleteView):
    """ Remove a single post
    """

    model = Post

    def get_success_url(self):
        return reverse("posts")

    @method_decorator(requires_csrf_token)
    @method_decorator(login_required)
    @method_decorator(permission_required('blog.post_delete'))
    def dispatch(self, request, *args, **kwargs):
        response = super(PostDelete, self).dispatch(request, *args, **kwargs)
        pk = request.POST.get("post")
        # If not pk I'm in the confirmation view
        if pk:
            # Dirty hack to wait to return until GAE really removed my object
            while Post.objects.filter(pk=pk).exists():
                pass
        return response


class JSONView(View):
    def render_to_response(self, context, **httpresponse_kwargs):
        "Returns a JSON response containing 'context' as payload"
        return self.get_json_response(self.convert_context_to_json(context),
                                      **httpresponse_kwargs)

    def get_json_response(self, content, **httpresponse_kwargs):
        "Construct an `HttpResponse` object."
        return HttpResponse(content,
                            content_type='application/json',
                            **httpresponse_kwargs)

    def convert_context_to_json(self, context):
        "Convert the context dictionary into a JSON object"
        return json.dumps(context)


class JSONCommentAdd(JSONView, BaseCreateView):
    """ View to add comment. Posting to this from post.html
    """
    model = Comment

    def form_invalid(self, form):
        context = self.get_context_data(form=form,
                                        success=False)
        return self.render_to_response(context)

    def form_valid(self, form):
        self.object = form.save()
        context = self.get_context_data(form=form,
                                        obj=self.object,
                                        success=True)
        return self.render_to_response(context)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(JSONCommentAdd, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        success = kwargs.get('success', False)
        options = kwargs.get('options', {})
        result = {}
        fields = {}
        result.update(options=options)
        result.update(success=success)

        if not success:
            errors = {}
            form = kwargs.get('form')
            for field_name, field in form.fields.items():
                fields[field_name] = unicode(form[field_name].value())
            result.update(fields=fields)
            if form.errors:
                errors.update({'non_field_errors': form.non_field_errors()})
            fields = {}
            for field_name, text in form.errors.items():
                fields[field_name] = text
            errors.update(fields=fields)
            result.update(errors=errors)
        else:
            obj = kwargs.get('obj')
            result.update({"title": obj.title,
                           "text": obj.text,
                           "author": obj.author,
                           "created": obj.created.strftime("%Y-%m-%d~%H:%M")})
        return result


class JSONTagsView(JSONView, BaseListView):
    """ Json view to get all tags for autocmpletion purpose
    """
    model = Tag

    def get_context_data(self, **kwargs):
        queryset = kwargs.pop('object_list', self.object_list)
        return [(tag.pk, tag.title) for tag in queryset]
