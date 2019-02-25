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
# $Id$

import os
import math

from pyglet import media

class PlayerReader(object):
    def __init__(self, player):
        self.player = player

    def line(self, line, lineno):
        parts = line.split()
        if parts[0] == 'position':
            if len(parts) < 4:
                raise ReaderException('Invalid position line %d' % lineno)
            self.player.position = tuple([float(x) for x in parts[1:]])
        if parts[0] == 'cone_orientation':
            if len(parts) < 4:
                raise ReaderException('Invalid orientation line %d' % lineno)
            self.player.cone_orientation = tuple([float(x) for x in parts[1:]])
        elif parts[0] == 'outer_cone_angle':
            if len(parts) < 2:
                raise ReaderException('Invalid angle line %d' % lineno)
            self.player.cone_outer_angle = float(parts[1])
        elif parts[0] == 'inner_cone_angle':
            if len(parts) < 2:
                raise ReaderException('Invalid angle line %d' % lineno)
            self.player.cone_inner_angle = float(parts[1])
        elif parts[0] == 'label':
            if len(parts) < 2:
                raise ReaderException('Invalid label line %d' % lineno)
            self.player.label = parts[1]

class SpaceReader(object):
    def __init__(self, space):
        self.basedir = ''
        self.space = space

    def read(self, file):
        if not hasattr(file, 'read'):
            self.basedir = os.path.dirname(file)
            file = open(file, 'rt')
        elif hasattr(file, 'name'):
            self.basedir = os.path.dirname(file.name)
        reader = None
        lineno = 0
        for line in file:
            lineno += 1

            if not isinstance('', bytes) and isinstance(line, bytes):
                # decode bytes to str on Python 3
                line = line.decode('ascii')

            if not line.strip() or line.startswith('#'):
                continue
            if line.startswith(' '):
                if not reader:
                    raise ReaderException(
                        'Unexpected indented block line %d' % lineno)
                reader.line(line, lineno)
            else:
                reader = None
                parts = line.split()
                if parts[0] == 'loop':
                    if len(parts) < 2:
                        raise ReaderException(
                            'No loop filename line %d' % lineno)
                    player = media.Player()
                    player.eos_action = 'loop'
                    player.queue(self.source(parts[1], streaming=False))
                    self.space.add_player(player)
                    reader = PlayerReader(player)

    def source(self, filename, **kwargs):
        filename = os.path.join(self.basedir, filename)
        return media.load(filename, **kwargs)
