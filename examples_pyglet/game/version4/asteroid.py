import pyglet, random, math
from game import load, player, resources

# Set up a window
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

# Set up the two top labels
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Version 4: Bullets and Structure",
                                x=400, y=575, anchor_x='center', batch=main_batch)

# Initialize the player sprite
player_ship = player.Player(x=400, y=300, batch=main_batch)

# Make three sprites to represent remaining lives
player_lives = load.player_lives(2, main_batch)

# Make three asteroids so we have something to shoot at 
asteroids = load.asteroids(3, player_ship.position, main_batch)

# Store all objects that update each frame in a list
game_objects = [player_ship] + asteroids

# Add any specified event handlers to the event handler stack
for obj in game_objects:
    for handler in obj.event_handlers:
        game_window.push_handlers(handler)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    # To avoid handling collisions twice, we employ nested loops of ranges.
    # This method also avoids the problem of colliding an object with itself.
    for i in range(len(game_objects)):
        for j in range(i + 1, len(game_objects)):

            obj_1 = game_objects[i]
            obj_2 = game_objects[j]

            # Make sure the objects haven't already been killed
            if not obj_1.dead and not obj_2.dead:
                if obj_1.collides_with(obj_2):
                    obj_1.handle_collision_with(obj_2)
                    obj_2.handle_collision_with(obj_1)

    # Let's not modify the list while traversing it
    to_add = []

    for obj in game_objects:
        obj.update(dt)
        to_add.extend(obj.new_objects)
        obj.new_objects = []

    # Get rid of dead objects
    for to_remove in [obj for obj in game_objects if obj.dead]:
        # If the dying object spawned any new objects, add those to the game_objects list later
        to_add.extend(obj.new_objects)

        # Remove the object from any batches it is a member of
        to_remove.delete()

        # Remove the object from our list
        game_objects.remove(to_remove)

    # Add new objects to the list
    game_objects.extend(to_add)


if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
