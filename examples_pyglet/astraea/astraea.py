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

'''A sprite-based game loosely based on the classic "Asteroids".

Shoot the asteroids, get high score.

Left/right: Turn ship
Up: Thrusters
Space: Shoot
'''

import math
import os
import random
import sys

import pyglet
from pyglet.gl import *
from pyglet import resource
from pyglet.window import key

PLAYER_SPIN_SPEED = 360.
PLAYER_ACCEL = 200.
PLAYER_FIRE_DELAY = 0.1

BULLET_SPEED = 1000.

MAX_ASTEROID_SPIN_SPEED = 180.
MAX_ASTEROID_SPEED = 100.

INITIAL_ASTEROIDS = [2, 3, 4, 5]
ASTEROID_DEBRIS_COUNT = 3
MAX_DIFFICULTY = len(INITIAL_ASTEROIDS) - 1

ARENA_WIDTH = 640
ARENA_HEIGHT = 480

KEY_FIRE = key.SPACE
KEY_PAUSE = key.ESCAPE

COLLISION_RESOLUTION = 8

SMOKE_ANIMATION_PERIOD = 0.05
EXPLOSION_ANIMATION_PERIOD = 0.07
PLAYER_FLASH_PERIOD = 0.15

GET_READY_DELAY = 1.
BEGIN_PLAY_DELAY = 2.
LIFE_LOST_DELAY = 2.

FONT_NAME = ('Verdana', 'Helvetica', 'Arial')

INSTRUCTIONS = \
'''Your ship is lost in a peculiar unchartered area of space-time infested with asteroids!  You have no chance for survival except to rack up the highest score possible.

Left/Right: Turn ship
Up: Thrusters
Space: Shoot

Be careful, there's not much friction in space.'''

def center_anchor(img):
    img.anchor_x = img.width // 2
    img.anchor_y = img.height // 2

# --------------------------------------------------------------------------
# Game objects
# --------------------------------------------------------------------------

def wrap(value, width):
    if value > width:
        value -= width
    if value < 0:
        value += width
    return value

def to_radians(degrees):
    return math.pi * degrees / 180.0

class WrappingSprite(pyglet.sprite.Sprite):
    dx = 0
    dy = 0
    rotation_speed = 0

    def __init__(self, img, x, y, batch=None):
        super(WrappingSprite, self).__init__(img, x, y, batch=batch)
        self.collision_radius = self.image.width // COLLISION_RESOLUTION // 2 

    def update(self, dt):
        x = self.x + self.dx * dt
        y = self.y + self.dy * dt
        rotation = self.rotation + self.rotation_speed * dt
        
        self.x = wrap(x, ARENA_WIDTH)
        self.y = wrap(y, ARENA_HEIGHT)
        self.rotation = wrap(rotation, 360.)

    def collision_cells(self):
        '''Generate a sequence of (x, y) cells this object covers,
        approximately.''' 
        radius = self.collision_radius
        cellx = int(self.x / COLLISION_RESOLUTION)
        celly = int(self.y / COLLISION_RESOLUTION)
        for y in range(celly - radius, celly + radius + 1):
            for x in range(cellx - radius, cellx + radius + 1):
                yield x, y

class AsteroidSize(object):
    def __init__(self, filename, points):
        self.img = resource.image(filename)
        center_anchor(self.img)
        self.next_size = None
        self.points = points

class Asteroid(WrappingSprite):
    def __init__(self, size, x, y, batch=None):
        super(Asteroid, self).__init__(size.img, x, y, batch=batch)
        self.dx = (random.random() - 0.5) * MAX_ASTEROID_SPEED
        self.dy = (random.random() - 0.5) * MAX_ASTEROID_SPEED
        self.size = size
        self.rotation = random.random() * 360.
        self.rotation_speed = (random.random() - 0.5) * MAX_ASTEROID_SPIN_SPEED
        self.hit = False

    def destroy(self):
        global score
        score += self.size.points

        # Modifies the asteroids list.
        next_size = self.size.next_size
        if next_size:
            # Spawn debris
            for i in range(ASTEROID_DEBRIS_COUNT):
                asteroids.append(Asteroid(next_size, self.x, self.y,
                                          batch=self.batch))

        self.delete()
        asteroids.remove(self)

