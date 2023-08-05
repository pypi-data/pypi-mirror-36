utmp/wtmp/btmp reader module for Python 3.x
===========================================

This project is a binary Python 3.x module using POSIX-compliant and/or
system-specific headers for reading utmp/wtmp/btmp entries. It aims at
being compatible with multiple UNIX-like systems.

The format of these files have been standardized as ``utmpx``, ``wtmpx`` and
``btmpx`` in the `Single Unix Specification`_, although their location
depends on the system. The systems/paths correspondances are not hardcoded
in order to be able to interface with this module by reproducing one of
the known behaviours without having to fork and add an entry to the code.

Prerequisites
-------------

You need the Python 3.x development files and a POSIX-compliant system.

Building and installing
-----------------------

`distutils`_ makes most of the job, but you know, I couldn't not make a
Makefile above it for people like me who regret those days you could just
``make`` and ``sudo make install`` on any project. So here, this is possible.

.. _Single Unix Specification:: http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/utmpx.h.html
.. _distutils:: https://docs.python.org/3/distutils/introduction.html
