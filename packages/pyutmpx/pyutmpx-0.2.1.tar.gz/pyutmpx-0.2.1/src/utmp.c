/* ****************************************************************************
 * utmp.c -- utmpx file iterator definition.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <errno.h>

/* ---
 * Compatibility.
 * --- */

/* Here, we want to decide which interface we want to use.
 * There are several we can use with various degrees of confidence:
 *
 * - the <utmpx.h> interface standardized in POSIX.1, which only allows us
 *   to interact with the utmp file and not the wtmp and btmp ones.
 * - the GNU <utmp.h> interface, which allows us to interact with wtmp
 *   and btmp as well, but with a global cursor.
 * - opening the files and interacting with them directly. This requires us
 *   to know exactly where the files are and what the structures are, plus
 *   some systems maintain a modern file set named after the standard and
 *   an older one for compatibility with older software.
 * - the utmpd interface, which is very similar to the standard.
 *
 * Here, for now, we only interact with the utmpx files using the standard
 * interface. */

#include <utmpx.h>
#define HAS_WTMP 0
#define HAS_BTMP 0

/* The affected functions are `pyutmpx_reset_utmp()` and `pyutmpx_next_utmp()`,
 * although the `HAS_WTMP` and `HAS_BTMP` are used in the
 * `pyutmpx_prepare_iterators()` to know if the `wtmp` and `btmp` objects
 * shall be opened. */

/* ---
 * Constructor, destructor.
 * --- */

/* `pyutmpx_utmp_t`: object structure.
 *
 * As this module uses the POSIX interface to utmp, using a global cursor,
 * this structure does not require any auxiliary data for now.
 * More data will be required if the module allows more interactions with
 * its environment, such as direct utmp/wtmp/btmp file reading, or
 * interaction with a utmp-managing daemon such as utmps. */

typedef struct {
	PyObject_HEAD
} pyutmpx_utmp_t;

/* `pyutmpx_create_utmp()`: create the Python object.
 * It does not initialize the connexion to the file,
 * see `pyutmpx_init_utmp()`. */

static PyObject *pyutmpx_create_utmp(PyTypeObject *type, PyObject *args,
	PyObject *kw)
{
	pyutmpx_utmp_t *self;

	self = (pyutmpx_utmp_t *)type->tp_alloc(type, 0);
	return ((PyObject *)self);
}

/* `pyutmpx_init_utmp()`: initialize the Python object.
 * Looks for the file, check if it has the rights to open it, and stuff. */

static int pyutmpx_init_utmp(pyutmpx_utmp_t *self, PyObject *args,
	PyObject *kw)
{
	if (!PyArg_ParseTuple(args, ""))
		return (-1);

	/* Reset the thing and return. */

	setutxent();
	return (0);
}

/* `pyutmpx_exit_utmp()`: destroy the Python object.
 * Deinitializes everything it can. */

static void pyutmpx_exit_utmp(pyutmpx_utmp_t *self)
{
	/* If `self` exists, free it. */

	if (!self)
		return ;
	Py_TYPE(self)->tp_free((PyObject *)self);
}

/* ---
 * Iterator-related methods.
 * --- */

/* `pyutmpx_reset_utmp()`: reset the cursor. */

static PyObject *pyutmpx_reset_utmp(pyutmpx_utmp_t *self,
	PyObject *Py_UNUSED(args))
{
	setutxent();

	Py_RETURN_NONE;
}

/* `pyutmpx_iter_utmp()`: return self because we are iterable. */

static PyObject *pyutmpx_iter_utmp(pyutmpx_utmp_t *self)
{
	if (!pyutmpx_reset_utmp(self, NULL))
		return (NULL);

	Py_INCREF(self);
	return ((PyObject *)self);
}

/* `pyutmpx_next_utmp()`: return next element in self. */

static PyObject *pyutmpx_next_utmp(pyutmpx_utmp_t *self)
{
	PyObject *type = NULL, *date = NULL;
	PyObject *arglist = NULL, *entry = NULL;
	struct utmpx *ent;
	int failed = 1;

	/* Get the entry and iterate using the POSIX utmpx interface. */

	do {
		ent = getutxent();
		if (!ent) {
			PyErr_SetNone(PyExc_StopIteration);
			return (NULL);
		}
	} while (!(type = pyutmpx_get_type(ent->ut_type)));

	/* Get the date. */

	date = pyutmpx_get_datetime((const struct timeval*)&ent->ut_tv);
	if (!date)
		goto fail;

	/* Create the argument list and call the object to create it. */

	arglist = Py_BuildValue("sOssOk", ent->ut_id, type, ent->ut_user,
		ent->ut_line, date, ent->ut_pid);
	if (!arglist)
		goto fail;

	entry = PyObject_CallObject((PyObject*)&pyutmpx_entry, arglist);
	if (!entry)
		goto fail;

	/* End. */

	Py_INCREF(entry);
	failed = 0;
fail:
	Py_XDECREF(arglist);

	/* Even in the case where everything went okay, the object will have
	 * incremented the reference count to these objects, so this should
	 * be okay. */

	Py_XDECREF(type);
	Py_XDECREF(date);
	Py_XDECREF(entry);

	/* Go, go, go! */

	if (failed)
		PyErr_SetString(PyExc_Exception, "");
	return (entry);
}

