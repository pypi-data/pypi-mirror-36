Usage
-----

1. Install
~~~~~~~~~~
::

    $ pip install django-rds-db-multitenant

2. Implement a mapper
~~~~~~~~~~~~~~~~~~~~~

3. Update settings.py
~~~~~~~~~~~~~~~~~~~~~

Set the multitenant mapper by specifying the full dotted path to your
implementation (in this example, `mapper` is the name of file `mapper.py`):

.. code:: python

    MULTITENANT_MAPPER_CLASS = 'myapp.mapper.TenantMapper'

Install the multitenant middleware as the *first* middleware of the list (prior to Django
1.10, you must use the ``MIDDLEWARE_CLASSES`` setting):

.. code:: python

    MIDDLEWARE = [
        'rds_db_multitenant.middleware.MultiTenantMiddleware',
        ....
    ]

Change your database backend to the multitenant wrapper:

.. code:: python

    DATABASES = {
        'default': {
            'ENGINE': 'rds_db_multitenant.db.backends.mysql',
            'NAME': 'devnull',
        }
    }

*Note*: the ``NAME`` is useless for MySQL but due to a current
limitation, the named database must exist. It may be empty and
read-only.

Optionally, add the multitenant helper ``KEY_FUNCTION`` to your cache
definition, which will cause cache keys to be prefixed with the value of
``mapper.get_cache_prefix``:

.. code:: python

    CACHES = {
      'default' : {
            'LOCATION': '127.0.0.1:11211',
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'KEY_FUNCTION': 'rds_db_multitenant.cache.helper.multitenant_key_func'
        }
    }
