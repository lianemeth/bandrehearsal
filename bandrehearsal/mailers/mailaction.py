from mailer import Mailer, Message


class MailAction(object):

    def __init__(self, To, From=None, request=None,
            charset='utf-8', server=None, **kw):
        settings = request.registry.settings if request else {}
        From = From or settings['bandrehearsal.mail_address']
        self.server = server or settings['bandrehearsal.mail_server']
        self.message = Message(From=From, To=To, charset=charset)
        for key in kw:
            setattr(self, key, kw[key])

    def render(self):
        self.message.Subject = self.subject
        self.message.Html = self.html

    def send(self):
        self.render()
        sender = Mailer(self.server)
        sender.send(self.message)