class Player(WrappingSprite, key.KeyStateHandler):
    def __init__(self, img, batch=None):
        super(Player, self).__init__(img, ARENA_WIDTH // 2, ARENA_HEIGHT // 2,
            batch=batch)
        center_anchor(img)
        self.reset()

    def reset(self):
        self.x = ARENA_WIDTH // 2
        self.y = ARENA_HEIGHT // 2
        self.dx = 0
        self.dy = 0
        self.rotation = 0
        self.fire_timeout = 0
        self.hit = False
        self.invincible = True
        self.visible = True

        self.flash_timeout = 0
        self.flash_visible = False

    def update(self, dt):
        # Update rotation
        if self[key.LEFT]:
            self.rotation -= PLAYER_SPIN_SPEED * dt
        if self[key.RIGHT]:
            self.rotation += PLAYER_SPIN_SPEED * dt

        # Get x/y components of orientation
        rotation_x = math.cos(to_radians(-self.rotation))
        rotation_y = math.sin(to_radians(-self.rotation))

        # Update velocity
        if self[key.UP]:
            self.dx += PLAYER_ACCEL * rotation_x * dt
            self.dy += PLAYER_ACCEL * rotation_y * dt

        # Update position
        super(Player, self).update(dt)

        # Fire bullet?
        self.fire_timeout -= dt
        if self[KEY_FIRE] and self.fire_timeout <= 0 and not self.invincible:
            self.fire_timeout = PLAYER_FIRE_DELAY

            # For simplicity, start the bullet at the player position.  If the
            # ship were bigger, or if bullets moved slower we'd adjust this
            # based on the orientation of the ship.
            bullets.append(Bullet(self.x, self.y, 
                                  rotation_x * BULLET_SPEED,
                                  rotation_y * BULLET_SPEED, batch=batch))

            if enable_sound:
                bullet_sound.play()

        # Update flash (invincible) animation
        if self.invincible:
            self.flash_timeout -= dt
            if self.flash_timeout <= 0:
                self.flash_timeout = PLAYER_FLASH_PERIOD
                self.flash_visible = not self.flash_visible
        else:
            self.flash_visible = True

        self.opacity = (self.visible and self.flash_visible) and 255 or 0

class MovingSprite(pyglet.sprite.Sprite):
    def __init__(self, image, x, y, dx, dy, batch=None):
        super(MovingSprite, self).__init__(image, x, y, batch=batch)
        self.dx = dx
        self.dy = dy

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

class Bullet(MovingSprite):
    def __init__(self, x, y, dx, dy, batch=None):
        super(Bullet, self).__init__(bullet_image, x, y, dx, dy, batch=batch)

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt
        if not (self.x >= 0 and self.x < ARENA_WIDTH and
                self.y >= 0 and self.y < ARENA_HEIGHT):
            self.delete()
            bullets.remove(self)

class EffectSprite(MovingSprite):
    def on_animation_end(self):
        self.delete()
        animations.remove(self)

class Starfield(object):
    def __init__(self, img):
        self.x = 0
        self.y = 0
        self.dx = 0.05
        self.dy = -0.06
        self.img = img

    def update(self, dt):
        self.x += self.dx * dt
        self.y += self.dy * dt

    def draw(self):
        # Fiddle with the texture matrix to make the starfield slide slowly
        # over the window.
        glMatrixMode(GL_TEXTURE)
        glPushMatrix()
        glTranslatef(self.x, self.y, 0)
        
        self.img.blit(0, 0, width=ARENA_WIDTH, height=ARENA_HEIGHT)
        
        glPopMatrix()
        glMatrixMode(GL_MODELVIEW)

# --------------------------------------------------------------------------
# Overlays, such as menus and "Game Over" banners
# --------------------------------------------------------------------------

class Overlay(object):
    def update(self, dt):
        pass

    def draw(self):
        pass

