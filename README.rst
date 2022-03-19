README
******

.. image:: https://github.com/aiops/logsight-cli-py/actions/workflows/build.yml/badge.svg
    :target: https://github.com/aiops/logsight-cli-py/actions/workflows/build.yml
    :alt: Build

.. image:: https://img.shields.io/pypi/v/logsight-cli-py
    :target: https://pypi.python.org/pypi/logsight-cli-py/
    :alt: Package version

.. image:: https://img.shields.io/pypi/pyversions/logsight-cli-py.svg
    :target: https://pypi.org/project/pytest/

.. image:: https://readthedocs.org/projects/logsight-cli-py/badge/?version=latest
    :target: https://logsight-cli-py.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/dw/logsight-cli-py.svg
    :target: https://pypi.org/project/logsight-cli-py/
    :alt: Weekly PyPI downloads

..  image:: https://img.shields.io/twitter/follow/logsight.svg?label=logsight&style=flat&logo=twitter&logoColor=4FADFF
    :target: https://twitter.com/logsight
    :alt: logsight.ai on Twitter


Scope
-----

How To Make Quality Gates in CI/CD with GitHub
    + https://cerberus-testing.medium.com/how-to-make-quality-gates-in-ci-cd-with-github-a373d8a443b8


Logsight Command Line Interface
-------------------------------

The Logsight Command Line Interface (CLI) is a unified tool to manage your logs.
With this tool, you can manage your logs, applications, tags and execute analytics over logs such as verification.

Commands available include:

+ Applications
    + Create and delete applications
+ Users
    + Register, activate and delete users (not yet available)
    + Change and reset password (not yet available)
+ Analytics
    + Compare logs
    + Detect incidents in logs


Installation
------------

Prerequisite
============
You have a `Logsight.ai`__ account with `EMAIL` and `PASSWORD`.

.. __: https://logsight.ai/


Install package
===============

The CLI can can installed using pip from PyPI.
It has been tested with Mac and Linux operating systems.

.. code-block:: console

    $ pip install logsight-cli-py


To verify your CLI installation, use the logsight --version command:

.. code-block:: console

    $ logsight --version
    logsight/0.0.6

The output looks like logsight/x.y.z.
If you don't see that output, and installed the Logsight CLI, check if you have an old logsight package on your system.
Uninstall it with these instructions `uninstallation`_.



Configuring Logsight CLI
========================
There are several methods you can use to configure the settings that the Logsight CLI uses when interacting with Logsight.ai service,
i.e. Logsight URL and account API keys. Account API keys can be created in API.

There is a specific load order for what will be used.

Using Logsight Config
======================
You can create a `.logsight` config file to set up your configuration with Logsight server.
The file should be placed in your home directory.

.. code-block:: console

    $ cat ~/.logsight
    [DEFAULT]
    EMAIL = john.miller@zmail.com
    PASSWORD = sawhUz-hanpe4-zaqtyr
    APP_ID = 07402355-e74e-4115-b21d-4cbf453490d1

Setting the variable APP_ID is optional.
It can be set if you frequently use the same application and want to avoid passing the Id as a parameter for each command invoked.


Using Environment Variables
===========================
You can also set the variables using your environment, `LOGSIGHT_EMAIL`, `LOGSIGHT_PASSWORD` and `LOGSIGHT_APP_ID`.
Environment variables take precedence over config variables.

.. code-block:: console

    $ export LOGSIGHT_EMAIL=john.miller@zmail.com
    $ export LOGSIGHT_PASSWORD=sawhUz-hanpe4-zaqtyr
    $ export LOGSIGHT_APP_ID=07402355-e74e-4115-b21d-4cbf453490d1
    $ export LOGSIGHT_DEBUG=True

Alternatively, to set the required environment variables for the Logsight command-line client,
you can create an environment file called an Logsight rc file, or logsightrc.sh file.
A sample file is available at bin/logsightrc.sh.
You can update it and, afterwards, source it:

.. code-block:: console

    $ source bin/logsightrc.sh


Passing Options
===============
If you choose not to use the logsight config file or set environment variables,
you can pass the same values as options as part of any logsight command.

.. code-block:: console

    $ logsight --email john.miller@zmail.com --password sawhUz-hanpe4-zaqtyr applications ls


Examples
--------

Single Commands
===============
The following list provides examples of useful commands:

.. code-block:: console

    $ logsight config
    EMAIL: john.miller@zmail.com, PASSWD: sawhUz-hanpe4-zaqtyr, APP_ID: 07402355-e74e-4115-b21d-4cbf453490d1

    $ logsight application ls
    +--------------------------------------+------------------+
    |            APPLICATION Id            |       NAME       |
    +--------------------------------------+------------------+
    | 84c2ca94-e39c-498f-ad0d-0263434c71ac |    hdfs_node     |
    | 8b6cd73b-299b-4f2b-8334-3b820434a23a |   node_manager   |
    | 208d3b6d-15b7-402d-b53a-4c32c2eff623 | resource_manager |
    | 7a858f4f-33f7-4bba-ac5e-bd5fec0bd9a2 |    name_node     |
    +--------------------------------------+------------------+

    $ logsight application create --name <app name>
    $ logsight application delete --app_id <app id>

    $ logsight log upload <file> --tag v1 --app_id <app id>
    $ logsight log tag ls --app_id <app id>
    $ [Under development] logsight log status --flush_id --app_id <app id>

    $ logsight compare log --app_id <app id> --tags <tag v1> <tag v2> --flush_id <flush id>
    $ logsight incident log --app_id <app id> --tag <tag v1>
    $ [Under development] logsight quality log --app_id <app id> --tags <tag v1>


Comparing Logs
==============

.. code-block:: console

    $ logsight application create --name apache_srv2
    $ # copy the <app_id> returned to next command
    $ export LOGSIGHT_APP_ID=<app_id>
    $ logsight log upload hadoop_name_node_v1 --tag v1
    $ logsight log upload hadoop_name_node_v1 --tag v2
    $ # copy <flush_id> returned to next command
    $ logsight compare log --tags v1 v2 --flush_id <flush_id>



Uninstallation
--------------

Uninstall logsight package:

.. code-block:: console

    $ pip uninstall logsight


Availability
------------

The Logsight CLI Python package is deployed to the following external platforms:

+ Test Python Package Index (TestPyPI): `Test PyPI`_
+ Python Package Index (PyPI): PyPI_
+ Documentation: docs_

.. _logsight.ai: https://logsight.ai
.. _test pypi: https://test.pypi.org/search/?q=%22logsight-cli-py%22&o=
.. _pypi: https://pypi.org/search/?q=%22logsight-cli-py%22&o=
.. _docs: https://logsight-cli-py.readthedocs.io