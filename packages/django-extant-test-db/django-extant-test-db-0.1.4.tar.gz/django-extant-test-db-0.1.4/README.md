Django Extant Test DB
=====================

This package provides a Django test runner that uses unittest2 test discovery,
and can test against a pre-existing database when configured to do so.


## Quickstart

```bash
pip install django-extant-test-db
```

In _settings.py_, set the following:

```python
TEST_RUNNER = 'extant_test_db.runner.DiscoverRunner'
```

For any databases you want to be unmanaged by the test runner, add the
following:

```python
DATABASES = {
  ...
    'TEST': {
        'MANAGED': False,
    },
  ...
}
```

## Configuration

This package provides a Django test runner that uses unittest2 test discovery,
and can test against a pre-existing database when configured to do so. In order
to use an extant database for tests (e.g., if you have a large database full of 
read-only data), in your database TEST settings, set a MANAGED flag:

```python
DATABASES = {
    'default': {
        ...
    },
    'warehouse': {
        ...

        'TEST': {
            'MANAGED': False,
        },
    }
}
```

The database used will be the same as the one used for the webserver, though
you can also provide an alternative test database name:

```python
DATABASES = {
    ...
        'TEST': {
            'MANAGED': False,
            'NAME': os.environ['TEST_DB_NAME'],
        },
    ...
}
```