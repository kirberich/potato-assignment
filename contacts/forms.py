from django import forms


class ContactForm(forms.Form):
    sender = forms.EmailField(label='Your email address',)
    message = forms.CharField(label='Message')