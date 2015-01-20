# -*- coding: utf-8 -*-
from django import forms

from .models import Post
from .models import Tag
from .models import Comment


class ModelMultipleSelect2Field(forms.ModelMultipleChoiceField):

    def clean(self, data):
        tags = []
        if not data:
            data = []
        for tag in data:
            try:
                tags.append(Tag.objects.get(pk=tag))
            except:
                tags.append(Tag.objects.create(title=tag))
        return tags


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ['slug', ]

    tags = ModelMultipleSelect2Field(queryset=Tag.objects.all())


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        exclude = ['slug', ]
