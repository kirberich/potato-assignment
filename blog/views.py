from django.views.generic import TemplateView

from .models import Post

import logging
logging.basicConfig()
logger = logging.getLogger("blog.console")


class HomepageView(TemplateView):
    """ Homepage view ...
    """

    template_name = "blog/homepage.html"
    queryset = Post.objects.prefetch_related("services")[:3]

#    def get_context_data(self, **kwargs):
#        context = super(HomepageView, self).get_context_data(**kwargs)
#        context.update({'facility_categories': self.queryset.filter(order__lt=10).order_by('order')})
#        return context
