========================
debexpo coding standards
========================

Parts of this document are copied from `netconf's coding standards`__.

__ http://git.debian.org/?p=netconf/netconf.git;a=blob;f=doc/coding_standards.txt;hb=HEAD

Python
======

debexpo Python code adheres to `PEP-8 coding guidelines`__.


__ http://www.python.org/dev/peps/pep-0008/

debexpo is written for Python 2.5; thus, all features up until and including
Python 2.5 may be used.

If the choice is between a Python 2.5 way of implementing something, and
a pre-2.5 way, the former should be taken.

Existing pre-2.5 constructs which have been deprecated by Python 2.5 must be
reimplemented accordingly.

Existing pre-2.5 constructs which can merely be expressed more concisely with
Python 2.5 can be migrated, and probably should be.
