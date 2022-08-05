# Organization Notifications Service
[![Python package](https://github.com/UrbanSwati/organization-notifications-service/actions/workflows/python-package.yml/badge.svg)](https://github.com/UrbanSwati/organization-notifications-service/actions/workflows/python-package.yml)

Service component that will send birthday wishes to employees with the ability be extended by developers to send any
type of notifications for an organization

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing
purposes.

### Prerequisites

Things you need to get start with the service and how to install them.

- [Python 3.6 >=](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [Pipenv](https://pipenv.pypa.io/en/latest/) - 
  *Pipenv is optional, you could use the standard pip for dependencies*

### Installing

A step by step series of examples that tell you how to get a development env running

After installing Python and Pip or Pipenv you need to install the dependencies.

Using Pip:

```
pip install -r requirements.txt
```

Using Pipenv:

```
pipenv install -d
```

*It's always best pratice to use a virtual enviornment, pipenv handles virtual enviornments for you out the box but pip
doesn't. read more about virtual environments in
python [here](https://www.dataquest.io/blog/a-complete-guide-to-python-virtual-environments/)*

Create a `.env` file in the root directory which will contain your environment variables for the service. You can copy
the `.env.example` file which has an example of required environment variables for the service. Optional you can set the
environment variables on your OS and the project should read them from there.

## Running the Birthday Notification Service

Run this command to run the default birthday notification

```
python main.py
```

## Running the tests

To run tests, run this command in the project root directory

```
pytest 
```

Run test with coverage

```
pytest --cov
```

## Built With

* [Love]() - The thing that makes the world go round
* [Coffee]() - Energy Management for developers
* [Computer]() - Used to generate code

## Contributing

Wide wild west - Anything goes.

## Acknowledgments

* Stackoverflow
* Google
* Github
* Youtube
* etc

