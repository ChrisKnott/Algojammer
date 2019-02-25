#############################################################################
##
## Copyright (C) 2018 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Qt for Python examples of the Qt Toolkit.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

import os, glob, re, sys, imp
from distutils import sysconfig

usage = """
Utility to determine include/link options of PySide2 and Python for qmake

Usage: pyside2_config.py [option]
Options:
    --python-include            Print Python include path
    --python-link               Print Python link flags
    --pyside2                   Print PySide2 location
    --pyside2-include           Print PySide2 include paths
    --pyside2-link              Print PySide2 link flags
    --pyside2-shared-libraries  Print paths of PySide2 shared libraries (.so's, .dylib's, .dll's)
    -a                          Print all
    --help/-h                   Print this help
"""

def cleanPath(path):
    return path if sys.platform != 'win32' else path.replace('\\', '/')

def sharedLibrarySuffix():
    if sys.platform == 'win32':
        return 'lib'
    elif sys.platform == 'darwin':
        return 'dylib'
    # Linux
    else:
        return 'so.*'

def sharedLibraryGlobPattern():
    glob = '*.' + sharedLibrarySuffix()
    return glob if sys.platform == 'win32' else 'lib' + glob

def filterPySide2SharedLibraries(list, only_shiboken=False):
    def predicate(item):
        basename = os.path.basename(item)
        if 'shiboken' in basename or ('pyside2' in basename and not only_shiboken):
            return True
        return False
    result = [item for item in list if predicate(item)]
    return result

# Return qmake link option for a library file name
def linkOption(lib):
    # On Linux:
    # Since we cannot include symlinks with wheel packages
    # we are using an absolute path for the libpyside and libshiboken
    # libraries when compiling the project
    baseName = os.path.basename(lib)
    link = ' -l'
    if sys.platform in ['linux', 'linux2']: # Linux: 'libfoo.so' -> '/absolute/path/libfoo.so'
        link = lib
    elif sys.platform in ['darwin']: # Darwin: 'libfoo.so' -> '-lfoo'
        link += os.path.splitext(baseName[3:])[0]
    else: # Windows: 'libfoo.dll' -> 'libfoo.dll'
        link += os.path.splitext(baseName)[0]
    return link

# Locate PySide2 via package path
def findPySide2():
    for p in sys.path:
        if 'site-' in p:
            pyside2 = os.path.join(p, 'PySide2')
            if os.path.exists(pyside2):
                return cleanPath(os.path.realpath(pyside2))
    return None

# Return version as "3.5"
def pythonVersion():
    return str(sys.version_info[0]) + '.' + str(sys.version_info[1])

def pythonInclude():
    return sysconfig.get_python_inc()

def pythonLinkQmake():
    flags = pythonLinkData()
    if sys.platform == 'win32':
        libdir = flags['libdir']
        # This will add the "~1" shortcut for directories that
        # contain white spaces
        # e.g.: "Program Files" to "Progra~1"
        for d in libdir.split("\\"):
            if " " in d:
                libdir = libdir.replace(d, d.split(" ")[0][:-1]+"~1")
        return '-L{} -l{}'.format(libdir, flags['lib'])
    elif sys.platform == 'darwin':
        return '-L{} -l{}'.format(flags['libdir'], flags['lib'])

    else:
        # Linux and anything else
        return '-L{} -l{}'.format(flags['libdir'], flags['lib'])

def pythonLinkCmake():
    flags = pythonLinkData()
    libdir = flags['libdir']
    lib = re.sub(r'.dll$', '.lib', flags['lib'])
    return '{};{}'.format(libdir, lib)

def pythonLinkData():
    # @TODO Fix to work with static builds of Python
    libdir = sysconfig.get_config_var('LIBDIR')
    if libdir is None:
        libdir = os.path.abspath(os.path.join(
            sysconfig.get_config_var('LIBDEST'), "..", "libs"))
    version = pythonVersion()
    version_no_dots = version.replace('.', '')

    flags = {}
    flags['libdir'] = libdir
    if sys.platform == 'win32':
        suffix = '_d' if any([tup[0].endswith('_d.pyd') for tup in imp.get_suffixes()]) else ''
        flags['lib'] = 'python{}{}'.format(version_no_dots, suffix)

    elif sys.platform == 'darwin':
        flags['lib'] = 'python{}'.format(version)

    # Linux and anything else
    else:
        if sys.version_info[0] < 3:
            suffix = '_d' if any([tup[0].endswith('_d.so') for tup in imp.get_suffixes()]) else ''
            flags['lib'] = 'python{}{}'.format(version, suffix)
        else:
            flags['lib'] = 'python{}{}'.format(version, sys.abiflags)

    return flags

