=============================
django-demo-site
=============================

.. image:: https://badge.fury.io/py/django-demo-site.svg
    :target: https://badge.fury.io/py/django-demo-site

.. image:: https://travis-ci.org/weholt/django-demo-site.svg?branch=master
    :target: https://travis-ci.org/weholt/django-demo-site

.. image:: https://codecov.io/gh/weholt/django-demo-site/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/weholt/django-demo-site

A reusable app to help manage a demo site.

Documentation
-------------

The full documentation is at https://django-demo-site.readthedocs.io.

Quickstart
----------

Install django-demo-site::

    pip install django-demo-site

Add it to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'demo_site.apps.DemoSiteConfig',
        ...
    )

Add django-demo-site's URL patterns:

.. code-block:: python

    from demo_site import urls as demo_site_urls


    urlpatterns = [
        ...
        url(r'^', include(demo_site_urls)),
        ...
    ]

Features
--------

* TODO

Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