class Banner(Overlay):
    def __init__(self, label, dismiss_func=None, timeout=None):
        self.text = pyglet.text.Label(label,
                                      font_name=FONT_NAME,
                                      font_size=36,
                                      x=ARENA_WIDTH // 2, 
                                      y=ARENA_HEIGHT // 2,
                                      anchor_x='center',
                                      anchor_y='center')

        self.dismiss_func = dismiss_func
        self.timeout = timeout
        if timeout and dismiss_func:
            pyglet.clock.schedule_once(dismiss_func, timeout)

    def draw(self):
        self.text.draw()

    def on_key_press(self, symbol, modifiers):
        if self.dismiss_func and not self.timeout:
            self.dismiss_func()
        return True

class Menu(Overlay):
    def __init__(self, title):
        self.items = []
        self.title_text = pyglet.text.Label(title, 
                                            font_name=FONT_NAME,
                                            font_size=36,
                                            x=ARENA_WIDTH // 2, 
                                            y=350,
                                            anchor_x='center',
                                            anchor_y='center')

    def reset(self):
        self.selected_index = 0
        self.items[self.selected_index].selected = True

    def on_key_press(self, symbol, modifiers):
        if symbol == key.DOWN:
            self.selected_index += 1
        elif symbol == key.UP:
            self.selected_index -= 1
        self.selected_index = min(max(self.selected_index, 0), 
                                  len(self.items) - 1)

        if symbol in (key.DOWN, key.UP) and enable_sound:
            bullet_sound.play()

    def on_key_release(self, symbol, modifiers):
        self.items[self.selected_index].on_key_release(symbol, modifiers)

    def draw(self):
        self.title_text.draw()
        for i, item in enumerate(self.items):
            item.draw(i == self.selected_index)

class MenuItem(object):
    pointer_color = (.46, 0, 1.)
    inverted_pointers = False

    def __init__(self, label, y, activate_func):
        self.y = y
        self.text = pyglet.text.Label(label,
                                      font_name=FONT_NAME,
                                      font_size=14,
                                      x=ARENA_WIDTH // 2, 
                                      y=y,
                                      anchor_x='center',
                                      anchor_y='center')
        self.activate_func = activate_func

    def draw_pointer(self, x, y, color, flip=False):
        # Tint the pointer image to a color
        glPushAttrib(GL_CURRENT_BIT)
        glColor3f(*color)
        if flip:
            pointer_image_flip.blit(x, y)
        else:
            pointer_image.blit(x, y)
        glPopAttrib()

    def draw(self, selected):
        self.text.draw()

        if selected:
            self.draw_pointer(
                self.text.x - self.text.content_width // 2 - 
                    pointer_image.width // 2,
                self.y, 
                self.pointer_color,
                self.inverted_pointers)
            self.draw_pointer(
                self.text.x + self.text.content_width // 2 + 
                    pointer_image.width // 2,
                self.y,
                self.pointer_color,
                not self.inverted_pointers)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.ENTER and self.activate_func:
            self.activate_func()
            if enable_sound:
                bullet_sound.play()

class ToggleMenuItem(MenuItem):
    pointer_color = (.27, .82, .25)
    inverted_pointers = True

    def __init__(self, label, value, y, toggle_func):
        self.value = value
        self.label = label
        self.toggle_func = toggle_func
        super(ToggleMenuItem, self).__init__(self.get_label(), y, None)

    def get_label(self):
        return self.label + (self.value and ': ON' or ': OFF')

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT or symbol == key.RIGHT:
            self.value = not self.value
            self.text.text = self.get_label()
            self.toggle_func(self.value)
            if enable_sound:
                bullet_sound.play()

class DifficultyMenuItem(MenuItem):
    pointer_color = (.27, .82, .25)
    inverted_pointers = True

    def __init__(self, y):
        super(DifficultyMenuItem, self).__init__(self.get_label(), y, None)

    def get_label(self):
        if difficulty == 0:
            return 'Difficulty: Pebbles'
        elif difficulty == 1:
            return 'Difficulty: Stones'
        elif difficulty == 2:
            return 'Difficulty: Asteroids'
        elif difficulty == 3:
            return 'Difficulty: Meteors'
        else:
            return 'Difficulty: %d' % difficulty

    def on_key_release(self, symbol, modifiers):
        global difficulty
        if symbol == key.LEFT:
            difficulty -= 1
        elif symbol == key.RIGHT:
            difficulty += 1
        difficulty = min(max(difficulty, 0), MAX_DIFFICULTY)
        self.text.text = self.get_label()

        if symbol in (key.LEFT, key.RIGHT) and enable_sound:
            bullet_sound.play()

