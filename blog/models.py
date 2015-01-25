# -*- coding: utf-8 -*-
import itertools

from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxLengthValidator
from django.core.validators import RegexValidator

from djangae.fields import RelatedSetField

from ckeditor.fields import RichTextField

from .validators import ImageSize


class BaseModel(models.Model):

    class Meta:
        abstract = True

    title = models.CharField(verbose_name="Title",
                             max_length=50,
                             validators=[
                                 RegexValidator(
                                     r'^[^\t]*$',
                                     "tab are disallowed in the title.'"
                                 )])
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
        if not self.id:
            max_length = self._meta.get_field("slug").max_length
            new = orig = slugify(self.title)[:max_length]
            for x in itertools.count(1):
                if not self.__class__.objects.filter(slug=new).exists():
                    break

                new = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)
            self.slug = new
        super(BaseModel, self).save(*args, **kwargs)
        # Dirty hack to redirect only if the content has really been created
        # in the datastore and not only queued)
        while not self.__class__.objects.filter(slug=self.slug).exists():
            pass


class Tag(BaseModel):

    created = models.DateTimeField(auto_now_add=True)

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
    image = models.ImageField(upload_to="post_images",
                              validators=[ImageSize(min_w=1900,
                                                    max_w=1900,
                                                    min_h=100,
                                                    max_h=500)],
                              help_text="Must be 1900px X 100-500px",
                              blank=True)
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

    def index_text(self):
        """ Text indexed for fulltext search
        """
        elems = [self.title, self.subtitle, self.text, ]
        tags = [unicode(t.title) for t in self.tags.all()]
        elems.extend(tags)
        return unicode(" ".join(elems))

    def index_tags(self, sep="\t"):
        """ Returns a string representing all the post tsgs separated by
            the sep val.
            Needed to index the tags as listid in whoosh and have facets
        """
        return unicode(sep.join([t.slug for t in self.tags.all()]))

    def index(self):
        """ Returns a dictionary representing the whoosh entry for
            the current object in the index
        """
        return dict(pk=unicode(self.pk),
                    text=self.index_text(),
                    tags=self.index_tags(),
                    )
