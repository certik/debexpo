.. _config-file:

===========
Config file
===========

``debexpo.upload.incoming``
===========================

This variable specifies the incoming directory. Newly uploaded files will be installed into this directory.
Therefore, it should be writeable by the webserver.

No default value -- this variable **must** be specified.

``debexpo.repository``
======================

This variable specifies the repository directory, where uploaded files are stored. The directory structure is easy -- files belonging to a package are stored in a subdirectory of this directory, with name of the source package name.
For example, If this is set to ``/home/myexpo/files`` then the package 'cream' would have its files stored in ``/home/myexpo/files/cream/``.
The directory does not have a Sources.gz file (no "apt-get source") but source packages can be downloaded via "dget ...dsc".

No default value -- this variable **must** be specified.

``debexpo.importer``
====================

This variable specifies the path to the importer script, distributed in ``bin/importer.py``. Therefore, this option is typically ``%(here)s/bin/importer.py``.

No default value -- this variable **must** be specified.

``debexpo.handle_debian``
=========================

This variable specifies whether debexpo should handle the ``/debian/`` directory. This can be set to false and let Apache handle this directory.

The possible values for this variable are ``true`` or ``false``. It defaults to ``true``.