/* `pyutmpx_get_path()`: getter to the `path` property. */

PyObject *pyutmpx_get_path(PyObject *self, void *cookie)
{
	(void)cookie;

	PyErr_SetString(PyExc_NotImplementedError, "");
	return (NULL);
}

/* ---
 * Representation.
 * --- */

/* `pyutmpx_repr_utmp()`: represent the Python object.
 * This is useful for debugging. */

static PyObject *pyutmpx_repr_utmp(pyutmpx_utmp_t *self)
{
	return (Py_BuildValue("s", "pyutmpx.utmp"));
}

/* ---
 * Classes definitions.
 * --- */

static PyMethodDef pyutmpx_utmp_methods[] = {
	{"reset", (PyCFunction)pyutmpx_reset_utmp, METH_NOARGS,
		"Resets the cursor."},
	{"next", (PyCFunction)pyutmpx_next_utmp, METH_NOARGS,
		"Gets the next entry."},
	{NULL, NULL, 0, NULL}
};

static PyGetSetDef pyutmpx_utmp_getset[] = {
	{"path", (getter)&pyutmpx_get_path, NULL,
		"Path to the raw file, if present.", NULL},
	{NULL, NULL, NULL, NULL, NULL}
};

PyTypeObject pyutmpx_utmp = {
	PyVarObject_HEAD_INIT(NULL, 0)

	/* Basic information. */

	.tp_name = "pyutmpx.utmp",
	.tp_doc = "utmp entries iterator",
	.tp_basicsize = sizeof(pyutmpx_utmp_t),
	.tp_flags = Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE,

	/* Callbacks. */

	.tp_new = pyutmpx_create_utmp,
	.tp_init = (initproc)pyutmpx_init_utmp,
	.tp_dealloc = (destructor)pyutmpx_exit_utmp,
	.tp_iter = (getiterfunc)pyutmpx_iter_utmp,
	.tp_iternext = (iternextfunc)pyutmpx_next_utmp,
	.tp_repr = (reprfunc)pyutmpx_repr_utmp,

	/* Members. */

	.tp_methods = pyutmpx_utmp_methods,
	.tp_getset = pyutmpx_utmp_getset
};

/* ---
 * Prepare the types.
 * --- */

/* `pyutmpx_prepare_iterators()`: prepare the iterators' types and
 * instances, and add them to the module. */

int pyutmpx_prepare_iterators(PyObject *m)
{
	int p_utmp = 0;
	PyObject *utmp;
#if HAS_WTMP
	int p_wtmp = 0;
	PyObject *wtmp;
#endif
#if HAS_BTMP
	int p_btmp = 0;
	PyObject *btmp;
#endif

	/* Create the utmp iterator type. */

	if (PyType_Ready(&pyutmpx_utmp) < 0)
		goto fail;
	Py_INCREF(&pyutmpx_utmp);
	p_utmp = 1;

	/* Create an instance of the utmp iterator type and add it
	 * to the module. */

	utmp = PyObject_CallObject((PyObject *)&pyutmpx_utmp, NULL);
	if (!utmp || PyModule_AddObject(m, "utmp", utmp) < 0)
		goto fail;

#if HAS_WTMP
	/* TODO */
#endif

#if HAS_BTMP
	/* TODO */
#endif

	return (0);
fail:
	if (p_utmp)
		Py_DECREF(&pyutmpx_utmp);
#if HAS_WTMP
	if (p_wtmp)
		Py_DECREF(&pyutmpx_wtmp);
#endif
#if HAS_BTMP
	if (p_btmp)
		Py_DECREF(&pyutmpx_btmp);
#endif

	return (-1);
}

/* `pyutmpx_destroy_iterators()`: deinitialize iterators' types and
 * instances. */

void pyutmpx_destroy_iterators(void)
{
	Py_DECREF(&pyutmpx_utmp);
#if HAS_WTMP
	Py_DECREF(&pyutmpx_wtmp);
#endif
#if HAS_BTMP
	Py_DECREF(&pyutmpx_btmp);
#endif
}
