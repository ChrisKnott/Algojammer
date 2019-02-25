#!/usr/bin/env python
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions 
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright 
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

# An example setup.py that can be used to create both standalone Windows
# executables (requires py2exe) and Mac OS X applications (requires py2app).
#
# On Windows::
#
#     python setup.py py2exe
#
# On Mac OS X::
#
#     python setup.py py2app
#

from distutils.core import setup

import os

# The main entry point of the program
script_file = 'astraea.py'

# Create a list of data files.  Add everything in the 'res/' directory.
data_files = []
for file in os.listdir('res'):
    file = os.path.join('res', file)
    if os.path.isfile(file):
        data_files.append(file)

# Setup args that apply to all setups, including ordinary distutils.
setup_args = dict(
    data_files=[('res', data_files)]
)

# py2exe options
try:
    import py2exe
    setup_args.update(dict(
        windows=[dict(
            script=script_file,
            icon_resources=[(1, 'assets/app.ico')],
        )],
    ))
except ImportError:
    pass

# py2app options
try:
    import py2app
    setup_args.update(dict(
        app=[script_file],
        options=dict(py2app=dict(
            argv_emulation=True,
            iconfile='assets/app.icns',
        )),
    ))
except ImportError:
    pass

setup(**setup_args)
