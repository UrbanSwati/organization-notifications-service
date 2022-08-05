import asyncio
import logging

import smtplib
import ssl
from typing import Optional, Dict, Union, List

import aiohttp

from config import config
from lib.core.data.repositories.notification_repository_impl import (
    NotificationRepositoryImpl,
)
from lib.core.domain.datasource.notification_remote_source import (
    NotificationRemoteSource,
)
from lib.core.platform.http_client import HTTPClient, Response
from lib.features.birthday_notification.data.usecase.birthday_notification_impl import (
    BirthdayNotificationUseCaseImpl,
)
from lib.features.birthday_notification.domain.datasource.employees_remote_source_impl import (
    EmployeesRemoteSourceImpl,
)
from lib.features.birthday_notification.domain.repositories.employees_repository_impl import (
    EmployeesRepositoryImpl,
)

logging.basicConfig(level=logging.DEBUG)


class ClientResponse(Response):
    def __init__(self, status, body: Union[Dict, List]):
        self.status = status
        self._body = body

    def json(self) -> Union[Dict, List]:
        return self._body


class AsyncoHTTPClient(HTTPClient):
    async def get(
        self, url: str, headers: Optional[Dict] = None, timeout: int = 10
    ) -> Response:
        logging.info(f"Requesting GET {url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                status_code = response.status
                logging.info(f"Response status {status_code}")
                body = await response.json()
                return ClientResponse(status=status_code, body=body)


class MailNotification(NotificationRemoteSource):
    def __init__(self):
        self.context = ssl.create_default_context()

    def send_notification(self, to, message):
        with smtplib.SMTP(config.smtp_server, config.smtp_port) as server:
            try:
                server.starttls(context=self.context)
                logging.info(f"Logging in email: {config.smtp_sender_email}")
                server.login(config.smtp_sender_email, config.smtp_password)
                logging.info(f"Sending email to: {to}")
                email_message = f"""\
From: {config.org_name} Team <{config.smtp_sender_email}>
Subject: Happy Birthday!

{message}
"""
                server.sendmail(config.smtp_sender_email, to, email_message)
                logging.info("Email sent!")
            except Exception as ex_info:
                logging.error("Failed to send email")
                logging.error(ex_info, exc_info=True)


if __name__ == "__main__":
    notification_repo = NotificationRepositoryImpl(MailNotification())
    employees_data_source = EmployeesRemoteSourceImpl(AsyncoHTTPClient())
    employees_repo = EmployeesRepositoryImpl(employees_data_source)
    use_case = BirthdayNotificationUseCaseImpl(notification_repo, employees_repo)

    asyncio.run(use_case.send_birthday_notification())
