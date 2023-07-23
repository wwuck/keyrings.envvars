keyrings.envvars
================

|PyPI| |Status| |Python Version| |License|

|CI| |Codecov|

|pre-commit| |Black|

.. |PyPI| image:: https://img.shields.io/pypi/v/keyrings.envvars.svg
   :target: https://pypi.org/project/keyrings.envvars/
   :alt: PyPI
.. |Status| image:: https://img.shields.io/pypi/status/keyrings.envvars.svg
   :target: https://pypi.org/project/keyrings.envvars/
   :alt: Status
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/keyrings.envvars
   :target: https://pypi.org/project/keyrings.envvars
   :alt: Python Version
.. |License| image:: https://img.shields.io/pypi/l/keyrings.envvars
   :target: https://opensource.org/licenses/MIT
   :alt: License
.. |CI| image:: https://github.com/wwuck/keyrings.envvars/workflows/CI/badge.svg
   :target: https://github.com/wwuck/keyrings.envvars/actions?workflow=CI
   :alt: CI
.. |Codecov| image:: https://codecov.io/gh/wwuck/keyrings.envvars/branch/main/graph/badge.svg
   :target: https://codecov.io/gh/wwuck/keyrings.envvars
   :alt: Codecov
.. |pre-commit| image:: https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white
   :target: https://github.com/pre-commit/pre-commit
   :alt: pre-commit
.. |Black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black


*keyrings.envvars* is a keyring backend plugin for the keyring_ utility that provides credentials via environment variables.


Requirements
------------

* keyring >= 23.4.0
* Python >= 3.9


Installation
------------

You can install *keyrings.envvars* via pip_ from PyPI_:

.. code:: console

   $ pip install keyrings.envvars


Usage
-----

*keyrings.envvars* uses the following format for environment variables:

.. code:: console

   KEYRING_SERVICE_NAME_<n>=<service>
   KEYRING_SERVICE_USERNAME_<n>=<username>
   KEYRING_SERVICE_PASSWORD_<n>=<password>

Example for usage with pip credentials:

.. code:: console

   KEYRING_SERVICE_NAME_0=https://private-pypi-index.example.com
   KEYRING_SERVICE_USERNAME_0=testusername
   KEYRING_SERVICE_PASSWORD_0=testpassword
   KEYRING_SERVICE_NAME_1=https://another-private-pypi-index.example.com
   KEYRING_SERVICE_USERNAME_1=testusername
   KEYRING_SERVICE_PASSWORD_1=testpassword

Note: Defining multiple identical credentials (service name and username)
will result in the last defined password being returned as the environment
variables are sorted by the keyring backend.

.. code:: console

   export KEYRING_SERVICE_NAME_0=https://private-pypi-index.example.com
   export KEYRING_SERVICE_USERNAME_0=testusername
   export KEYRING_SERVICE_PASSWORD_0=testpassword
   export KEYRING_SERVICE_NAME_1=https://private-pypi-index.example.com
   export KEYRING_SERVICE_USERNAME_1=testusername
   export KEYRING_SERVICE_PASSWORD_1=testpassword_1
   keyring get https://private-pypi-index.example.com testusername
   testpassword_1

Contributing
------------

Contributions including suggestions, pull requests, etc. are very welcome.
*keyrings.envvars* uses `Conventional Commits`_ format for commit messages.


License
-------

Distributed under the terms of the `MIT license`_,
*keyrings.envvars* is free and open source software.


Issues
------

If you encounter any problems,
please `file an issue`_ along with a detailed description.

Please read https://www.chiark.greenend.org.uk/~sgtatham/bugs.html before you file an issue.


Credits
-------

This project was generated from `@cjolowicz`_'s `Hypermodern Python Cookiecutter`_ template.

.. _@cjolowicz: https://github.com/cjolowicz
.. _MIT license: https://opensource.org/licenses/MIT
.. _PyPI: https://pypi.org/
.. _Hypermodern Python Cookiecutter: https://github.com/cjolowicz/cookiecutter-hypermodern-python
.. _file an issue: https://github.com/wwuck/keyrings.envvars/issues
.. _pip: https://pip.pypa.io/
.. _keyring: https://pypi.org/project/keyring/
.. _Conventional Commits: https://www.conventionalcommits.org/
