from abc import ABC, abstractmethod


class BirthdayNotificationUseCase(ABC):
    @abstractmethod
    async def send_birthday_notification(self):
        """
        Sends awesome company birthday message
        """
