from django.core import mail
from django .test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeGet(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Response must return 200 as status code"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """Response should be using the template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):

        tags = (('<form', 1),
                ('<input', 6),
                ('type="text"', 3),
                ('type="email"', 1),
                ('type="submit"', 1))

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.response, text, count)

    def test_csrf(self):
        """The page must contain the CSRF Token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)


class SubscribePostValid(TestCase):
    def setUp(self):
        data = {'name':'Arthur', 'cpf': '12345678901',
                'email': 'arthur@nobrega.net', 'phone': '61 1234-5678'}
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(self.response.status_code, 302)

    def test_send_subscribe_email(self):
        self.assertEqual(len(mail.outbox), 1)


class SubscribePostInvalid(TestCase):
    def setUp(self):
        self.response = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(200, self.response.status_code)

    def test_template(self):
        """The template should be subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_form(self):
        """The page must include the form in the context"""
        form = self.response.context['form']

        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        """The form should contain errors"""
        form = self.response.context['form']

        self.assertTrue(form.errors)

class SubscribeSuccessfulMessage(TestCase):
    def test_message(self):
        data = {'name':'Arthur', 'cpf': '12345678901',
                'email': 'arthur@nobrega.net', 'phone': '61 1234-5678'}
        response = self.client.post('/inscricao/', data, follow=True)

        self.assertContains(response, 'Inscrição realizada com sucesso!')