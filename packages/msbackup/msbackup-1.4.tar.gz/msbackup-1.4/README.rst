MSBackup utility
================

The *msbackup* utility performs data archiving.
The main use for this is the daily execution of the utility by system scheduler
(*cron* for example).

Usage
-----

For reliable archiving of various data have the appropriate backend:

* **file** - archive folder by the *tar* with compression format *bzip2*.

* **subversion** - scans the folder repositories of version control system
  `Apache Subversion
  <http://subversion.apache.org/>`_ and archives each
  repository by the *tar* with compression format *bzip2* on dump of *hot copy*
  of each repository.

* **mercurial** - scans the folder repositories of version control system
  `Mercurial
  <http://www.mercurial-scm.org/>`_ and executes the command *tar*
  with compression format *bzip2* on clone of each repository.

When you start utility with the *--rotated* parameter, from the backup folder
will deleted all expired archives on the basis of configuration.

Archive files can be encrypted with the *--encryptor gpg* parameter.

Testing
-------

Dependencies of this project can be installed by the command::

   $ pip install -U -e .[dev]

Tests can be launched by the command::

   $ python -m unittest discover -s src/test

Test reports and coverage report can be generate using::

   $ ./test.sh

After the successful execution of the script folder *test-reports* will contain
a report (in **XML** format) of the tests, and in the folder *coverage* will be
a report (in **HTML** format) of the code coverage.
