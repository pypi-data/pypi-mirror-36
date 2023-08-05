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

Usage
-----

The module defines at least the ``utmp`` object, and at most it and two other
databases, which are ``wtmp`` and ``btmp``. The three objects behave the
same, so in the rest of the description, I'll only deal with ``utmp``.

``utmp`` is both an iterator and iterable, using itself as the iterator, which
allows you to use tools such as list comprehensions with it. You can also use
the ``.reset()`` and ``.next()`` methods with it.

Every return entry will be a ``utmp_entry``, which has the following
properties:

``type``
	The entry type, among the following:

		``BOOT_TIME``
			Time of system boot.

		``OLD_TIME``
			Time before system clock change.

		``NEW_TIME``
			Time after system clock change.

		``USER_PROCESS``
			Normal process.

		``INIT_PROCESS``
			Process spawned by init(8).

		``LOGIN_PROCESS``
			Session leader process for user login.

		``DEAD_PROCESS``
			Terminated process.

``id``
	The terminal name suffix, or inittab(5) ID (as a string).

``user``
	The username (as a string).

``line``
	The line on which the user is logged in, usually the device name of the
	tty minus the "/dev/" part (as a string).

``date``
	The date of the event (as a ``datetime.datetime`` instance).

``pid``
	The process identifier (as an integer).

What is left to do
------------------

- Implement other interfaces, standard and non-standard, as explained in
  the “Compatibility” section in ``utmp.c``.
- Add the ``wtmp`` and ``btmp`` objects.
- Add utmp filename getting and setting for these objects.
- Add a list-like interface, with length and index.
- Add methods to add an event, such as login or logout events.

.. _Single Unix Specification: http://pubs.opengroup.org/onlinepubs/9699919799/basedefs/utmpx.h.html
