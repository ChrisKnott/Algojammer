#include "Python.h"
#include "recorder.h"
#include "hacks.h"
#include <vector>
#include <iostream>
// #include <unistd.h>
#include "sparsepp/spp.h"
#include <algorithm>

#define PYPRINT(obj) PyObject_Print(obj, stdout, 0);

using AssignOp = std::tuple<int, unsigned char, PyObject*, PyObject*, PyObject*>;
using Recording = std::tuple<std::vector<AssignOp>, std::vector<PyObject*>, PyObject*>;

int execution_step;
std::vector<int> line_history;

std::vector<Recording> recordings;  // Each recording has a starting state and 50,000 deltas
std::vector<AssignOp> assignment_history;
std::vector<PyObject*> pickle_order;
PyObject* start_state_pickle;

spp::sparse_hash_set<PyObject*> every_object_seen;
spp::sparse_hash_set<PyObject*> locals_dicts;
spp::sparse_hash_set<PyObject*> variable_names;

bool recording = false;
bool recording_paused = false;
PyObject* io_module             = PyImport_ImportModule("io");
PyObject* pickle_module         = PyImport_ImportModule("_pickle");
PyObject* pickler_str           = PyUnicode_FromString("Pickler");
PyObject* dump_str              = PyUnicode_FromString("dump");
PyObject* builtins_str          = PyUnicode_FromString("__builtins__");
PyObject* comprehension_iter    = PyUnicode_FromString(".0");
PyObject* start_state_pickler;

void reset_recorder(){
    execution_step = 0;
    line_history.clear();
    recordings.clear();
    variable_names.clear();
    reset_recording();
}

static bool seen_object(PyObject* obj){
    return every_object_seen.find(obj) != every_object_seen.end();
}

bool is_locals_dict(PyObject* obj){
    return locals_dicts.find(obj) != locals_dicts.end();
}

int save_visit(PyObject *obj, PyObject *arg){
    save_object(obj);
    return 0;
}

void save_object(PyObject* obj){
    if(obj != NULL && !PyModule_Check(obj) && !seen_object(obj)){
        Py_INCREF(obj); // To stop ID being reused
        every_object_seen.insert(obj);
        
        PyObject_CallMethodObjArgs(start_state_pickler, dump_str, obj, NULL);
        if(PyErr_Occurred() == NULL){
            pickle_order.push_back(obj);
            
            PyTypeObject* type = Py_TYPE(obj);

            if((type->tp_flags & Py_TPFLAGS_HEAPTYPE)){
                traverseproc traverse = type->tp_traverse;
                if(traverse){
                    traverse(obj, (visitproc)save_visit, NULL);
                }
            }
        } else {
            PyErr_Clear();
        }
    }
}

void reset_recording(){
    for(const auto& obj : pickle_order){
        Py_DECREF(obj);
    }

    start_state_pickle = PyObject_CallMethod(io_module, "BytesIO", NULL);
    start_state_pickler = PyObject_CallMethodObjArgs(pickle_module, pickler_str, start_state_pickle, NULL);
    assignment_history = std::vector<AssignOp>();
    pickle_order = std::vector<PyObject*>();
    every_object_seen.clear();
    locals_dicts.clear();
}

void save_assignment(PyObject *o, PyObject* k, PyObject* v, int kind){
    if(recording && !recording_paused){
        recording_paused = true;
        
        if(kind == 0){
            // We must be in my code, new binding of form 'o = v'
            if(PyObject_RichCompareBool(o, builtins_str, Py_NE) &&
                PyObject_RichCompareBool(o, comprehension_iter, Py_NE)){
                save_object(o);
                save_object(v);
                variable_names.insert(o);
                assignment_history.push_back(AssignOp(execution_step, 0, o, NULL, v));
            }
        } else if(seen_object(o)){
            // Seen o before somehow, so trace it's mutation from now on
            save_object(k);
            save_object(v);
            assignment_history.push_back(AssignOp(execution_step, kind, o, k, v));
        }

        recording_paused = false;
    }
}

