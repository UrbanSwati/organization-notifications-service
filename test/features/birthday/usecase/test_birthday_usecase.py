import datetime
import json
from typing import Optional, Dict

import pytest

from lib.core.data.datasource.notification_remote_source_impl import NotificationRemoteSourceImpl
from lib.core.data.repositories.notification_repository_impl import NotificationRepositoryImpl
from lib.core.platform.http_client import HTTPClient, Response
from lib.features.birthday_notification.data.usecase.birthday_notification_impl import BirthdayNotificationUseCaseImpl
from lib.features.birthday_notification.domain.datasource.employees_remote_source_impl import EmployeesRemoteSourceImpl
from lib.features.birthday_notification.domain.repositories.employees_repository_impl import EmployeesRepositoryImpl


class MockHTTPClient(HTTPClient):
    async def get(self, url: str, headers: Optional[Dict] = None, timeout: int = 10) -> Response:
        pass


class MockEmployeesResponse:
    status = 200

    @staticmethod
    def json():
        with open('./test/fixtures/employees_mock.json', 'r') as file:
            return json.load(file)


class MockExcludedEmployeesResponse:
    status = 200

    @staticmethod
    def json():
        with open('./test/fixtures/do_not_send_birthday_wishes_mock.json', 'r') as file:
            return json.load(file)


MOCK_NOW_DATETIME = datetime.datetime.strptime('2022-01-15', '%Y-%m-%d')


@pytest.mark.asyncio
async def test_send_birthday_notification(monkeypatch):
    async def mock_get(*args, **kwargs):
        if kwargs.get('url', '').endswith('/employees'):
            return MockEmployeesResponse()
        return MockExcludedEmployeesResponse()

    class mockdatetime:
        @classmethod
        def now(cls):
            return MOCK_NOW_DATETIME

    monkeypatch.setattr(MockHTTPClient, "get", mock_get)
    monkeypatch.setattr(datetime, "datetime", mockdatetime)

    notification_repo = NotificationRepositoryImpl(NotificationRemoteSourceImpl())

    employees_data_source = EmployeesRemoteSourceImpl(MockHTTPClient())
    employees_repo = EmployeesRepositoryImpl(employees_data_source)
    use_case = BirthdayNotificationUseCaseImpl(notification_repo, employees_repo)

    await use_case.send_birthday_notification()
