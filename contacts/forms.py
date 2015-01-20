# -*- coding: utf-8 -*-
from django import forms


class ContactForm(forms.Form):
    sender = forms.EmailField(label='Your email address',)
    message = forms.CharField(widget=forms.Textarea)
