============
Mamba-Client
============


.. image:: https://api.travis-ci.org/mamba-framework/mamba-client.svg?branch=master
   :target: https://travis-ci.org/github/mamba-framework/mamba-client/builds
.. image:: https://img.shields.io/codecov/c/github/mamba-framework/mamba-client/master.svg
   :target: https://codecov.io/github/mamba-framework/mamba-client?branch=master
   :alt: Coverage report
.. image:: https://img.shields.io/pypi/v/Mamba-Client.svg
        :target: https://pypi.python.org/pypi/Mamba-Client
.. image:: https://img.shields.io/readthedocs/mamba-client.svg
        :target: https://readthedocs.org/projects/mamba-client/builds/
        :alt: Documentation Status
.. image:: https://img.shields.io/badge/license-%20MIT-blue.svg
   :target: ../master/LICENSE

Mamba Framework Overview
========================

Mamba is a framework for data acquisition in distributed test environments. The Mamba Framework is composed of:
  
- **Mamba Server**: A tool to develop the controllers for the different Ground Control Equipments (https://github.com/mamba-framework/mamba-server).
- **Mamba Client**: A set of libraries for composing a central controller that can use the services provided from one or more Mamba Servers. The central controller can be writen in a Jupyter Notebook, in a traditional development environment (like Visual Code or PyCharm) or be executed as an stand-alone script.
- **Mamba Utils**: A set of utilities that are useful in the development of Ground Testbeds, like UDP and TCP sniffers (https://github.com/mamba-framework/mamba-utils).

The next image shows an architectural example of a testbed implemented with the Mamba Framework:

.. image:: docs/utils/mamba_framework_architecture.jpg
   :height: 18px

Where each Mamba Server can run in the same or different computers and be located in the same building or in different countries.

Overview
===========
Client libraries for Mamba Server

Requirements
============

* Python 3.6+
* Works on Linux, Windows, macOS, BSD

Install
=======

The quick way::

    pip install mamba-client
