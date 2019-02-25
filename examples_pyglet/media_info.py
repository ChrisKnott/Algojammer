#!/usr/bin/env python

'''Print details of a media file that pyglet can open (requires AVbin).

Usage::

    media_info.py <filename>

'''

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import sys
import pyglet


def print_avbin_info():
    from pyglet.media import have_avbin

    if have_avbin():
        from pyglet.media.sources import avbin
        print('Using AVbin version %d (FFmpeg r%d)' % (
            avbin.get_version(),
            avbin.av.avbin_get_ffmpeg_revision()))
    else:
        print('AVbin not available; required for media decoding.')
        print('http://code.google.com/p/avbin')
        print()


def print_source_info(source):
    if source.info:
        if source.info.title:
            print('Title: %s' % source.info.title)
        if source.info.album:
            print('Album: %s' % source.info.album)
        if source.info.author:
            print('Author: %s' % source.info.author)
        if source.info.year:
            print('Year: %d' % source.info.year)
        if source.info.track:
            print('Track: %d' % source.info.track)
        if source.info.genre:
            print('Genre: %s' % source.info.genre)
        if source.info.copyright:
            print('Copyright: %s' % source.info.copyright)
        if source.info.comment:
            print('Comment: %s' % source.info.comment)

    if source.audio_format:
        af = source.audio_format
        print('Audio: %d channel(s), %d bits, %.02f Hz' % (
            af.channels, af.sample_size, af.sample_rate))

    if source.video_format:
        vf = source.video_format
        if vf.frame_rate:
            frame_rate = '%.02f' % vf.frame_rate
        else:
            frame_rate = 'unknown'
        if vf.sample_aspect >= 1:
            display_width = vf.sample_aspect * vf.width
            display_height = vf.height
        else:
            display_width = vf.width
            display_height = vf.sample_aspect / vf.height
        print('Video: %dx%d at aspect %r (displays at %dx%d), %s fps' % (
            vf.width, vf.height, vf.sample_aspect,
            display_width, display_height, frame_rate))

    hours = int(source.duration / 3600)
    minutes = int(source.duration / 60) % 60
    seconds = int(source.duration) % 60
    milliseconds = int(source.duration * 1000) % 1000
    print('Duration: %d:%02d:%02d.%03d' % (
        hours, minutes, seconds, milliseconds))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        print_avbin_info()
        sys.exit(1)

    print_avbin_info()

    filename = sys.argv[1]
    try:
        source = pyglet.media.load(filename, streaming=True)
        print_source_info(source)
    except pyglet.media.MediaException:
        print('Could not open %s' % filename)
