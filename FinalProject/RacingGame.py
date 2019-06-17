"""
Racing Game
"""
import arcade
import os

# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Racing Game"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.4
TILE_SCALING = 1.6
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5
VIEWPORT_MARGIN = 500


class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        self.total_time = 0.0

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.background = None

        self.coin_list = None
        self.wall_list = None
        self.player_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        self.total_time = 0.0

        self.background = arcade.load_texture("images/backgroundRoad.png")

        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()

        # Set up the player, specifically placing it at these coordinates.
        self.player_sprite = arcade.Sprite("images/player.png", CHARACTER_SCALING)
        self.player_sprite.center_x = 500
        self.player_sprite.center_y = 110
        self.player_sprite.angle = 90
        self.player_sprite.change_y = 1
        self.player_list.append(self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.wall_list)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                                      SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        # Draw our sprites

        # Calculate minutes
        minutes = int(self.total_time) // 60

        # Calculate seconds by using a modulus (remainder)
        seconds = int(self.total_time) % 60

        # Figure out our output
        output = f"Time: {minutes:02d}:{seconds:02d}"

        # Output the timer text.
        arcade.draw_text(output, 10 + self.view_left, 10 + self.view_bottom,
                         arcade.color.BLACK, 24)
        arcade.draw_text(output, 12 + self.view_left, 12 + self.view_bottom,
                         arcade.color.WHITE_SMOKE, 24)

        self.wall_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.update()

        self.total_time += delta_time

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        self.physics_engine.update()

        # --- Manage Scrolling ---

        # Track if we need to change the viewport

        changed = False

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_bndry:
            self.view_bottom += self.player_sprite.top - top_bndry
            changed = True

        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
