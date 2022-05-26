from datetime import datetime, date
from typing import List

from config import config
from lib.core.domain.entities.employee import Employee
from lib.core.domain.repositories.notification_repository import NotificationRepository
from lib.features.birthday_notification.data.repositories.employees_repository import EmployeesRepository
from lib.features.birthday_notification.domain.usecases.birthday_notification import BirthdayNotificationUseCase


class BirthdayNotificationUseCaseImpl(BirthdayNotificationUseCase):

    def __init__(self, notification_repo: NotificationRepository, employees_repo: EmployeesRepository):
        self._notification_repo = notification_repo
        self._employees_repo = employees_repo

    def _is_it_employees_birthday(self, emp: Employee, date_to_check: datetime):
        # TODO: Consider leap years
        return emp.dateOfBirth.month == date_to_check.month and emp.dateOfBirth.day == date_to_check.day

    def _filter_by_employees_today_birthdays(self, employees_list: List[Employee]) -> List[Employee]:
        # todays_date = datetime.strptime('2022-01-15', '%Y-%m-%d')
        todays_date = datetime.now()
        return list(filter(
            lambda emp: self._is_it_employees_birthday(emp, todays_date),
            employees_list))

    def _should_emplyee_be_included(self, emp: Employee, excluded_employees_ids: List[int], date_filter: datetime):
        return emp.id not in excluded_employees_ids \
               and emp.employmentEndDate is None \
               and emp.employmentStartDate is not None \
               and emp.employmentStartDate <= date_filter

    def _filter_excluded_employees(
            self,
            employees_list: List[Employee],
            excluded_employees_ids: List[int]) -> List[Employee]:
        today_date = datetime.now()

        return list(
            filter(lambda emp: self._should_emplyee_be_included(emp, excluded_employees_ids, today_date),
                   employees_list)
        )

    async def send_birthday_notification(self):
        """
        Sends awesome company birthday message
        """
        employees_list = await self._employees_repo.get_all_employees()
        employees_ids_to_exclude = await self._employees_repo.get_employees_ids_to_not_send_birthday_notification()

        employees_not_excluded = self._filter_excluded_employees(employees_list, employees_ids_to_exclude)

        today_employees_birthday = self._filter_by_employees_today_birthdays(employees_not_excluded)

        names_of_employees = list(map(lambda emp: emp.name, today_employees_birthday))
        message = "Happy Birthday! " + ", ".join(names_of_employees)
        self._notification_repo.send_notification(config.recipient, message)