class MainMenu(Menu):
    def __init__(self):
        super(MainMenu, self).__init__('Astraea')

        self.items.append(MenuItem('New Game', 240, begin_game))
        self.items.append(MenuItem('Instructions', 200, 
                                   begin_instructions_menu))
        self.items.append(MenuItem('Options', 160, begin_options_menu))
        self.items.append(MenuItem('Quit', 120, sys.exit))
        self.reset()

class OptionsMenu(Menu):
    def __init__(self):
        super(OptionsMenu, self).__init__('Options')

        self.items.append(DifficultyMenuItem(280))
        def set_enable_sound(value):
            global enable_sound
            enable_sound = value
        self.items.append(ToggleMenuItem('Sound', enable_sound, 240,
                                         set_enable_sound))

        def set_enable_fullscreen(value):
            win.set_fullscreen(value, width=ARENA_WIDTH, height=ARENA_HEIGHT)
        self.items.append(ToggleMenuItem('Fullscreen', win.fullscreen, 200,
                                         set_enable_fullscreen))
                                
        self.items.append(ToggleMenuItem('Vsync', win.vsync, 160, 
                                         win.set_vsync))

        def set_show_fps(value):
            global show_fps
            show_fps = value
        self.items.append(ToggleMenuItem('FPS', show_fps, 120, set_show_fps))
        self.items.append(MenuItem('Ok', 60, begin_main_menu))
        self.reset()

class InstructionsMenu(Menu):
    def __init__(self):
        super(InstructionsMenu, self).__init__('Instructions')

        self.items.append(MenuItem('Ok', 50, begin_main_menu))
        self.reset()

        self.instruction_text = pyglet.text.Label(INSTRUCTIONS,
                                                  font_name=FONT_NAME,
                                                  font_size=14,
                                                  x=20, y=300,
                                                  width=ARENA_WIDTH - 40,
                                                  anchor_y='top',
                                                  multiline=True)

    def draw(self):
        super(InstructionsMenu, self).draw()
        self.instruction_text.draw()

class PauseMenu(Menu):
    def __init__(self):
        super(PauseMenu, self).__init__('Paused')

        self.items.append(MenuItem('Continue Game', 240, resume_game))
        self.items.append(MenuItem('Main Menu', 200, end_game))
        self.reset()

# --------------------------------------------------------------------------
# Game state functions
# --------------------------------------------------------------------------

def check_collisions():
    # Check for collisions using an approximate uniform grid.
    #
    #   1. Mark all grid cells that the bullets are in
    #   2. Mark all grid cells that the player is in
    #   3. For each asteroid, check grid cells that are covered for
    #      a collision.
    #
    # This is by no means perfect collision detection (in particular,
    # there are rounding errors, and it doesn't take into account the
    # arena wrapping).  Improving it is left as an exercise for the
    # reader.

    # The collision grid.  It is recreated each iteration, as bullets move
    # quickly.
    hit_squares = {}

    # 1. Mark all grid cells that the bullets are in.  Assume bullets
    #    occupy a single cell.
    for bullet in bullets:
        hit_squares[int(bullet.x / COLLISION_RESOLUTION), 
                    int(bullet.y / COLLISION_RESOLUTION)] = bullet

    # 2. Mark all grid cells that the player is in.
    for x, y in player.collision_cells():
        hit_squares[x, y] = player

    # 3. Check grid cells of each asteroid for a collision.
    for asteroid in asteroids:
        for x, y in asteroid.collision_cells():
           if (x, y) in hit_squares:
                asteroid.hit = True
                hit_squares[x, y].hit = True
                del hit_squares[x, y]

def begin_main_menu():
    set_overlay(MainMenu())
    
def begin_options_menu():
    set_overlay(OptionsMenu())

def begin_instructions_menu():
    set_overlay(InstructionsMenu())

