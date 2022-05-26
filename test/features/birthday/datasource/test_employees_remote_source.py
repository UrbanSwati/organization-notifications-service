import json

import pytest

from lib.core.error.exception import ServerException
from lib.core.platform.http_client import HTTPClient
from lib.features.birthday_notification.domain.datasource.employees_remote_source_impl import EmployeesRemoteSourceImpl


@pytest.mark.asyncio
async def test_should_get_employees_when_status_http_200():
    class MockResponse:
        status = 200

        @staticmethod
        def json():
            with open('./test/fixtures/employees_mock.json', 'r') as file:
                return json.load(file)

    class MockHTTPClient(HTTPClient):
        async def get(self, *args, **kwargs):
            return MockResponse()

    data_source = EmployeesRemoteSourceImpl(MockHTTPClient())
    all_employees = await data_source.get_all_employees()
    assert len(all_employees) == 129


@pytest.mark.asyncio
async def test_should_raise_exception_when_status_not_http_200():
    class MockResponse:
        status = 500

    class MockHTTPClient(HTTPClient):
        async def get(self, *args, **kwargs):
            return MockResponse()

    data_source = EmployeesRemoteSourceImpl(MockHTTPClient())

    with pytest.raises(ServerException) as e_info:
        await data_source.get_all_employees()
        assert e_info == 'Could not get employees'


@pytest.mark.asyncio
async def test_should_get_employees_ids_when_status_http_200():
    class MockResponse:
        status = 200

        @staticmethod
        def json():
            with open('./test/fixtures/do_not_send_birthday_wishes_mock.json', 'r') as file:
                return json.load(file)

    class MockHTTPClient(HTTPClient):
        async def get(self, *args, **kwargs):
            return MockResponse()

    data_source = EmployeesRemoteSourceImpl(MockHTTPClient())
    all_employees = await data_source.get_employee_ids_excluded_from_notification()
    assert len(all_employees) == 3


@pytest.mark.asyncio
async def test_should_raise_exception_when_failed_to_get_excluded_employees_ids():
    class MockResponse:
        status = 500

    class MockHTTPClient(HTTPClient):
        async def get(self, *args, **kwargs):
            return MockResponse()

    data_source = EmployeesRemoteSourceImpl(MockHTTPClient())

    with pytest.raises(ServerException) as e_info:
        await data_source.get_all_employees()
        assert e_info == 'Could not get employees excluded from notifications'
