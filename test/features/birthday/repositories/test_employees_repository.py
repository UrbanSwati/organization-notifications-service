from typing import List

import pytest

from lib.core.domain.entities.employee import Employee
from lib.features.birthday_notification.data.datasource.employees_remote_source import EmployeesRemoteSource
from lib.features.birthday_notification.domain.repositories.employees_repository_impl import EmployeesRepositoryImpl


@pytest.mark.asyncio
async def test_should_get_employees():
    class MockDataSource(EmployeesRemoteSource):

        async def get_employee_ids_excluded_from_notification(self) -> List[int]:
            pass

        async def get_all_employees(self) -> List[Employee]:
            return [Employee.from_dict({'id': 100, 'name': 'Test', 'lastname': 'Test123',
                                        'dateOfBirth': '1960-03-13T00:00:00',
                                        'employmentStartDate': '2001-03-01T00:00:00', 'employmentEndDate': None,
                                        'lastNotification': '2022-03-16T12:16:03.5156964+02:00',
                                        'lastBirthdayNotified': '2022-05-04'})]

    employees_repo = EmployeesRepositoryImpl(MockDataSource())

    employees_list = await employees_repo.get_all_employees()
    assert len(employees_list) == 1


@pytest.mark.asyncio
async def test_should_get_employees_excluded_from_notifications():
    class MockDataSource(EmployeesRemoteSource):

        async def get_all_employees(self) -> List[Employee]:
            pass

        async def get_employee_ids_excluded_from_notification(self) -> List[int]:
            return [1, 2, 3]

    employees_repo = EmployeesRepositoryImpl(MockDataSource())

    employees_list = await employees_repo.get_employees_ids_to_not_send_birthday_notification()
    assert len(employees_list) == 3
