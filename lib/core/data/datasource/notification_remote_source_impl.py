from lib.core.domain.datasource.notification_remote_source import (
    NotificationRemoteSource,
)
import logging as log


class NotificationRemoteSourceImpl(NotificationRemoteSource):
    """
    This can use any type of notification (SMS, EMAIL etc)
    The implementation is up to the developer
    """

    async def send_notification(self, to, message):
        log.info(f"SENDING NOTIFICATION TO: {to}")
        log.info("----------------------")
        log.info(message)
        log.info("----- END MESSAGE ----")
