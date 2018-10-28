#include "Python.h"

int jam_set_subscript(PyObject *o, PyObject *key, PyObject *value);
int jam_set_attro(PyObject *o, PyObject *name, PyObject *value);
int jam_set_item(PyObject *o, Py_ssize_t i, PyObject *value);
int jam_set_attr(PyObject *o, char *name, PyObject *value);
void hijack_assignment_calls(PyTypeObject* type);
void unhijack_assignment_calls(PyTypeObject* type);
void unhijack_everything();
PyTypeObject* hijacked_dict();