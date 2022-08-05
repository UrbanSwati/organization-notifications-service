from datetime import datetime

from lib.core.domain.entities.employee import Employee

employee = Employee(
    id=1,
    name="test",
    lastName="last_name",
    dateOfBirth=datetime.now(),
    employmentStartDate=datetime.now(),
)


def test_should_be_a_of_employee_entity():
    assert isinstance(employee, Employee)


def test_should_be_able_to_cast_to_dict():
    employee_dict = employee.to_dict()
    expected_dict = {
        "id": employee.id,
        "name": employee.name,
        "lastName": employee.lastName,
        "dateOfBirth": employee.dateOfBirth,
        "lastBirthdayNotified": employee.lastBirthdayNotified,
        "lastNotification": employee.lastNotification,
        "employmentStartDate": employee.employmentStartDate,
        "employmentEndDate": employee.employmentEndDate,
    }

    assert employee_dict == expected_dict


def test_should_serialize_dict_to_class():
    given_employee_dict = {
        "id": 100,
        "name": "Test",
        "lastname": "Test123",
        "dateOfBirth": "1960-03-13T00:00:00",
        "employmentStartDate": "2001-03-01T00:00:00",
        "employmentEndDate": None,
        "lastNotification": "2022-03-16T12:16:03.5156964+02:00",
        "lastBirthdayNotified": "2022-05-04",
    }

    employee_object = Employee.from_dict(given_employee_dict)
    assert isinstance(employee_object, Employee)
    assert isinstance(employee_object.employmentStartDate, datetime)
    assert employee_object.id == given_employee_dict["id"]
    assert employee_object.name == given_employee_dict["name"]
