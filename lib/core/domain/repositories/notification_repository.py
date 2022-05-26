from abc import ABC, abstractmethod


class NotificationRepository(ABC):
    """
    Base notification class to be used
    """
    @abstractmethod
    def send_notification(self, to, message):
        """
        Sends notification
        """