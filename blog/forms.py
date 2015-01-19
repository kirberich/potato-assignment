import itertools

from django import forms
from django.forms.util import flatatt
from django.utils.text import slugify
from django.utils.html import format_html
from django.utils.html import mark_safe

from .models import Post
from .models import Tag


class HiddenMultiple(forms.SelectMultiple):

#    def value_from_datadict(self, data, files, name):
#        import pdb; pdb.set_trace()
#        if isinstance(data, (MultiValueDict, MergeDict)):
#            return data.getlist(name)
#        return data.get(name, None)

    def render_options(self, choices, value):
        if not choices:
            return ""
        return "value=%s" % ",".join(choices)

    def render(self, name, value, attrs=None, choices=()):
        if not choices:
            choices = list(self.choices)

        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<input type="hidden" {0}',
                  flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('/>')
        return mark_safe(' '.join(output))


class PostEditForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['slug', ]


class PostAddForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['slug', ]

    tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all(),
                                          widget=HiddenMultiple(attrs={"class": "Aaa"}, choices=Tag.objects.values("title")),
                                          required=False,
                                          )

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
