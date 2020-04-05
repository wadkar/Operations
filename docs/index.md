# Operations-org

[![Build Status](https://travis-ci.org/GoCorona-org/Operations-org.svg?branch=master)](https://travis-ci.org/GoCorona-org/Operations-org)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

API for Covid-19 Hotspot detection and rapid response.. Check out the project's [documentation](http://GoCorona-org.github.io/Operations-org/).

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

# Initialize the project

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```
