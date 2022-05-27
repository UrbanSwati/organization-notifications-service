from typing import List

from config import config
from lib.core.domain.entities.employee import Employee
from lib.core.error.exception import ServerException
from lib.core.platform.http_client import HTTPClient
from lib.features.birthday_notification.data.datasource.employees_remote_source import EmployeesRemoteSource


class EmployeesRemoteSourceImpl(EmployeesRemoteSource):

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client

    async def get_all_employees(self) -> List[Employee]:
        employees_list = []
        response = await self._http_client.get(url=f'{config.base_api_url}/employees')
        if response.status == 200:
            for employee in response.json():
                employees_list.append(Employee.from_dict(employee))
            return employees_list
        raise ServerException('Could not get employees')

    async def get_employee_ids_excluded_from_notification(self) -> List[int]:
        response = await self._http_client.get(url=f'{config.base_api_url}/do-not-send-birthday-wishes')
        if response.status == 200:
            return response.json()
        raise ServerException('Could not get employees excluded from notifications')
