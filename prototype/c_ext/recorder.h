#include "Python.h"
#include "frameobject.h"

void process_execution_step(int what, PyFrameObject *frame, PyObject *arg);
PyObject* get_recording(long n);
PyObject* get_execution_lines();
PyObject* get_variable_names();
void stop_recording();
void reset_recorder();
void reset_recording();
bool is_locals_dict(PyObject* obj);
void save_assignment(PyObject *o, PyObject* k, PyObject* v, int kind);
void save_object(PyObject* obj);