from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from taggit_autosuggest.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=50,)
    slug = AutoSlugField(verbose_name=_("Slug"),
                         populate_from='title',
                         max_length=50,
                         unique=True,
                         editable=True,)
    subtitle = models.CharField(verbose_name=_("Subtitle"),
                                max_length=100,)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ("post", [self.slug, ])
