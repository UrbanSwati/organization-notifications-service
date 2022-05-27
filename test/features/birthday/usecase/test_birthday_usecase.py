import calendar
import json
from datetime import datetime
from typing import Optional, Dict

import pytest

from lib.core.data.datasource.notification_remote_source_impl import NotificationRemoteSourceImpl
from lib.core.data.repositories.notification_repository_impl import NotificationRepositoryImpl
from lib.core.domain.entities.employee import Employee
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


async def mock_get(*args, **kwargs):
    if kwargs.get('url', '').endswith('/employees'):
        return MockEmployeesResponse()
    return MockExcludedEmployeesResponse()


@pytest.mark.skip('Used for debugging purposes')
@pytest.mark.asyncio
async def test_send_birthday_notification(monkeypatch):
    monkeypatch.setattr(MockHTTPClient, "get", mock_get)

    notification_repo = NotificationRepositoryImpl(NotificationRemoteSourceImpl())

    employees_data_source = EmployeesRemoteSourceImpl(MockHTTPClient())
    employees_repo = EmployeesRepositoryImpl(employees_data_source)
    use_case = BirthdayNotificationUseCaseImpl(notification_repo, employees_repo)

    await use_case.send_birthday_notification()


def test_should_filter_by_excluded_employee_ids():
    id_to_exclude = 101
    test_employees = [
        Employee(id=100, name='Test', lastName='Test123', dateOfBirth=datetime(1960, 3, 13, 0, 0),
                 employmentStartDate=datetime(2001, 3, 1, 0, 0), employmentEndDate=None,
                 lastNotification=datetime(2022, 3, 16, 12, 16, 3, 515696),
                 lastBirthdayNotified=datetime(2022, 5, 4, 0, 0)),
        Employee(id=id_to_exclude, name='Anders2', lastName='Hejlsberg',
                 dateOfBirth=datetime(1960, 12, 2, 0, 0),
                 employmentStartDate=datetime(2001, 3, 1, 0, 0))]

    filtered_employees = BirthdayNotificationUseCaseImpl.filter_excluded_employees(test_employees, [id_to_exclude])
    assert len(test_employees) > len(filtered_employees)
    assert id_to_exclude not in list(map(lambda emp: emp.id, filtered_employees))


def test_should_return_employees_that_have_birthday_of_given_date(monkeypatch):
    given_date = datetime.strptime('2022-01-15', '%Y-%m-%d')

    test_employees = [
        Employee(id=20, name='Test', lastName='Test123', dateOfBirth=datetime(1960, 3, 13, 0, 0),
                 employmentStartDate=datetime(2001, 3, 1, 0, 0), employmentEndDate=None,
                 lastNotification=datetime(2022, 3, 16, 12, 16, 3, 515696),
                 lastBirthdayNotified=datetime(2022, 5, 4, 0, 0)),
        Employee(id=29, name='Anders2', lastName='Hejlsberg',
                 dateOfBirth=datetime(1960, 1, 15, 0, 0),
                 employmentStartDate=datetime(2001, 3, 1, 0, 0))]

    monkeypatch.setattr(MockHTTPClient, "get", mock_get)

    notification_repo = NotificationRepositoryImpl(NotificationRemoteSourceImpl())

    employees_data_source = EmployeesRemoteSourceImpl(MockHTTPClient())
    employees_repo = EmployeesRepositoryImpl(employees_data_source)
    use_case = BirthdayNotificationUseCaseImpl(notification_repo, employees_repo)

    employees_who_have_birthdays = use_case._filter_by_employees_birthdays(test_employees, given_date)
    assert len(employees_who_have_birthdays) < len(test_employees)
    for employee in employees_who_have_birthdays:
        assert employee.dateOfBirth.month == given_date.month
        assert employee.dateOfBirth.day == given_date.day


def test_should_return_employees_that_have_birthday_of_given_date_in_leap_years(monkeypatch):
    given_date = datetime.strptime('2022-02-28', '%Y-%m-%d')

    test_employees = [
        Employee(id=20, name='Test', lastName='Test123', dateOfBirth=datetime(1960, 3, 13, 0, 0),
                 employmentStartDate=datetime(2001, 3, 1, 0, 0), employmentEndDate=None,
                 lastNotification=datetime(2022, 3, 16, 12, 16, 3, 515696),
                 lastBirthdayNotified=datetime(2022, 5, 4, 0, 0)),
        Employee(id=29, name='Anders2', lastName='Hejlsberg',
                 dateOfBirth=datetime(1984, 2, 29, 0, 0),  # 1984 was  the 80s leap year
                 employmentStartDate=datetime(2001, 3, 1, 0, 0))]

    monkeypatch.setattr(MockHTTPClient, "get", mock_get)

    notification_repo = NotificationRepositoryImpl(NotificationRemoteSourceImpl())

    employees_data_source = EmployeesRemoteSourceImpl(MockHTTPClient())
    employees_repo = EmployeesRepositoryImpl(employees_data_source)
    use_case = BirthdayNotificationUseCaseImpl(notification_repo, employees_repo)

    employees_who_have_birthdays = use_case._filter_by_employees_birthdays(test_employees, given_date)
    assert len(employees_who_have_birthdays) < len(test_employees)
    for employee in employees_who_have_birthdays:
        assert calendar.isleap(employee.dateOfBirth.year)
        assert employee.dateOfBirth.month == given_date.month
        assert employee.dateOfBirth.day == given_date.day + 1
