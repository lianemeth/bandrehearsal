import unittest
from pyramid import testing


class TestMailers(unittest.TestCase):

    def setUp(self):
        self.config = testing.setUp(settings={
            'bandrehearsal.mail_address': 'daband@algo.com',
            'bandrehearsal.mail_server': 'smtp.algo.com'
        })

    def tearDown(self):
        testing.tearDown()

    def test_MailAction(self):
        from ..mailers import mailaction

        class MockMailer:
            def __init__(self, item):
                self.item = item

            def send(self, message):
                return

        mailaction.Mailer = MockMailer
        request = testing.DummyRequest()
        mail = mailaction.MailAction('test@example.com', request=request)
        mail.subject = 'something'
        mail.html = '<h1> hi </h1>'
        self.assertTrue(mail.message)
        self.assertTrue(mail.server)
        mail.send()
        mail = mailaction.MailAction('test@example.com',
                From='me@example.com', server="smtp.example.com",
                randomstuff=10)
        mail.subject = 'something'
        mail.html = '<h1> hi </h1>'
        mail.send()
        self.assertEqual(mail.randomstuff, 10)
