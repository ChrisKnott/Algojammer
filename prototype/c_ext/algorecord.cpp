#include <Python.h>
#include "frameobject.h"
#include "recorder.h"
#include <iostream>
#include <chrono>

using Clock = std::chrono::high_resolution_clock;

#define PYPRINT(obj) PyObject_Print(obj, stdout, 0);

PyObject* algojammer_str = PyUnicode_FromString("algojammer");
PyObject* callback;
auto last_callback_time = Clock::now();
int steps_since_callback = 0;

void do_callback();

static int trace(PyObject *obj, PyFrameObject *frame, int what, PyObject *arg){
    switch(what) {
        case PyTrace_CALL:
        case PyTrace_EXCEPTION:
        case PyTrace_LINE:
        case PyTrace_RETURN:
        PyObject *filename = frame->f_code->co_filename;
        bool in_my_code = PyObject_RichCompareBool(filename, algojammer_str, Py_EQ);
        if(in_my_code){
            process_execution_step(what, frame, arg);
            --steps_since_callback;
        }
    }

    auto elapsed = Clock::now() - last_callback_time;
    auto ms = std::chrono::duration_cast<std::chrono::milliseconds>(elapsed).count();
    if(ms > 50 || steps_since_callback < 0){
        // Callback every 0.05s or 25,000 steps (whichever is sooner)
        do_callback();
        last_callback_time = Clock::now();
        steps_since_callback = 25000;
    }

    return 0;
}

void do_callback(){
    if(PyErr_Occurred() == NULL){
        if(PyCallable_Check(callback)){
            auto arglist = Py_BuildValue("(O)", get_execution_lines());
            PyEval_CallObject(callback, arglist);
        }
    }
}

static PyObject* get_milestone(PyObject *self, PyObject *args){
    long step = PyLong_AsLong(PyTuple_GET_ITEM(args, 0));
    return get_recording(step);
}

static PyObject* get_all_variables(PyObject *self, PyObject *args){
    return get_variable_names();
}

static PyObject* start_trace(PyObject *self, PyObject *args){
    PyObject* new_callback = PyTuple_GET_ITEM(args, 0);
    Py_XDECREF(callback);
    Py_XINCREF(new_callback);
    callback = new_callback;

    PyEval_SetTrace((Py_tracefunc) trace, NULL);
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* clear_recordings(PyObject *self, PyObject *args){
    reset_recorder();
    Py_INCREF(Py_None);
    return Py_None;
}

static PyObject* stop_trace(PyObject *self, PyObject *args){
    PyEval_SetTrace(NULL, NULL);
    do_callback();
    PyErr_Clear();
    Py_INCREF(Py_None);
    return Py_None;
}

static PyMethodDef
methods[] = {
    {"get_milestone", (PyCFunction) get_milestone, METH_VARARGS, PyDoc_STR("")},
    {"start_trace", (PyCFunction) start_trace, METH_VARARGS, PyDoc_STR("")},
    {"stop_trace", (PyCFunction) stop_trace, METH_VARARGS, PyDoc_STR("")},
    {"clear_recordings", (PyCFunction) clear_recordings, METH_VARARGS, PyDoc_STR("")},
    {"get_all_variables", (PyCFunction) get_all_variables, METH_VARARGS, PyDoc_STR("")},
    {NULL}
};

static struct PyModuleDef moduledef = {
    PyModuleDef_HEAD_INIT,
    "algorecord", NULL, -1, methods,
    NULL, NULL, NULL, NULL,
};

extern "C"
PyObject *PyInit_algorecord(void) {
    return PyModule_Create(&moduledef);
}


