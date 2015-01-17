# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.mail import EmailMessage
from django.contrib import messages
from django.views.generic.edit import FormView

from .forms import ContactForm

import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactView(FormView):

    template_name = "contacts/contacts.html"
    form_class = ContactForm
    success_message = "Thanks for contacting us. We will get in touch asap."

    def form_valid(self, form):
        message = form.cleaned_data['message']
        recipients = [email[1] for email in settings.ADMINS]
        sender = form.cleaned_data['sender']
        subject = "[potato-assigment blog] Information request"

        try:
            email = EmailMessage(subject=subject,
                                 body=message,
                                 to=recipients,
                                 headers={'Reply-To': sender})
            email.send()
            messages.add_message(self.request,
                                 messages.INFO,
                                 self.success_message)
        except Exception as e:
            logger.error("Error '%s' sending the mail" % str(e))
            messages.add_message(self.request,
                                 messages.ERROR,
                                 "Error sending the mail: Contact us at \
                                 info at bagnialmare dot com to inform \
                                 us about the error. Thanks")
        return super(ContactView, self).form_valid(form)
