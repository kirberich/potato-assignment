import itertools

from django import forms
from django.utils.text import slugify

from .models import Post


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['slug', ]


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['slug', ]

    def save(self):
        instance = super(PostAddForm, self).save(commit=False)

        max_length = Post._meta.get_field('slug').max_length
        instance.slug = orig = slugify(instance.title)[:max_length]

        for x in itertools.count(1):
            if not Post.objects.filter(slug=instance.slug).exists():
                break

            # Truncate the original slug dynamically. Minus 1 for the hyphen.
            instance.slug = "%s-%d" % (orig[:max_length - len(str(x)) - 1], x)

        instance.save()

        return instance