void process_execution_step(int what, PyFrameObject *frame, PyObject *arg){
    recording = true;   // Turn on recording first time we hit algojammer maincode
    line_history.push_back(frame->f_lineno);
//    frame_history.push_back(frame->f_back->f_lineno);

    if(frame->f_locals == NULL){
        frame->f_locals = PyDict_New();
    }
    PyObject* locals = frame->f_locals;
    locals->ob_type = hijacked_dict();    // So PyDict_CheckExact() fails
    every_object_seen.insert(locals);
    locals_dicts.insert(locals);

    ++execution_step;

    PyFrame_FastToLocals(frame);    // Force "fast" vars into locals dict

    PyObject *key, *value;
    Py_ssize_t pos = 0;
    while(PyDict_Next(locals, &pos, &key, &value)) {
        // Hijack assignment operations for type (if we haven't already)
        if(value->ob_type->tp_cache == NULL){
            hijack_assignment_calls(value->ob_type);
        }
    }

    if(assignment_history.size() >= 50000){
        recordings.push_back(Recording(assignment_history, pickle_order, start_state_pickle));
        reset_recording();
        PyObject *key, *value;
        Py_ssize_t pos = 0;
        for(auto& dict : {frame->f_globals, frame->f_locals}){
            while(PyDict_Next(dict, &pos, &key, &value)) {
                save_assignment(key, NULL, value, 0);
            }
        }
    }
}

PyObject* get_recording(long step){
    recording_paused = true;
    std::vector<AssignOp> history; std::vector<PyObject*> order; PyObject* pickle;
    int s; unsigned char op; PyObject *o, *k, *v;

    history = assignment_history;
    order = pickle_order;
    pickle = start_state_pickle;
    
    if(history.size() > 0){
        int current_recording_start = std::get<0>(history[0]);
        if(current_recording_start > step){
            // We want state from older recording, find the relevant one
            for(auto& recording : recordings){
                std::tie(s, op, o, k, v) = std::get<0>(recording)[0];
                if(s <= step){
                    std::tie(history, order, pickle) = recording;
                } else {
                    break;
                }
            }
        }
    }

    PyObject *data_dict = PyDict_New();
    PyObject *pickle_order_list = PyList_New(order.size());
    for(size_t i = 0; i < order.size(); i++){
        PyList_SetItem(pickle_order_list, i, PyLong_FromVoidPtr(order[i]));
    }

    PyObject *assignments_list = PyList_New(history.size());
    for(size_t i = 0; i < history.size(); i++){
        std::tie(s, op, o, k, v) = history[i];
        PyObject* assignment = PyTuple_New(5);
        PyTuple_SET_ITEM(assignment, 0, PyLong_FromLong(s));
        PyTuple_SET_ITEM(assignment, 1, PyLong_FromLong(op));
        PyTuple_SET_ITEM(assignment, 2, PyLong_FromVoidPtr(o));
        PyTuple_SET_ITEM(assignment, 3, PyLong_FromVoidPtr(k));
        PyTuple_SET_ITEM(assignment, 4, PyLong_FromVoidPtr(v));
        PyList_SetItem(assignments_list, i, assignment);
    }

    PyDict_SetItemString(data_dict, "pickle_order", pickle_order_list);
    PyDict_SetItemString(data_dict, "pickle_bytes", pickle);
    PyDict_SetItemString(data_dict, "assignments", assignments_list);
    Py_DECREF(pickle_order_list);
    Py_DECREF(assignments_list);

    recording_paused = false;
    return data_dict;
}

PyObject* get_execution_lines(){
    PyObject *lines_list = PyList_New(line_history.size());
    for(size_t i = 0; i < line_history.size(); i++){
        PyList_SetItem(lines_list, i, PyLong_FromLong(line_history[i]));
    }

    line_history.clear();
    return lines_list;
}

PyObject* get_variable_names() {
    PyObject* variables_list = PyList_New(variable_names.size());
    size_t i = 0;
    for(const auto& obj : variable_names){
        Py_XINCREF(obj);
        PyList_SetItem(variables_list, i++, obj);
    }
    return variables_list;    
}

// ////============================= temp ==========
// #define OCCPR(x) if(step % 100000 == 0){ std::cout << x; };

// static int refs_count = 0;
// static PyObject *refs[1000];
// static void CLEAR_REFS(void) {
//     for (int i = 0; i < refs_count; i++) {
//         Py_DECREF(refs[i]);
//     }
//     refs_count = 0;
// }
// static char* PYSTR_TO_CHAR(PyObject *obj) {
//     PyObject *bytes = PyUnicode_AsUTF8String(obj);
//     refs[refs_count++] = bytes;
//     return PyBytes_AS_STRING(bytes);
// }

// int check = 0;
// ////=============================================



