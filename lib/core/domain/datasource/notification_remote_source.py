from abc import ABC, abstractmethod


class NotificationRemoteSource(ABC):
    @abstractmethod
    def send_notification(self, to, message):
        pass
