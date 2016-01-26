from django.core import mail
from django.test import TestCase


class SubscribePostValid(TestCase):
    def setUp(self):
        data = {'name':'Arthur', 'cpf': '12345678901',
                'email': 'arthur@nobrega.net', 'phone': '61 1234-5678'}
        self.response = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscribe_email_subject(self):
        expect = 'Confirmação de inscrição'

        self.assertEqual(self.email.subject, expect)

    def test_subscribe_email_from(self):
        expect = 'contato@eventex.com.br'

        self.assertEqual(self.email.from_email, expect)

    def test_subscribe_email_to(self):
        expect = ['contato@eventex.com.br', 'arthur@nobrega.net']

        self.assertEqual(self.email.to, expect)

    def test_subscribe_email_body(self):
        contents = ['Arthur', '12345678901', 'arthur@nobrega.net', '61 1234-5678']
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)