def begin_game():
    global player_lives
    global score
    player_lives = 3
    score = 0

    begin_clear_background()
    set_overlay(Banner('Get Ready', begin_first_round, GET_READY_DELAY))

def begin_first_round(*args):
    player.reset()
    player.visible = True
    begin_round()

def next_round(*args):
    global in_game
    player.invincible = True
    in_game = False
    set_overlay(Banner('Get Ready', begin_round, GET_READY_DELAY))

def begin_round(*args):
    global asteroids
    global bullets
    global animations
    global in_game
    asteroids = []
    for i in range(INITIAL_ASTEROIDS[difficulty]):
        x = random.random() * ARENA_WIDTH
        y = random.random() * ARENA_HEIGHT
        asteroids.append(Asteroid(asteroid_sizes[-1], x, y, wrapping_batch))

    for bullet in bullets:
        bullet.delete()

    for animation in animations:
        animation.delete()

    bullets = []
    animations = []
    in_game = True
    set_overlay(None)
    pyglet.clock.schedule_once(begin_play, BEGIN_PLAY_DELAY)

def begin_play(*args):
    player.invincible = False

def begin_life(*args):
    player.reset()
    pyglet.clock.schedule_once(begin_play, BEGIN_PLAY_DELAY)
    
def life_lost(*args):
    global player_lives
    player_lives -= 1

    if player_lives > 0:
        begin_life()
    else:
        game_over()

def game_over():
    set_overlay(Banner('Game Over', end_game))

def pause_game():
    global paused
    paused = True
    set_overlay(PauseMenu())

def resume_game():
    global paused
    paused = False
    set_overlay(None)

def end_game():
    global in_game
    global paused
    paused = False
    in_game = False
    player.invincible = True
    pyglet.clock.unschedule(life_lost)
    pyglet.clock.unschedule(begin_play)
    begin_menu_background()
    set_overlay(MainMenu())

def set_overlay(new_overlay):
    global overlay
    if overlay:
        win.remove_handlers(overlay)
    overlay = new_overlay
    if overlay:
        win.push_handlers(overlay)

