from mailaction import MailAction
from pyramid.renderers import render

class NewBandMailer(MailAction):

    def render(self):
        self.message.Subject = u'%s, You were addded to the new Band %s' % (
            self.user, self.band)
        self.message.Html = render(
                'bandrehearsal:templates/mailers/newband.mako',
                {'band': self.band, 'user': self.user },
                request=self.request)
