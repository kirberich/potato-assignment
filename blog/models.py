from django.db import models
from django.utils.translation import ugettext_lazy as _

from autoslug.fields import AutoSlugField
from ckeditor.fields import RichTextField
from taggit_autosuggest.managers import TaggableManager


class Post(models.Model):
    title = models.CharField(verbose_name=_("Title"),
                             max_length=100,)
    slug = AutoSlugField(verbose_name=_("Slug"),
                         populate_from='title',
                         max_length=50,
                         unique=True,
                         editable=True,)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = TaggableManager()

    def __unicode__(self):
        return self.title
