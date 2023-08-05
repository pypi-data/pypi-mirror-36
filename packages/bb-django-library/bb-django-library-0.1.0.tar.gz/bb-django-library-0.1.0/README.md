# bb-django-library

[![build status](https://img.shields.io/travis/openbox/bb-django-library.svg)](https://travis-ci.org/openbox/bb-django-library)
[![coverage](https://img.shields.io/codecov/c/github/openbox/bb-django-library.svg)](https://codecov.io/gh/openbox/bb-django-library)
[![PyPI version](https://img.shields.io/pypi/v/bb-django-library.svg)](https://pypi.org/project/bb-django-library/)
![python version](https://img.shields.io/pypi/pyversions/bb-django-library.svg)
![django version](https://img.shields.io/pypi/djversions/bb-django-library.svg)

This is an example repository for a simple Django library.


## Install

```bash
pip install bb-django-library
```


## Usage

```py
from bb_django_library.models import Foo

Foo.objects.create(bar='foobar')
```
