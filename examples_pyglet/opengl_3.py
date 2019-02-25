#!/usr/bin/python
# $Id:$

'''In order to use the new features of OpenGL 3, you must explicitly create
an OpenGL 3 context.  You can do this by supplying the `major_version` and
`minor_version` attributes for a GL Config.

This example creates an OpenGL 3 context, prints the version string to stdout,
and exits.

At time of writing, only the beta nvidia driver on Windows and Linux support
OpenGL 3, and requires an 8-series or higher.

On Windows, OpenGL 3 API must be explicitly enabled using the nvemulate tool
[1].  Additionally, at time of writing the latest driver did not yet support
forward compatible or debug contexts.

On Linux, the only driver that currently exposes the required GLX extensions
is 177.61.02 -- later drivers (177.67, 177.68, 177.7*, 177.8*, 180.06) seem to
be missing the extensions.

[1] http://developer.nvidia.com/object/nvemulate.html
'''

from __future__ import print_function

import pyglet

# Specify the OpenGL version explicitly to request 3.0 features, including
# GLSL 1.3.
#
# Some other attributes relevant to OpenGL 3:
#   forward_compatible = True       To request a context without deprecated
#                                   functionality
#   debug = True                    To request a debug context
config = pyglet.gl.Config(major_version=3, minor_version=0)

# Create a context matching the above configuration.  Will fail if
# OpenGL 3 is not supported by the driver.
window = pyglet.window.Window(config=config, visible=False)

# Print the version of the context created.
print('OpenGL version:', window.context.get_info().get_version())

window.close()
