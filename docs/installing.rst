.. _installing:

=================================
Installing and setting up debexpo
=================================

debexpo is easy to set up on your own. Simply follow the instructions below.

Install prerequisites
---------------------

You need to install the required packages. Using apt, you should execute::

    sudo apt-get install python-setuptools python-apt python-sphinx python-pylons python-debian python-sqlalchemy python-soappy lintian dpkg-dev python-nose python-pybabel

`lintian` and `dpkg-dev` are optional if you do not want to run any plugins,
and `python-nose` is optional if you don't want to run the test suite.

Getting debexpo
---------------

You can either download a release tarball, or clone from the Git repository.

`The debexpo website <http://debexpo.workaround.org/>`_ will contain details
about releases.

You can clone the repository contents by executing::

    git clone git://debexpo.workaround.org/debexpo.git

Building debexpo
----------------

Simply enter into the debexpo directory and execute ``python setup.py build``::

    cd debexpo
    make build

Installing debexpo
------------------

It is easier in some situations to leave debexpo in its source directory and
run it from there. However, if you wish to have it installed, follow these
instructions:

From the debexpo root directory, execute::

    sudo make install

This will install debexpo into your ``/usr/lib/pythonX.Y/site-packages/``
directory, ready for use.

Editing your configuration
---------------------------

Next you should edit the default configuration file. This file will be called
``debexpo.ini``. You should only have to look at options with the ``DEBEXPO``
comment preceeding them. You can find explanations of the `debexpo.*` options
on the :ref:`config-file` page.

Running debexpo
---------------

Using paste's built-in webserver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Simply execute::

    paster serve debexpo.ini

and visit http://localhost:5000/ in your web browser.

Using Apache
^^^^^^^^^^^^

(Canonical instructions for getting Pylons apps working under Apache are
`here <http://wiki.pylonshq.com/display/pylonsdocs/Running+Pylons+apps+with+Webservers>`_.)

#. Install apache2, mod-fastcgi and flup::

    sudo apt-get install python-flup apache2 libapache2-mod-fastcgi

#. Edit the ``server:main`` section of your `debexpo.ini` so it reads
   something like this::

    [server:main]
    use = egg:PasteScript#flup_fcgi_thread
    host = 0.0.0.0
    port = 6500
 
#. Add the following to your config::

    <IfModule mod_fastcgi.c>
      FastCgiIpcDir /tmp
      FastCgiExternalServer /some/path/to/debexpo.fcgi -host localhost:6500
    </IfModule>

  Note: Parts of this may conflict with your `/etc/apache2/conf-available/fastcgi.conf`.

  `/some/path/to/debexpo/fcgi` need not physically exist on the webserver.

#. Start the server::

    paster serve debexpo.ini

#. Reload apache and visit http://localhost/.
