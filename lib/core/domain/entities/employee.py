from copy import copy
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict

from lib.core.domain.entities.user import User


@dataclass(frozen=True, order=True)
class Employee(User):
    date_of_birth: datetime
    employment_start_date: datetime
    employment_end_date: Optional[datetime] = None
    last_notification: Optional[datetime] = None
    last_birthday_notified: Optional[datetime] = None

    @classmethod
    def from_dict(cls, data: Dict, dateformat: str = '%Y-%m-%dT%H:%M:%S'):
        """
        Takes a dictionary and serialize it to Employee class
        :param data: dictionary
        :param dateformat: string formate type for all datetime fields
        :return: Employee
        """
        employee_dict = copy(data)

        for property_name in ['date_of_birth', 'employment_start_date', 'employment_end_date', 'last_notification',
                              'last_birthday_notified']:
            property_value = data.get(property_name)
            employee_dict[property_name] = datetime.strptime(property_value, dateformat) if property_value else None

        return cls(**employee_dict)
