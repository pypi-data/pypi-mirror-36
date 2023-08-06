

.. nlx_middleware documentation master file, created by startproject.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to nlx_middleware's documentation!
=================================================

:Version: 0.1.0
:Source: https://github.com/maykinmedia/nlx_middleware
:Keywords: ``<keywords>``
:PythonVersion: 3.6

|build-status| |requirements| |coverage|

|python-versions| |django-versions| |pypi-version|

A Django middleware to integrate your service with `NLx`_.

This middleware takes care of rewriting URLs in the linked-data responses if
you're operating in the NLx network. This makes it possible to use the
NLx-outway URLs everywhere, while still saving/linking data against their
canonical URLs.

.. contents::

.. section-numbering::

Features
========

* Rewriting of NLx outway URLs in the request body to canonical URLs
* Rewriting of canonical URLs in the response body to NLx outway URLs
* Rewrites URLs in GET query params
* Leverages the OpenAPI schema to figure out what needs rewriting

TODO:
-----

* Set up registry of external services to rewrite as well
* Support OAS 3.0 (via ``gemma-zds-client``)

Installation
============

Requirements
------------

* Python 3.6 or above
* setuptools 30.3.0 or above
* Django 1.11 or above
* django-rest-framework
* the API schema must be available at ``{API_ROOT}/schema/openapi.yaml``
  (currently Swagger 2.0 is supported)
* ``gemma-zds-common`` (recommended)


Install
-------

.. code-block:: bash

    pip install nlx-middleware


Usage
=====

Add the middleware to you ``MIDDLEWARE`` setting:

.. code-block:: python

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        ...
        'nlx_middleware.middleware.NLxInwayURLRewriteMiddleware',
    ]

We recommend to put it as close to the end as possible. Review the Django
middleware documentation to see why the order matters.

Next, ensure the following settings are defined:

.. code-block:: python

    NLX_SERVICE = os.getenv('NLX_SERVICE', 'zrc')
    NLX_INWAY_ADDRESS = os.getenv('NLX_ADDRESS', 'localhost:8000')
    NLX_ORGANIZATION = os.getenv('NLX_ORGANIZATION', 'vng-realisatie')
    NLX_OUTWAY_ADDRESS = os.getenv('NLX_OUTWAY_ADDRESS', 'http://localhost:2018')

.. note::
    In the example, we pull them from the environment, but you can of course
    follow your own preferred method.


.. |build-status| image:: https://travis-ci.org/maykinmedia/nlx_middleware.svg?branch=develop
    :target: https://travis-ci.org/maykinmedia/nlx_middleware

.. |requirements| image:: https://requires.io/github/maykinmedia/nlx_middleware/requirements.svg?branch=develop
    :target: https://requires.io/github/maykinmedia/nlx_middleware/requirements/?branch=develop
    :alt: Requirements status

.. |coverage| image:: https://codecov.io/gh/maykinmedia/nlx_middleware/branch/develop/graph/badge.svg
    :target: https://codecov.io/gh/maykinmedia/nlx_middleware
    :alt: Coverage status

.. |python-versions| image:: https://img.shields.io/pypi/pyversions/nlx_middleware.svg

.. |django-versions| image:: https://img.shields.io/pypi/djversions/nlx_middleware.svg

.. |pypi-version| image:: https://img.shields.io/pypi/v/nlx_middleware.svg
    :target: https://pypi.org/project/nlx_middleware/


.. _NLx: https://nlx.io
