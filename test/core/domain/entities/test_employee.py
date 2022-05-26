from datetime import datetime

from lib.core.domain.entities.employee import Employee
from lib.core.domain.entities.user import User

employee = Employee(id=1,
                    name='test',
                    last_name='last_name',
                    date_of_birth=datetime.now(),
                    employment_start_date=datetime.now())


def test_should_be_a_subclass_of_user_entity():
    assert isinstance(employee, Employee)
    assert isinstance(employee, User)


def test_should_be_able_to_cast_to_dict():
    employee_dict = employee.to_dict()
    expected_dict = {
        'id': employee.id,
        'name': employee.name,
        'last_name': employee.last_name,
        'date_of_birth': employee.date_of_birth,
        'last_birthday_notified': employee.last_birthday_notified,
        'last_notification': employee.last_notification,
        'employment_start_date': employee.employment_start_date,
        'employment_end_date': employee.employment_end_date
    }

    assert employee_dict == expected_dict


def test_should_serialize_dict_to_class():
    given_employee_dict = {
        'id': 77,
        'name': 'Zack',
        'last_name': 'Snyder',
        'date_of_birth': '1994-01-19T08:11:00',
        'last_birthday_notified': None,
        'last_notification': None,
        'employment_start_date': '2022-06-19T21:11:00',
        'employment_end_date': None
    }

    employee_object = Employee.from_dict(given_employee_dict)
    assert isinstance(employee_object, Employee)
    assert employee_object.id == given_employee_dict['id']
    assert employee_object.name == given_employee_dict['name']
