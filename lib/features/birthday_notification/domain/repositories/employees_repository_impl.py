from typing import List

from lib.core.domain.entities.employee import Employee
from lib.features.birthday_notification.data.datasource.employees_remote_source import (
    EmployeesRemoteSource,
)
from lib.features.birthday_notification.data.repositories.employees_repository import (
    EmployeesRepository,
)


class EmployeesRepositoryImpl(EmployeesRepository):
    def __init__(self, data_source: EmployeesRemoteSource):
        self._data_source = data_source

    async def get_all_employees(self) -> List[Employee]:
        """
        Get all employees of Realm Digital
        :return: List[Employee]
        """

        # NOTE: besides fetching employees, we can even catch exceptions and handle them differently like fetch from
        # a different datasource source etc.

        return await self._data_source.get_all_employees()

    async def get_employees_ids_to_not_send_birthday_notification(self) -> List[int]:
        """
        Get all employees that should not be included on birthday notification
        :return: List[int]
        """
        return await self._data_source.get_employee_ids_excluded_from_notification()