def pyside2Include(only_shiboken=False):
    pySide2 = findPySide2()
    if pySide2 is None:
        return None

    includes = "{0}/include/shiboken2".format(pySide2)
    if not only_shiboken:
        includes = includes + " {0}/include/PySide2".format(pySide2)

    return includes

def pyside2Link():
    pySide2 = findPySide2()
    if pySide2 is None:
        return None
    link = "-L{}".format(pySide2)
    glob_result = glob.glob(os.path.join(pySide2, sharedLibraryGlobPattern()))
    for lib in filterPySide2SharedLibraries(glob_result):
        link += ' '
        link += linkOption(lib)
    return link

def pyside2SharedLibrariesData(only_shiboken=False):
    pySide2 = findPySide2()
    if pySide2 is None:
        return None

    glob_result = glob.glob(os.path.join(pySide2, sharedLibraryGlobPattern()))
    filtered_libs = filterPySide2SharedLibraries(glob_result, only_shiboken)
    libs = []
    if sys.platform == 'win32':
        for lib in filtered_libs:
            libs.append(os.path.realpath(lib))
    else:
        for lib in filtered_libs:
            libs.append(lib)
    return libs

def pyside2SharedLibraries():
    libs = pyside2SharedLibrariesData()
    if libs is None:
        return None

    if sys.platform == 'win32':
        if not libs:
            return ''
        dlls = ''
        for lib in libs:
            dll = os.path.splitext(lib)[0] + '.dll'
            dlls += dll + ' '

        return dlls
    else:
        libs_string = ''
        for lib in libs:
            libs_string += lib + ' '
        return libs_string

def pyside2SharedLibrariesCmake(only_shiboken=False):
    libs = pyside2SharedLibrariesData(only_shiboken)
    result = ';'.join(libs)
    return result

option = sys.argv[1] if len(sys.argv) == 2 else '-a'
if option == '-h' or option == '--help':
    print(usage)
    sys.exit(0)

generic_error = (' Did you forget to activate your virtualenv? Or perhaps'
                 ' you forgot to build / install PySide2 into your currently active Python'
                 ' environment?')
pyside2_error = 'Unable to locate PySide2.' + generic_error
pyside2_libs_error = 'Unable to locate the PySide2 shared libraries.' + generic_error
python_link_error = 'Unable to locate the Python library for linking.'

if option == '--pyside2' or option == '-a':
    pySide2 = findPySide2()
    if pySide2 is None:
        sys.exit(pyside2_error)
    print(pySide2)

if option == '--pyside2-link' or option == '-a':
    l = pyside2Link()
    if l is None:
        sys.exit(pyside2_error)

    print(l)

if option == '--shiboken-include' or option == '-a':
    i = pyside2Include(only_shiboken=True)
    if i is None:
        sys.exit(pyside2_error)
    print(i)

if option == '--pyside2-include' or option == '-a':
    i = pyside2Include()
    if i is None:
        sys.exit(pyside2_error)
    print(i)

if option == '--python-include' or option == '-a':
    i = pythonInclude()
    if i is None:
        sys.exit('Unable to locate the Python include headers directory.')
    print(i)

if option == '--python-link' or option == '-a':
    l = pythonLinkQmake()
    if l is None:
        sys.exit(python_link_error)
    print(l)

if option == '--python-link-cmake' or option == '-a':
    l = pythonLinkCmake()
    if l is None:
        sys.exit(python_link_error)
    print(l)

if option == '--pyside2-shared-libraries' or option == '-a':
    l = pyside2SharedLibraries()
    if l is None:
        sys.exit(pyside2_libs_error)
    print(l)

if option == '--pyside2-shared-libraries-cmake' or option == '-a':
    l = pyside2SharedLibrariesCmake()
    if l is None:
        sys.exit(pyside2_libs_error)
    print(l)

if option == '--shiboken-shared-libraries-cmake' or option == '-a':
    l = pyside2SharedLibrariesCmake(only_shiboken=True)
    if l is None:
        sys.exit(pyside2_libs_error)
    print(l)
