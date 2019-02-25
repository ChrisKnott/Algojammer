import pyglet
from . import physicalobject, resources


class Bullet(physicalobject.PhysicalObject):
    """Bullets fired by the player"""

    def __init__(self, *args, **kwargs):
        super(Bullet, self).__init__(resources.bullet_image, *args, **kwargs)

        # Bullets shouldn't stick around forever
        pyglet.clock.schedule_once(self.die, 0.5)

        # Flag as a bullet
        self.is_bullet = True

    def die(self, dt):
        self.dead = True
