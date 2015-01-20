# -*- coding: utf-8 -*-
import itertools

from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator

from djangae.fields import RelatedSetField

from ckeditor.fields import RichTextField


class BaseModel(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(verbose_name="Title",
                             max_length=50,)
    slug = models.SlugField(verbose_name="Slug",
                            max_length=50,
                            editable=True,
                            blank=True)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """ This ensure uniqueness. Have to do here cause
            this method was never called if unique=True is set
        """
        max_length = self._meta.get_field("slug").max_length

        new = orig = slugify(self.title)[:max_length]
        for x in itertools.count(1):
            if not self.__class__.objects.filter(slug=new).exists():
                break

            new = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
        self.slug = new
        super(BaseModel, self).save(*args, **kwargs)
        # Dirty hack to redirect only if the content has really been created
        # in the datastore and not only queued
        while not self.__class__.objects.filter(slug=new).exists():
            pass


class Tag(BaseModel):

    class Meta:
        ordering = ("title", )

    @models.permalink
    def get_absolute_url(self):
        return ("tag", [self.slug, ])


class Comment(BaseModel):

    class Meta:
        ordering = ("-created", )

    author = models.CharField(max_length=50)
    text = models.TextField(max_length=500,
                            validators=[MaxLengthValidator(500)])
    created = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey("Post", related_name="comments", null=True)


class Post(BaseModel):

    class Meta:
        ordering = ("-created", )

    subtitle = models.CharField(verbose_name="Subtitle",
                                max_length=100,)
    text = RichTextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    tags = RelatedSetField(Tag, related_name="posts", blank=True)

    @models.permalink
    def get_absolute_url(self):
        return ("post", [self.slug, ])

    @models.permalink
    def get_edit_url(self):
        return ("post-edit", [self.slug, ])

    @models.permalink
    def get_delete_url(self):
        return ("post-delete", [self.slug, ])
