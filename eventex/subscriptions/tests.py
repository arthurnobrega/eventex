from django .test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionTest(TestCase):
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
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 3)
        self.assertContains(self.response, 'type="email"')
        self.assertContains(self.response, '<button type="submit"')

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