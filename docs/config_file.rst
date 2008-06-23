.. _config-file:

===========
Config file
===========

These are configuration options that go in the ini file that configures debexpo. Every option should be present otherwise debexpo will fail somewhere. A sane default is in the distributed ini file.

``debexpo.upload.incoming``
===========================

This variable specifies the incoming directory. Newly uploaded files will be installed into this directory.
Therefore, it should be writeable by the webserver.

``debexpo.repository``
======================

This variable specifies the repository directory, where uploaded files are stored. The directory structure is easy -- files belonging to a package are stored in a subdirectory of this directory, with name of the source package name.
For example, If this is set to ``/home/myexpo/files`` then the package 'cream' would have its files stored in ``/home/myexpo/files/cream/``.
The directory does not have a Sources.gz file (no "apt-get source") but source packages can be downloaded via "dget ...dsc".

``debexpo.importer``
====================

This variable specifies the path to the importer script, distributed in ``bin/importer.py``. Therefore, this option is typically ``%(here)s/bin/importer.py``.

``debexpo.handle_debian``
=========================

This variable specifies whether debexpo should handle the ``/debian/`` directory. This can be set to false and let Apache handle this directory.

``debexpo.sitename``
====================

Name of the site repository. This is used as the title of the web pages.

``debexpo.tagline``
===================

Tag-line of the repository. This is used under the main title of the web pages.

``debexpo.logo``
================

Site logo of the repository to display at the top of the web pages.

``debexpo.email``
=================

Email address of site support.

``debexpo.debian_specific``
===========================

Toggle whether to show Debian-specific contents of the site. Values are ``true`` or ``false``.
