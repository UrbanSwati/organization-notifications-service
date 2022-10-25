import calendar
import logging
from datetime import datetime
from typing import List

from config import config
from lib.core.domain.entities.employee import Employee
from lib.core.data.repositories.notification_repository import NotificationRepository
from lib.features.birthday_notification.data.repositories.employees_repository import (
    EmployeesRepository,
)
from lib.features.birthday_notification.data.usecase.birthday_notification import (
    BirthdayNotificationUseCase,
)

logging.basicConfig(level=logging.DEBUG)


class BirthdayNotificationUseCaseImpl(BirthdayNotificationUseCase):
    def __init__(
        self,
        notification_repo: NotificationRepository,
        employees_repo: EmployeesRepository,
    ):
        self._notification_repo = notification_repo
        self._employees_repo = employees_repo

    def _is_it_employees_birthday(self, emp: Employee, date_to_check: datetime):
        birthday_month = emp.dateOfBirth.month
        birthday_day = emp.dateOfBirth.day
        check_month = date_to_check.month
        check_day = date_to_check.day
        if (
            calendar.isleap(emp.dateOfBirth.year)
            and (birthday_month == 2 and birthday_day == 29)
            and (check_month == 2 and check_day == 28)
        ):
            return True
        return birthday_month == check_month and birthday_day == check_day

    def _filter_by_employees_birthdays(
        self, employees_list: List[Employee], date_to_check: datetime
    ) -> List[Employee]:
        return list(
            filter(
                lambda emp: self._is_it_employees_birthday(emp, date_to_check),
                employees_list,
            )
        )

    @staticmethod
    def _should_employee_be_included(
        emp: Employee, excluded_employees_ids: List[int], date_filter: datetime
    ):
        return (
            emp.id not in excluded_employees_ids
            and emp.employmentEndDate is None
            and emp.employmentStartDate is not None
            and emp.employmentStartDate <= date_filter
        )

    @staticmethod
    def filter_excluded_employees(
        employees_list: List[Employee], excluded_employees_ids: List[int]
    ) -> List[Employee]:
        today_date = datetime.now()

        return list(
            filter(
                lambda emp: BirthdayNotificationUseCaseImpl._should_employee_be_included(
                    emp, excluded_employees_ids, today_date
                ),
                employees_list,
            )
        )

    async def send_birthday_notification(self):
        """
        Sends awesome company birthday message
        """
        employees_list = await self._employees_repo.get_all_employees()
        logging.info(f"{len(employees_list)} Employees Retrieved")
        employees_ids_to_exclude = (
            await self._employees_repo.get_employees_ids_to_not_send_birthday_notification()
        )

        employees_not_excluded = self.filter_excluded_employees(
            employees_list, employees_ids_to_exclude
        )
        logging.info(
            f"{len(employees_not_excluded)} Employees excluded to birthday wishes :( "
        )

        # NOTE: You can change this date to test locally
        # date_to_check_birthday = datetime.strptime('2022-02-04', '%Y-%m-%d')
        date_to_check_birthday = datetime.now()

        today_employees_birthday = self._filter_by_employees_birthdays(
            employees_not_excluded, date_to_check_birthday
        )
        logging.info(
            f"{len(today_employees_birthday)} Employees to send birthday wishes"
        )
        if len(today_employees_birthday) > 0:
            # only send email if there is someone's awesome birthday :P
            names_of_employees = list(
                map(lambda emp: emp.name, today_employees_birthday)
            )
            message = "Happy Birthday! " + ", ".join(names_of_employees)
            self._notification_repo.send_notification(config.recipient, message)
