import pyglet, random, math
from game import load, player, resources

# Set up a window
game_window = pyglet.window.Window(800, 600)

main_batch = pyglet.graphics.Batch()

# Set up the two top labels
score_label = pyglet.text.Label(text="Score: 0", x=10, y=575, batch=main_batch)
level_label = pyglet.text.Label(text="Version 2: Basic Motion",
                                x=400, y=575, anchor_x='center', batch=main_batch)

# Initialize the player sprite
player_ship = player.Player(x=400, y=300, batch=main_batch)

# Make three sprites to represent remaining lives
player_lives = load.player_lives(2, main_batch)

# Make three asteroids so we have something to shoot at 
asteroids = load.asteroids(3, player_ship.position, main_batch)

# Store all objects that update each frame in a list
game_objects = [player_ship] + asteroids

# Tell the main window that the player object responds to events
game_window.push_handlers(player_ship)


@game_window.event
def on_draw():
    game_window.clear()
    main_batch.draw()


def update(dt):
    for obj in game_objects:
        obj.update(dt)


if __name__ == "__main__":
    # Update the game 120 times per second
    pyglet.clock.schedule_interval(update, 1 / 120.0)

    # Tell pyglet to do its thing
    pyglet.app.run()
