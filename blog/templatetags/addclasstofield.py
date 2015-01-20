# -*- coding: utf-8 -*-
from django import template
register = template.Library()


@register.filter(name='addclasstofield')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})
