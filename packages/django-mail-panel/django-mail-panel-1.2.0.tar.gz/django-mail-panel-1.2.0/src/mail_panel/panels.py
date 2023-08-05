from django.utils.translation import ugettext_lazy as _

from collections import OrderedDict
import datetime

from debug_toolbar.panels import DebugPanel

from .conf import MAIL_TOOLBAR_TTL
from .utils import load_outbox, save_outbox
from .urls import urlpatterns

class MailToolbarPanel(DebugPanel):
    """
    Panel that displays informations about mail
    """
    name = 'Mail'
    template = 'mail_panel/panel.html'
    has_content = True
    mail_list = OrderedDict()

    def nav_title(self):
        return _('Mail')

    def nav_subtitle(self):
        mail_list = load_outbox()
        unread_count = 0
        for message in list(mail_list.values()):
            if not message.read:
                unread_count += 1
        if unread_count == 1:
            return '{0} unread message'.format(unread_count)
        elif unread_count > 1:
            return '{0} unread messages'.format(unread_count)
        return ''

    def title(self):
        return _('Mail')

    def process_response(self, request, response):
        """
        Main panel view.  Loads and displays listing of mail.
        """

        mail_list = load_outbox()
        if mail_list == {}:
            return
        mail_list = OrderedDict(
            sorted(iter(mail_list.items()),
            key=lambda x: x[1].date_sent,
            reverse=True
        ))
        prev_len = len(mail_list)

        # Expire messages past TTL
        expire_at = datetime.datetime.now() - datetime.timedelta(
            seconds=MAIL_TOOLBAR_TTL)
        for message_id, message in list(mail_list.items()):
            if message.date_sent < expire_at:
                del mail_list[message_id]

        if prev_len != len(mail_list):
            save_outbox(mail_list)

        self.mail_list = mail_list
        self.record_stats({
            'mail_list': self.mail_list,
        })

    @classmethod
    def get_urls(cls):
        return urlpatterns
