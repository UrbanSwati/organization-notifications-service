from abc import ABC, abstractmethod
from typing import List

from lib.core.domain.entities.employee import Employee


class EmployeesRemoteSource(ABC):
    @abstractmethod
    async def get_all_employees(self) -> List[Employee]:
        pass

    @abstractmethod
    async def get_employee_ids_excluded_from_notification(self) -> List[int]:
        pass
