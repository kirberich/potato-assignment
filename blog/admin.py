from django.contrib import admin
from . import models


class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'text']
    list_filter = ['tags']
    list_display = ['title', 'text', 'tags', 'created', 'modified', ]

admin.site.register(models.Post, PostAdmin)
