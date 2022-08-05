from abc import ABC
from pydantic import EmailStr


class MailClient(ABC):
    def send_mail(self, to: EmailStr, body: str):
        pass
