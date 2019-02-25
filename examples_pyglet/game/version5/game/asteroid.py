import random
from . import physicalobject, resources


class Asteroid(physicalobject.PhysicalObject):
    """An asteroid that divides a little before it dies"""

    def __init__(self, *args, **kwargs):
        super(Asteroid, self).__init__(resources.asteroid_image, *args, **kwargs)

        # Slowly rotate the asteroid as it moves
        self.rotate_speed = random.random() * 100.0 - 50.0

    def update(self, dt):
        super(Asteroid, self).update(dt)
        self.rotation += self.rotate_speed * dt

    def handle_collision_with(self, other_object):
        super(Asteroid, self).handle_collision_with(other_object)

        # Superclass handles deadness already
        if self.dead and self.scale > 0.25:
            num_asteroids = random.randint(2, 3)
            for i in range(num_asteroids):
                new_asteroid = Asteroid(x=self.x, y=self.y, batch=self.batch)
                new_asteroid.rotation = random.randint(0, 360)
                new_asteroid.velocity_x = random.random() * 70 + self.velocity_x
                new_asteroid.velocity_y = random.random() * 70 + self.velocity_y
                new_asteroid.scale = self.scale * 0.5
                self.new_objects.append(new_asteroid)
