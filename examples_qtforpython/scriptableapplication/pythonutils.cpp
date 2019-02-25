/****************************************************************************
**
** Copyright (C) 2017 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Qt for Python examples of the Qt Toolkit.
**
** $QT_BEGIN_LICENSE:BSD$
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** BSD License Usage
** Alternatively, you may use this file under the terms of the BSD license
** as follows:
**
** "Redistribution and use in source and binary forms, with or without
** modification, are permitted provided that the following conditions are
** met:
**   * Redistributions of source code must retain the above copyright
**     notice, this list of conditions and the following disclaimer.
**   * Redistributions in binary form must reproduce the above copyright
**     notice, this list of conditions and the following disclaimer in
**     the documentation and/or other materials provided with the
**     distribution.
**   * Neither the name of The Qt Company Ltd nor the names of its
**     contributors may be used to endorse or promote products derived
**     from this software without specific prior written permission.
**
**
** THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
** "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
** LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
** A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
** OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
** SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
** LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
** DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
** THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
** (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
** OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
**
** $QT_END_LICENSE$
**
****************************************************************************/

#include "pythonutils.h"

#include <QtCore/QByteArray>
#include <QtCore/QCoreApplication>
#include <QtCore/QDebug>
#include <QtCore/QStringList>
#include <QtCore/QTemporaryFile>
#include <QtCore/QDir>

#include <sbkpython.h>
#include <sbkconverter.h>
#include <sbkmodule.h>

/* from AppLib bindings */

#if PY_MAJOR_VERSION >= 3
    extern "C" PyObject *PyInit_AppLib();
#else
    extern "C" void initAppLib();
#endif

// This variable stores all Python types exported by this module.
extern PyTypeObject **SbkAppLibTypes;

// This variable stores all type converters exported by this module.
extern SbkConverter **SbkAppLibTypeConverters;

namespace PythonUtils {

static State state = PythonUninitialized;

static void cleanup()
{
    if (state > PythonUninitialized) {
        Py_Finalize();
        state = PythonUninitialized;
    }
}

State init()
{
    if (state > PythonUninitialized)
        return state;

    // If there is an active python virtual environment, use that environment's packages location.
    QByteArray virtualEnvPath = qgetenv("VIRTUAL_ENV");
    if (!virtualEnvPath.isEmpty())
        qputenv("PYTHONHOME", virtualEnvPath);

    Py_Initialize();
    qAddPostRoutine(cleanup);
    state = PythonInitialized;
#if PY_MAJOR_VERSION >= 3
    const bool pythonInitialized = PyInit_AppLib() != nullptr;
#else
    const bool pythonInitialized = true;
    initAppLib();
#endif
    const bool pyErrorOccurred = PyErr_Occurred() != nullptr;
    if (pythonInitialized && !pyErrorOccurred) {
        state = AppModuleLoaded;
    } else {
        if (pyErrorOccurred)
            PyErr_Print();
        qWarning("Failed to initialize the module.");
    }
    return state;
}

bool bindAppObject(const QString &moduleName, const QString &name,
                      int index, QObject *o)
{
    if (init() != AppModuleLoaded)
        return false;
    PyTypeObject *typeObject = SbkAppLibTypes[index];

    PyObject *po = Shiboken::Conversions::pointerToPython(reinterpret_cast<SbkObjectType *>(typeObject), o);
    if (!po) {
        qWarning() << __FUNCTION__ << "Failed to create wrapper for" << o;
        return false;
    }
    Py_INCREF(po);

    PyObject *module = PyImport_AddModule(moduleName.toLocal8Bit().constData());
    if (!module) {
        Py_DECREF(po);
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed to locate module" << moduleName;
        return false;
    }

    if (PyModule_AddObject(module, name.toLocal8Bit().constData(), po) < 0) {
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed add object" << name << "to" << moduleName;
        return false;
    }

    return true;
}

bool runScript(const QStringList &script)
{
    if (init() == PythonUninitialized)
        return false;

    // Concatenating all the lines
    QString content;
    QTextStream ss(&content);
    for (const QString &line: script)
        ss << line << "\n";

    // Executing the whole script as one line
    bool result = true;
    const QByteArray line = content.toUtf8();
    if (PyRun_SimpleString(line.constData()) == -1) {
        if (PyErr_Occurred())
            PyErr_Print();
        result = false;
    }

    return result;
}

} // namespace PythonUtils
