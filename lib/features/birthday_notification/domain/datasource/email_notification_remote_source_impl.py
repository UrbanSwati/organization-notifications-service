from lib.core.domain.datasource.notification_remote_source import (
    NotificationRemoteSource,
)
from lib.core.platform.mail_client import MailClient


class EmailNotificationRemoteSource(NotificationRemoteSource):
    def __init__(self, mail_client: MailClient):
        self._mail_client = mail_client

    def send_notification(self, to, message):
        self._mail_client.send_mail(to, message)
