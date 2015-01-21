# -*- coding: utf-8 -*-
from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):
    list_filter = ('tags', )
    list_display = ('title', 'text', 'get_tags', 'created', 'modified', )

    def get_tags(self, obj):
        return "\n".join([t.title for t in obj.tags.all()])

admin.site.register(models.Tag)
admin.site.register(models.Comment)
admin.site.register(models.Post, PostAdmin)
