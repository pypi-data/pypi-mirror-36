Django AsyncViews
=================

![Build](https://git.steadman.io/podiant/django-asyncviews/badges/master/build.svg)
![Coverage](https://git.steadman.io/podiant/django-asyncviews/badges/master/coverage.svg)

Asynchronous JSON/HTML view library

## Quickstart

Install Django AsyncViews:

```sh
pip install django-asyncviews
```

Add it to your `INSTALLED_APPS`:
```python
INSTALLED_APPS = (
    ...
    'asyncviews',
    ...
)
```

Add AsyncViews' URL patterns:

```python
from asyncviews import urls as asyncviews_urls

urlpatterns = [
    ...
    url(r'^', include(asyncviews_urls)),
    ...
]
```

## Running tests

Does the code actually work?

```
coverage run --source asyncviews runtests.py
```

## Credits

Tools used in rendering this package:

- [Cookiecutter](https://github.com/audreyr/cookiecutter)
- [`cookiecutter-djangopackage`](https://github.com/pydanny/cookiecutter-djangopackage)
