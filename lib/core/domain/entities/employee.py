from copy import copy
from dataclasses import dataclass, asdict, astuple
from datetime import datetime
from typing import Optional, Dict

from dateutil.parser import parse


@dataclass(frozen=True, order=True)
class Employee:
    id: int
    name: str
    lastName: str
    dateOfBirth: datetime
    employmentStartDate: datetime
    employmentEndDate: Optional[datetime] = None
    lastNotification: Optional[datetime] = None
    lastBirthdayNotified: Optional[datetime] = None

    def to_dict(self) -> Dict:
        return asdict(self)

    def to_tuple(self) -> tuple:
        return astuple(self)

    @classmethod
    def from_dict(cls, data: Dict):
        """
        Takes a dictionary and serialize it to Employee class
        :param data: dictionary
        :return: Employee
        """
        employee_dict = copy(data)
        employee_dict['lastName'] = employee_dict.get('lastName', data.get('lastname'))

        del data['lastname']
        del employee_dict['lastname']

        for property_name in ['dateOfBirth', 'employmentStartDate', 'employmentEndDate', 'lastNotification',
                              'lastBirthdayNotified']:
            property_value = data.get(property_name)
            employee_dict[property_name] = parse(property_value) if property_value else None

        return cls(**employee_dict)
