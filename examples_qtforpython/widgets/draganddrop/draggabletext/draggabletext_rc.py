# -*- coding: utf-8 -*-

#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2016 The Qt Company Ltd.
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

# Resource object code
#
# Created: Fri Jul 30 17:41:35 2010
#      by: The Resource Compiler for PySide (Qt v4.6.2)
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore

qt_resource_data = b"\
\x00\x00\x00\xf7\
\x51\
\x74\x0a\x51\x75\x61\x72\x74\x65\x72\x6c\x79\x0a\x69\x73\x0a\x61\
\x0a\x70\x61\x70\x65\x72\x0a\x62\x61\x73\x65\x64\x0a\x6e\x65\x77\
\x73\x6c\x65\x74\x74\x65\x72\x0a\x65\x78\x63\x6c\x75\x73\x69\x76\
\x65\x6c\x79\x0a\x61\x76\x61\x69\x6c\x61\x62\x6c\x65\x0a\x74\x6f\
\x0a\x51\x74\x0a\x63\x75\x73\x74\x6f\x6d\x65\x72\x73\x0a\x45\x76\
\x65\x72\x79\x0a\x71\x75\x61\x72\x74\x65\x72\x0a\x77\x65\x0a\x6d\
\x61\x69\x6c\x0a\x6f\x75\x74\x0a\x61\x6e\x0a\x69\x73\x73\x75\x65\
\x0a\x74\x68\x61\x74\x0a\x77\x65\x0a\x68\x6f\x70\x65\x0a\x77\x69\
\x6c\x6c\x0a\x62\x72\x69\x6e\x67\x0a\x61\x64\x64\x65\x64\x0a\x69\
\x6e\x73\x69\x67\x68\x74\x0a\x61\x6e\x64\x0a\x70\x6c\x65\x61\x73\
\x75\x72\x65\x0a\x74\x6f\x0a\x79\x6f\x75\x72\x0a\x51\x74\x0a\x70\
\x72\x6f\x67\x72\x61\x6d\x6d\x69\x6e\x67\x0a\x77\x69\x74\x68\x0a\
\x68\x69\x67\x68\x0a\x71\x75\x61\x6c\x69\x74\x79\x0a\x74\x65\x63\
\x68\x6e\x69\x63\x61\x6c\x0a\x61\x72\x74\x69\x63\x6c\x65\x73\x0a\
\x77\x72\x69\x74\x74\x65\x6e\x0a\x62\x79\x0a\x51\x74\x0a\x65\x78\
\x70\x65\x72\x74\x73\x0a\
"

qt_resource_name = b"\
\x00\x0a\
\x0b\x0b\x17\xd9\
\x00\x64\
\x00\x69\x00\x63\x00\x74\x00\x69\x00\x6f\x00\x6e\x00\x61\x00\x72\x00\x79\
\x00\x09\
\x08\xb6\xa7\x34\
\x00\x77\
\x00\x6f\x00\x72\x00\x64\x00\x73\x00\x2e\x00\x74\x00\x78\x00\x74\
"

qt_resource_struct = b"\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x01\
\x00\x00\x00\x00\x00\x02\x00\x00\x00\x01\x00\x00\x00\x02\
\x00\x00\x00\x1a\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\
"

def qInitResources():
    QtCore.qRegisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

def qCleanupResources():
    QtCore.qUnregisterResourceData(0x01, qt_resource_struct, qt_resource_name, qt_resource_data)

qInitResources()
