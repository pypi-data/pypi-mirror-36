/* ****************************************************************************
 * main.c -- pyutmpx module definition.
 * Copyright (C) 2017-2018 Thomas "Cakeisalie5" Touhey <thomas@touhey.fr>
 *
 * This file is part of the pyutmpx Python 3.x module, which is MIT-licensed.
 * ************************************************************************* */

#include "pyutmpx.h"
#include <datetime.h>

/* ---
 * Datetime utilities.
 * --- */

/* Utility to get a datetime from a timeval. */

PyObject *pyutmpx_get_datetime(const struct timeval *tv)
{
	PyObject *result = NULL;
	PyObject *epoch = NULL, *date_delta = NULL;

	epoch = PyDateTime_FromDateAndTime(1970, 1, 1, 0, 0, 0, 0);
	date_delta = PyDelta_FromDSU(0, tv->tv_sec, tv->tv_usec);
	if (!epoch || !date_delta)
		goto fail;

	result = PyNumber_Add(epoch, date_delta);

fail:
	Py_XDECREF(epoch);
	Py_XDECREF(date_delta);

	return (result);
}

/* ---
 * Module definitions.
 * --- */

/* Module deinitialization.
 * We ought to deinitialize objects that the user can't see. */

static void pyutmpx_del(void *module)
{
	(void)module;

	pyutmpx_destroy_iterators();
	Py_XDECREF(&pyutmpx_entry);
}

/* Module methods. */

static PyMethodDef module_methods[] = {
	{NULL, NULL, 0, NULL}
};

/* Module definition. */

static struct PyModuleDef module = {
	PyModuleDef_HEAD_INIT,

	/* .m_name = */ "pyutmpx",
	/* .m_doc = */ "This module provides a utmp reader.",
	/* .m_size = */ -1,
	/* .m_methods = */ module_methods,
	/* .m_slots = */ NULL,
	/* .m_traverse = */ NULL,
	/* .m_clear = */ NULL,
	/* .m_free = */ &pyutmpx_del
};

/* Module initialization. */

PyMODINIT_FUNC PyInit_pyutmpx(void)
{
	PyObject *m;
	int p_iter = 0;
	int p_types = 0;
	int p_ent = 0;

	/* Import the datetime module. */

	PyDateTime_IMPORT;

	/* Initialize the module. */

	m = PyModule_Create(&module);
	if (!m)
		goto fail;

	/* Version. */

	if (PyModule_AddStringConstant(m, "version", PYUTMPX_VERSION) < 0)
		goto fail;

	/* Prepare the iterators. */

	if (pyutmpx_prepare_iterators(m))
		goto fail;
	p_iter = 1;

	/* Make the constants and add them to the module. */

	if (pyutmpx_prepare_types(m))
		goto fail;
	p_types = 1;

	/* Create the utmp entry type to the module. */

	if (PyType_Ready(&pyutmpx_entry) < 0)
		goto fail;
	Py_INCREF((PyObject *)&pyutmpx_entry);
	p_ent = 1;

	/* Everything went well in the end :) */

	return (m);
fail:
	if (p_ent)
		Py_DECREF(&pyutmpx_entry);
	if (p_types)
		pyutmpx_destroy_types();
	if (p_iter)
		pyutmpx_destroy_iterators();
	Py_XDECREF(m);
	return (NULL);
}
