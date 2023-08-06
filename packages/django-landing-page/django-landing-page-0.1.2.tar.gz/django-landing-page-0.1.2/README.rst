=============================
django-landing-page
=============================

.. image:: https://badge.fury.io/py/django-landing-page.svg
    :target: https://badge.fury.io/py/django-landing-page

.. image:: https://travis-ci.org/weholt/django-landing-page.svg?branch=master
    :target: https://travis-ci.org/weholt/django-landing-page

.. image:: https://codecov.io/gh/weholt/django-landing-page/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/weholt/django-landing-page

About
-----

A reusable app to create and manage a landing page for your project - with supplied themes.

- Version 0.1.1 - initial release, not ready for general use. Seriously. Don't.
- Project home: https://github.com/weholt/django-landing-page
- Author: thomas@weholt.org


Quickstart
----------

Install django-landing-page::

    pip install django-landing-page

Add the app and it requirements to your `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'landing_page',
        'fontawesome',
        'sorl.thumbnail',
        'ckeditor',
        ...
    )

See the requirements.txt in the source-folder at github for details.

Add django-landing-page's URL patterns:

.. code-block:: python

    from landing_page import urls as landing_page_urls


    urlpatterns = [
        ...
        url(r'^', include('landing_page.urls', namespace='landing_page')),
        ...
    ]

Features
--------

* TODO

Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
