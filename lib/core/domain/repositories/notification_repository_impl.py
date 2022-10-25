from lib.core.data.datasource.notification_remote_source import (
    NotificationRemoteSource,
)
from lib.core.data.repositories.notification_repository import NotificationRepository


class NotificationRepositoryImpl(NotificationRepository):
    def __init__(self, notification_source: NotificationRemoteSource):
        self._notification_source = notification_source

    def send_notification(self, to, message):
        self._notification_source.send_notification(to, message)
