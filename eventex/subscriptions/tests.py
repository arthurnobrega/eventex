from django.core import mail
from django .test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscribeTest(TestCase):
    def setUp(self):
        self.response = self.client.get('/inscricao/')

    def test_get(self):
        """Response must return 200 as status code"""
        self.assertEqual(self.response.status_code, 200)

    def test_template(self):
        """Response should be using the template subscriptions/subscription_form.html"""
        self.assertTemplateUsed(self.response, 'subscriptions/subscription_form.html')

    def test_html(self):
        """The page must contain a form with 5 inputs"""
        self.assertContains(self.response, '<form')
        self.assertContains(self.response, '<input', 6)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, 'type="submit"')

    def test_csrf(self):
        """The page must contain the CSRF Token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_has_form(self):
        """Context must have subscription form"""
        form = self.response.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have 4 fields"""
        form = self.response.context['form']
        self.assertSequenceEqual(list(form.fields), ['name', 'cpf', 'email', 'phone'])


class SubscribeSuccessPost(TestCase):
    def setUp(self):
        data = {'name':'Arthur', 'cpf': '12345678901',
                'email': 'arthur@nobrega.net', 'phone': '61 1234-5678'}
        self.response = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid POST should redirect to /inscricao/"""
        self.assertEqual(self.response.status_code, 302)

    def test_send_subscribe_email(self):
        self.assertEqual(len(mail.outbox), 1)

    def test_subscribe_email_subject(self):
        email = mail.outbox[0]
        expect = 'Confirmação de inscrição'

        self.assertEqual(email.subject, expect)

    def test_subscribe_email_from(self):
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(email.from_email, expect)

    def test_subscribe_email_to(self):
        email = mail.outbox[0]
        expect = ['arthur@nobrega.net', 'contato@eventex.com.br']

        self.assertEqual(email.to, expect)

    def test_subscribe_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Arthur', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('arthur@nobrega.net', email.body)
        self.assertIn('61 1234-5678', email.body)


class SubscribeInvalidPost(TestCase):
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