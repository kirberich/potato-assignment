# -*- coding: utf-8 -*-
from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse
from google.appengine.ext import testbed

from forms import ContactForm


class ContactViewsTestCase(TestCase):

    def setUp(self):
        self.contacts_url = reverse('contact-form')
        self.c = Client()
        self.sender = "john.doe@example.com"
        self.message = "Hi there"
        self.testbed = testbed.Testbed()
        self.testbed.activate()
        self.testbed.init_mail_stub()
        self.mail_stub = self.testbed.get_stub(testbed.MAIL_SERVICE_NAME)

    def tearDown(self):
        pass

    def test_contacts(self):
        """ Test that the contacts returns 200 code using the right template
        """
        response = self.c.get(self.contacts_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacts/contacts.html')

    def test_contacts_content(self):
        """ Check only last 5 posts in hp (others are in second page)
        """
        response = self.c.get(self.contacts_url)
        self.assertIn('id_message', response.content)
        self.assertIn('id_sender', response.content)
        self.assertIn('<button', response.content)

    def test_form_valid_data(self):
        form = ContactForm({
            'sender': self.sender,
            'message': self.message,
        })
        self.assertTrue(form.is_valid())

    def test_form_blank_data(self):
        form = ContactForm({})
        self.assertFalse(form.is_valid())
        self.assertIn("sender", form.errors)
        self.assertIn("message", form.errors)

    def test_send_email(self):

        response = self.c.post(self.contacts_url,
                               {'sender': self.sender,
                                'message': self.message},
                               follow=True)
        self.assertTrue("Thanks for contacting us" in response.content)
        messages = self.mail_stub.get_sent_messages()
        self.assertEqual(1, len(messages))
        self.assertIn(self.message, messages[0].body.decode())
        self.assertIn(self.sender, messages[0].body.decode())
