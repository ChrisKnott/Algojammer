'''
A silly demonstration of how to use the Apple remote.
'''

from __future__ import print_function

__docformat__ = 'restructuredtext'
__version__ = '$Id: $'

import pyglet
from pyglet.gl import *
import sys


class MainWindow(pyglet.window.Window):
    def __init__(self):
        super(MainWindow, self).__init__(visible=False)
        self.set_caption('Apple Remote Example')

        # Look for the Apple Remote device.
        remote = pyglet.input.get_apple_remote()
        if not remote:
            print('Apple IR Remote not available.')
            sys.exit(0)

        # Open the remote in exclusive mode so that pressing the remote
        # buttons does not activate Front Row, change volume, etc. while
        # the remote is being used by our program.
        remote.open(self, exclusive=True)

        # We push this class onto the remote's event handler stack so that
        # the on_button_press and on_button_release methods which we define
        # below will be called for the appropriate remote events.
        remote.push_handlers(self)

        self.carousel = Carousel()
        self.setup_opengl()
        pyglet.clock.schedule_interval(self.update, 1/60.0)

    # Event handler for Apple Remote button press events.
    # The button parameter is a string specifying the button that was pressed.
    def on_button_press(self, button):
        print('on_button_press', button)

        if button == 'up':
            self.carousel.scroll_up()
        elif button == 'down':
            self.carousel.scroll_down()
        elif button == 'left':
            self.carousel.step_left()
        elif button == 'right':
            self.carousel.step_right()
        elif button == 'left_hold':
            self.carousel.rotate_left()
        elif button == 'right_hold':
            self.carousel.rotate_right()
        elif button == 'select' or button == 'select_hold':
            self.carousel.swap_left()
        elif button == 'menu' or button == 'menu_hold':
            self.carousel.swap_right()

    # Event handler for Apple Remote button release events.
    # The button parameter is a string specifying the button that was released.
    def on_button_release(self, button):
        print('on_button_release', button)

        if button == 'left_hold':
            self.carousel.stop_rotating()
        elif button == 'right_hold':
            self.carousel.stop_rotating()

    def on_draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        gluLookAt(0,3,-12,0,3,0,0,1,0)
        self.carousel.draw()

    def on_resize(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = width / float(height)
        glFrustum(-1,1,-1.8/aspect,0.2/aspect,1,100)
        glMatrixMode(GL_MODELVIEW)
        return pyglet.event.EVENT_HANDLED

    def setup_opengl(self):
        glClearColor(1,1,1,1)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    def update(self, dt):
        self.carousel.update(dt)


class Carousel:
    """A rotating collection of labeled tiles."""
    def __init__(self):
        self.num_tiles = 14
        self.index = 0
        self.float_index = 0.0
        self.float_increment = 1.0 / self.num_tiles
        self.angle = 0
        self.index_diff = 0
        self.is_rotating = False
        self.speed = 4 * self.num_tiles

        # Create the tiles in the carousel.
        self.tiles = []
        colors = [(255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,205,205), (128,0,128), (255,165,0)]
        class Tile:
            value = 0
            color = [255,255,255]
        for i in range(self.num_tiles):
            tile = Tile()
            tile.value = i % 26
            tile.color = colors[i%len(colors)]
            self.tiles.append(tile)

        # Create glyphs for the characters displayed on the tiles.
        font = pyglet.font.load('Courier', 64)
        self.glyphs = font.get_glyphs('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

    def scroll_up(self):
        """Increment the character displayed on the main tile."""
        self.tiles[self.index].value = (self.tiles[self.index].value + 1) % 26

    def scroll_down(self):
        """Decrement the character displayed on the main tile."""
        self.tiles[self.index].value = (self.tiles[self.index].value - 1) % 26

    def swap_left(self):
        """Swap the two left tiles."""
        i = self.index
        j = (self.index - 1) % self.num_tiles
        self.tiles[i], self.tiles[j] = self.tiles[j], self.tiles[i]

    def swap_right(self):
        """Swap the two right tiles."""
        i = self.index
        j = (self.index + 1) % self.num_tiles
        self.tiles[i], self.tiles[j] = self.tiles[j], self.tiles[i]

    def step_left(self):
        """Rotate the carousel one tile to the left."""
        self.direction = -1
        self.index_diff += 1.0

    def step_right(self):
        """Rotate the carousel one tile to the right."""
        self.direction = 1
        self.index_diff += 1.0

    def rotate_left(self):
        """Start the carousel rotating continuously to the left."""
        self.is_rotating = True
        self.direction = -1

    def rotate_right(self):
        """Start the carousel rotating continuously to the right."""
        self.is_rotating = True
        self.direction = 1

    def stop_rotating(self):
        """Stop continuous rotation and make sure we end up at a tile location."""
        self.index_diff = round(self.float_index) - self.float_index
        if self.index_diff < 0:
            self.direction = -1
        else:
            self.direction = 1
        self.index_diff = abs(self.index_diff)

    def draw(self):
        glPushMatrix()
        glRotatef(-self.angle, 0, 1, 0)
        for i in range(self.num_tiles):
            self.draw_tile(i)
        glPopMatrix()

    def draw_tile(self, index):
        angle = index * (360.0 / self.num_tiles)

        glPushMatrix()
        glRotatef(angle,0,1,0)
        glTranslatef(0,0,-7.5)
        glRotatef(-angle+self.angle,0,1,0)

        texture = self.glyphs[self.tiles[index].value].texture
        vertex_list = pyglet.graphics.vertex_list(4, 'v2f', ('t3f', texture.tex_coords))
        vertex_list.vertices[:] = [-1, -1, 1, -1, 1, 1, -1, 1]
        # Draw tile background.
        glColor3ub(*self.tiles[index].color)
        vertex_list.draw(GL_QUADS)
        # Draw tile label.
        glBindTexture(texture.target, texture.id)
        glEnable(texture.target)
        glColor3ub(0,0,0)
        vertex_list.vertices[:] = [.8, -.8, -.8, -.8, -.8, .8, .8, .8]
        glTranslatef(0,0,-.01)
        vertex_list.draw(GL_QUADS)
        glDisable(texture.target)
        glPopMatrix()

    def update(self, dt):
        if self.is_rotating or self.index_diff:
            increment = self.direction * self.speed * self.float_increment * dt
            self.float_index = (self.float_index + increment) % self.num_tiles

            if self.index_diff:
                self.index_diff -= abs(increment)
                if self.index_diff < 0:
                    self.index_diff = 0
                    self.float_index = round(self.float_index) % self.num_tiles
                    self.index = int(self.float_index)
                    self.is_rotating = False

            self.angle = (self.float_index / self.num_tiles) * 360


if __name__ == '__main__':
    window = MainWindow()
    window.clear()
    window.flip()
    window.set_visible(True)
    pyglet.app.run()
