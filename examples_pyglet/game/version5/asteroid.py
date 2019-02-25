import pyglet, random, math
from game import asteroid, load, player, resources

# Set up a window
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

# Set up the two top labels
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Version 5: It's a Game!",
                                x=400, y=575, anchor_x='center', batch=main_batch)

# Set up the game over label offscreen
game_over_label = pyglet.text.Label(text="GAME OVER",
                                    x=400, y=-300, anchor_x='center',
                                    batch=main_batch, font_size=48)

counter = pyglet.clock.ClockDisplay()

player_ship = None
player_lives = []
score = 0
num_asteroids = 3
game_objects = []

# We need to pop off as many event stack frames as we pushed on
# every time we reset the level.
event_stack_size = 0


def init():
    global score, num_asteroids

    score = 0
    score_label.text = "Score: " + str(score)

    num_asteroids = 3
    reset_level(2)


def reset_level(num_lives=2):
    global player_ship, player_lives, game_objects, event_stack_size

    # Clear the event stack of any remaining handlers from other levels
    while event_stack_size > 0:
        game_window.pop_handlers()
        event_stack_size -= 1

    for life in player_lives:
        life.delete()

    # Initialize the player sprite
    player_ship = player.Player(x=400, y=300, batch=main_batch)

    # Make three sprites to represent remaining lives
    player_lives = load.player_lives(num_lives, main_batch)

    # Make some asteroids so we have something to shoot at 
    asteroids = load.asteroids(num_asteroids, player_ship.position, main_batch)

    # Store all objects that update each frame in a list
    game_objects = [player_ship] + asteroids

    # Add any specified event handlers to the event handler stack
    for obj in game_objects:
        for handler in obj.event_handlers:
            game_window.push_handlers(handler)
            event_stack_size += 1


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()
    counter.draw()


def update(dt):
    global score, num_asteroids

    player_dead = False
    victory = False

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

    # Check for win condition
    asteroids_remaining = 0

    for obj in game_objects:
        obj.update(dt)

        to_add.extend(obj.new_objects)
        obj.new_objects = []

        # Check for win condition
        if isinstance(obj, asteroid.Asteroid):
            asteroids_remaining += 1

    if asteroids_remaining == 0:
        # Don't act on victory until the end of the time step
        victory = True

    # Get rid of dead objects
    for to_remove in [obj for obj in game_objects if obj.dead]:
        if to_remove == player_ship:
            player_dead = True
        # If the dying object spawned any new objects, add those to the 
        # game_objects list later
        to_add.extend(to_remove.new_objects)

        # Remove the object from any batches it is a member of
        to_remove.delete()

        # Remove the object from our list
        game_objects.remove(to_remove)

        # Bump the score if the object to remove is an asteroid
        if isinstance(to_remove, asteroid.Asteroid):
            score += 1
            score_label.text = "Score: " + str(score)

    # Add new objects to the list
    game_objects.extend(to_add)

    # Check for win/lose conditions
    if player_dead:
        # We can just use the length of the player_lives list as the number of lives
        if len(player_lives) > 0:
            reset_level(len(player_lives) - 1)
        else:
            game_over_label.y = 300
    elif victory:
        num_asteroids += 1
        player_ship.delete()
        score += 10
        reset_level(len(player_lives))


if __name__ == "__main__":
    # Start it up!
    init()

    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
