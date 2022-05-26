from abc import ABC, abstractmethod
from typing import List

from lib.core.domain.entities.employee import Employee


class EmployeesRepository(ABC):

    @abstractmethod
    async def get_all_employees(self) -> List[Employee]:
        """
        Get all employees of Realm Digital
        :return: List[Employee]
        """

    @abstractmethod
    async def get_employees_ids_to_not_send_birthday_notification(self) -> List[int]:
        """
        Get all employees that should not be included on birthday notification
        :return: List[int]
        """
