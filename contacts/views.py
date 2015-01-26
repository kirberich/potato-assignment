# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.views.generic.edit import FormView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from google.appengine.api import mail

from .forms import ContactForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactView(FormView):

    template_name = "contacts/contacts.html"
    form_class = ContactForm
    success_message = "Thanks for contacting us. We will get in touch asap."

    def form_valid(self, form):
        sender = form.cleaned_data['sender']
        message = "Message received from %s\n\n" % sender
        message += form.cleaned_data['message']
        recipients = [email[1] for email in settings.ADMINS]
        admin = recipients[0]
        subject = "[potato-assigment blog] Information request"
        self.success_url = reverse('homepage')

        try:
            email = mail.EmailMessage(sender=admin,
                                      subject=subject,
                                      body=message,
                                      to=recipients)
            email.send()
            messages.add_message(self.request,
                                 messages.INFO,
                                 self.success_message)
        except Exception as e:
            logger.error("Error '%s' sending the mail" % str(e))
            messages.add_message(self.request,
                                 messages.ERROR,
                                 "Error sending the mail: Contact us at \
                                 potato-assigment@google.com to inform \
                                 us about the error. Thanks")
        return super(ContactView, self).form_valid(form)

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(ContactView, self).dispatch(*args, **kwargs)
