kotti_group_manager
************************

This is an extension to Kotti that helps admin users to manage groups and users.

Features
=================

- Allow groups and group pages to be created from email domains of new users if
  enabled.
 
.. image:: https://preview.ibb.co/frhUUz/Welcome_to_Kotti_Kotti_1.gif

|pypi|_
|downloads_month|_
|license|_
|build_status_stable|_

.. |pypi| image:: https://img.shields.io/pypi/v/kotti_group_manager.svg?style=flat-square
.. _pypi: https://pypi.python.org/pypi/kotti_group_manager/

.. |downloads_month| image:: https://img.shields.io/pypi/dm/kotti_group_manager.svg?style=flat-square
.. _downloads_month: https://pypi.python.org/pypi/kotti_group_manager/

.. |license| image:: https://img.shields.io/pypi/l/kotti_group_manager.svg?style=flat-square
.. _license: http://www.repoze.org/LICENSE.txt

.. |build_status_stable| image:: https://img.shields.io/travis/Collective-Kotti/kotti_group_manager/production.svg?style=flat-square
.. _build_status_stable: http://travis-ci.org/Collective-Kotti/kotti_group_manager

`Find out more about Kotti`_

Development happens at https://github.com/Collective-Kotti/kotti_group_manager

.. _Find out more about Kotti: http://pypi.python.org/pypi/Kotti

Setup
=====

To enable the extension in your Kotti site, activate the configurator::

    kotti.configurators =
        kotti_group_manager.kotti_configure

Database upgrade
================

If you are upgrading from a previous version you might have to migrate your
database.  The migration is performed with `alembic`_ and Kotti's console script
``kotti-migrate``. To migrate, run
``kotti-migrate upgrade --scripts=kotti_group_manager:alembic``.

For integration of alembic in your environment please refer to the
`alembic documentation`_. If you have problems with the upgrade,
please create a new issue in the `tracker`_.

Development
===========

|build_status_master|_

.. |build_status_master| image:: https://img.shields.io/travis/Collective-Kotti/kotti_group_manager/master.svg?style=flat-square
.. _build_status_master: http://travis-ci.org/Collective-Kotti/kotti_group_manager

Contributions to kotti_group_manager are highly welcome.
Just clone its `Github repository`_ and submit your contributions as pull requests.

.. _alembic: http://pypi.python.org/pypi/alembic
.. _alembic documentation: http://alembic.readthedocs.org/en/latest/index.html
.. _tracker: https://github.com/Collective-Kotti/kotti_group_manager/issues
.. _Github repository: https://github.com/Collective-Kotti/kotti_group_manager
