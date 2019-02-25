#include "Python.h"
#include "hacks.h"
#include "recorder.h"
#include <vector>
#include <iostream>

/*
(If I was still a programmer I'd probably be ashamed of this...)
------------------------------------------------------------------------
We overwrite several function pointers so we can intercept and record any calls
which mutate state. Essentially we need to record when any of these things happen;
	obj = val
	obj.attr = val
	obj[key] = val

These correspond to the bytecode instructions STORE_NAME, STORE_ATTR and STORE_SUBSCR.

An unused pointer on PyObjectType (tp_cache) is used to store a pointer to an array
of the original methods, which we overwrite (the pointer is converted to a PyLong)

This implementation is *extremely brittle* and relies on arbitrary implementation details
of CPython. These could easily change in minor versions. I have no idea what versions
of Python this works on - possibly not many. There is also no efficient way to intercept
calls to STORE_GLOBAL using this method (as it directly calls PyDict_SetItem rather than
PyObject_SetItem)

Ultimately, this is not a long term solution, just temp hack that allows Algojammer to
ship as a small cross-platform library rather than a large binary. A long term solution 
would be to fork CPython (or Pypy) and manually add the relevant callbacks in the heart 
of the interpreter.
*/

PyTypeObject hijacked_dict_type;
PyTypeObject* hijacked_dict_addr;
std::vector<void**> method_ptrs;
std::vector<PyTypeObject*> hijacked_types;

void* hijacked_method(PyTypeObject* type, int m){
    void** methods = (void**)PyLong_AsVoidPtr(type->tp_cache);
    return methods[m];
}

// o[key] = value
int jam_set_subscript(PyObject *o, PyObject *key, PyObject *value) {
    if(PyErr_Occurred() == NULL){
        if(is_locals_dict(o)){
            save_assignment(key, NULL, value, 0);   // This was caused by STORE_NAME
        } else {
            save_assignment(o, key, value, 1);      // This is a real STORE_SUBSCR
        }
    }
    objobjargproc real_method = (objobjargproc)hijacked_method(o->ob_type, 0);
    return real_method(o, key, value);
}

// o.name = value
int jam_set_attro(PyObject *o, PyObject *name, PyObject *value) {
    save_assignment(o, name, value, 2);
    setattrofunc real_method = (setattrofunc)hijacked_method(o->ob_type, 1);
    return real_method(o, name, value);
}

// o[i] = value
int jam_set_item(PyObject *o, Py_ssize_t i, PyObject *value) {
    // I can't actually find anything that ever calls this, because pretty much 
    // everything also has tp_as_mapping which is preferred by PyObject_SetItem
    // see https://github.com/python/cpython/blob/master/Objects/abstract.c#L188
    save_assignment(o, PyLong_FromSsize_t(i), value, 1);
    ssizeobjargproc real_method = (ssizeobjargproc)hijacked_method(o->ob_type, 2);
    return real_method(o, i, value);
}

// o.name = value (deprecated, include it just in case)
int jam_set_attr(PyObject *o, char *name, PyObject *value){
    save_assignment(o, PyUnicode_FromString(name), value, 2);
    setattrfunc real_method = (setattrfunc)hijacked_method(o->ob_type, 3);
    return real_method(o, name, value);
}

void hijack_assignment_calls(PyTypeObject* type){
    void** methods = new void*[4]{NULL, NULL, NULL, NULL};
    method_ptrs.push_back(methods);
    type->tp_cache = PyLong_FromVoidPtr(methods);   // tp_cache is "unused"

    PyMappingMethods *meth_map = type->tp_as_mapping;
    if(meth_map && meth_map->mp_ass_subscript){
        methods[0] = (void*)meth_map->mp_ass_subscript;
        meth_map->mp_ass_subscript = jam_set_subscript; // Replace with my function
    }
    
    setattrofunc set_attro = type->tp_setattro;
    if(set_attro){
        methods[1] = (void*)set_attro;
        type->tp_setattro = jam_set_attro;              // Replace with my function
    }

    PySequenceMethods *meth_seq = type->tp_as_sequence;
    if(meth_seq && meth_seq->sq_ass_item){
        methods[2] = (void*)meth_seq->sq_ass_item;
        meth_seq->sq_ass_item = jam_set_item;           // Replace with my function
    }

    setattrfunc set_attr = type->tp_setattr;
    if(set_attr){
        methods[3] = (void*)set_attr;
        type->tp_setattr = jam_set_attr;                // Replace with my function
    }

    if(type->tp_base && type->tp_base->tp_cache){
        for(int i = 0; i < 4; i++){
            methods[i] = hijacked_method(type->tp_base, i);
        }
    }

    hijacked_types.push_back(type);
}

void unhijack_assignment_calls(PyTypeObject* type){
    PyMappingMethods *meth_map = type->tp_as_mapping;
    if(meth_map && meth_map->mp_ass_subscript){
        meth_map->mp_ass_subscript = (objobjargproc)hijacked_method(type, 0);
    }

    type->tp_setattro = (setattrofunc)hijacked_method(type, 1);

    PySequenceMethods *meth_seq = type->tp_as_sequence;
    if(meth_seq && meth_seq->sq_ass_item){
        meth_seq->sq_ass_item = (ssizeobjargproc)hijacked_method(type, 2);
    }

    type->tp_setattr = (setattrfunc)hijacked_method(type, 3);

    type->tp_cache = NULL;
}

void unhijack_everything(){
    for(auto& type : hijacked_types){
        unhijack_assignment_calls(type);
    }

    for(const auto& p : method_ptrs) {
        delete p;
    }
}

PyTypeObject* hijacked_dict(){
	if(hijacked_dict_addr == NULL){
		auto dict = PyDict_New();
	    hijack_assignment_calls(dict->ob_type);
	    hijacked_dict_type = *(dict->ob_type);		// Copy to new address
	    hijacked_dict_addr = &(hijacked_dict_type);	// Save new address
	    Py_DECREF(dict);
	}

    return hijacked_dict_addr;
}