def begin_menu_background():
    global asteroids
    global bullets
    global animations
    global in_game
    global player_lives

    asteroids = []
    for i in range(11):
        x = random.random() * ARENA_WIDTH
        y = random.random() * ARENA_HEIGHT
        asteroids.append(Asteroid(asteroid_sizes[i // 4], x, y, wrapping_batch))

    for bullet in bullets:
        bullet.delete()

    for animation in animations:
        animation.delete()

    bullets = []
    animations = []
    in_game = False
    player_lives = 0
    player.visible = False

def begin_clear_background():
    global asteroids
    global bullets
    global animations

    for bullet in bullets:
        bullet.delete()

    for animation in animations:
        animation.delete()

    asteroids = []
    bullets = []
    animations = []
    player.visible = False

# --------------------------------------------------------------------------
# Create window
# --------------------------------------------------------------------------

win = pyglet.window.Window(ARENA_WIDTH, ARENA_HEIGHT, caption='Astraea')

@win.event
def on_key_press(symbol, modifiers):
    # Overrides default Escape key behaviour
    if symbol == KEY_PAUSE and in_game:
        if not paused:
            pause_game()
        else:
            resume_game()
        return True
    elif symbol == key.ESCAPE:
        sys.exit()
    return pyglet.event.EVENT_HANDLED

@win.event
def on_draw():
    glColor3f(1, 1, 1)

    # Render
    starfield.draw()

    for (x, y) in ((0, ARENA_HEIGHT),   # Top
                   (-ARENA_WIDTH, 0),   # Left
                   (0, 0),              # Center
                   (ARENA_WIDTH, 0),    # Right
                   (0, -ARENA_HEIGHT)): # Bottom
        glLoadIdentity()
        glTranslatef(x, y, 0)
        wrapping_batch.draw()

    glLoadIdentity()
    batch.draw()

    glLoadIdentity()

    if in_game:
        # HUD ship lives
        x = 10 + player.image.width // 2
        for i in range(player_lives - 1):
            player.image.blit(x, win.height - player.image.height // 2 - 10, 0)
            x += player.image.width + 10
        
        # HUD score
        score_text.text = str(score)
        score_text.draw()

    if overlay:
        overlay.draw()

    if show_fps:
        fps_display.draw()


# --------------------------------------------------------------------------
# Load resources
# --------------------------------------------------------------------------

batch = pyglet.graphics.Batch()
wrapping_batch = pyglet.graphics.Batch()

resource.path.append('res')
resource.reindex()

asteroid_sizes = [AsteroidSize('asteroid1.png', 100),
                  AsteroidSize('asteroid2.png', 50),
                  AsteroidSize('asteroid3.png', 10)]
for small, big in zip(asteroid_sizes[:-1], asteroid_sizes[1:]):
    big.next_size = small

bullet_image = resource.image('bullet.png')
center_anchor(bullet_image)

smoke_images_image = resource.image('smoke.png')
smoke_images = pyglet.image.ImageGrid(smoke_images_image, 1, 8)
for smoke_image in smoke_images:
    center_anchor(smoke_image)
smoke_animation = \
    pyglet.image.Animation.from_image_sequence(smoke_images,
                                               SMOKE_ANIMATION_PERIOD,
                                               loop=False)

explosion_images_image = resource.image('explosion.png')
explosion_images = pyglet.image.ImageGrid(explosion_images_image, 2, 8)
explosion_images = explosion_images.get_texture_sequence()
for explosion_image in explosion_images:
    center_anchor(explosion_image)
explosion_animation = \
    pyglet.image.Animation.from_image_sequence(explosion_images,
                                               EXPLOSION_ANIMATION_PERIOD,
                                               loop=False)

pointer_image = resource.image('pointer.png')
pointer_image.anchor_x = pointer_image.width // 2
pointer_image.anchor_y = pointer_image.height // 2
pointer_image_flip = resource.image('pointer.png', flip_x=True)

explosion_sound = resource.media('explosion.wav', streaming=False)
bullet_sound = resource.media('bullet.wav', streaming=False)

starfield = Starfield(resource.image('starfield.jpg'))
player = Player(resource.image('ship.png'), wrapping_batch)
win.push_handlers(player)

# --------------------------------------------------------------------------
# Global game state vars
# --------------------------------------------------------------------------

overlay = None
in_game = False
paused = False
score = 0

difficulty = 2
show_fps = False
enable_sound = True

score_text = pyglet.text.Label('',
                               font_name=FONT_NAME,
                               font_size=18,
                               x=ARENA_WIDTH - 10, 
                               y=ARENA_HEIGHT - 10,
                               anchor_x='right',
                               anchor_y='top')

fps_display = pyglet.window.FPSDisplay(win)

bullets = []
animations = []

# --------------------------------------------------------------------------
# Game update
# --------------------------------------------------------------------------

def update(dt):
    if overlay:
        overlay.update(dt)

    if not paused:
        starfield.update(dt)

        player.update(dt)
        for asteroid in asteroids:
            asteroid.update(dt)
        for bullet in bullets[:]:
            bullet.update(dt)
        for animation in animations[:]:
            animation.update(dt)


    if not player.invincible:
        # Collide bullets and player with asteroids
        check_collisions()

        # Destroy asteroids that were hit
        for asteroid in [a for a in asteroids if a.hit]:
            animations.append(EffectSprite(smoke_animation,
                                           asteroid.x, asteroid.y, 
                                           asteroid.dx, asteroid.dy,
                                           batch=batch))
            asteroid.destroy()
            if enable_sound:
                explosion_sound.play()

        # Check if the player was hit 
        if player.hit:
            animations.append(EffectSprite(explosion_animation,
                                           player.x, player.y,
                                           player.dx, player.dy, 
                                           batch=batch))
            player.invincible = True
            player.visible = False
            pyglet.clock.schedule_once(life_lost, LIFE_LOST_DELAY)

        # Check if the area is clear
        if not asteroids:
            next_round()
pyglet.clock.schedule_interval(update, 1/60.)

# --------------------------------------------------------------------------
# Start game
# --------------------------------------------------------------------------

glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

begin_menu_background()
begin_main_menu()

pyglet.app.run()
