"""
Racing Game
"""
import arcade
import os
import math
import random


# Constants
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Racing Game"
MOVEMENT_SPEED = 3
SCALE = 0.5

OFFSCREEN_SPACE = 50
LEFT_LIMIT = -OFFSCREEN_SPACE
RIGHT_LIMIT = SCREEN_WIDTH + OFFSCREEN_SPACE
BOTTOM_LIMIT = -OFFSCREEN_SPACE
TOP_LIMIT = SCREEN_HEIGHT + OFFSCREEN_SPACE

STARTING_OBJECTS_COUNT = 5
OBJECTS_SPEED = 4

SPRITE_SCALING_COIN = 0.2
COIN_COUNT = 3

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 0.15
TILE_SCALING = 1.6
COIN_SCALING = 0.5

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 5


class VehicleSprite(arcade.Sprite):
    """ 
    Vehicle class 
    Sprite that represents our Vehicle.
    """

    def __init__(self, image, scale):
        """ Set up the Vehicle """

        # Call the parent init
        super().__init__(image, scale)

        # Create a variable to hold our speed. 'angle' is created by the parent
        # The put vehicle to init position
        self.speed = 0
        self.max_speed = 5
        self.respawning = 0
        
        # Mark that we are respawning.
        self.respawn()
        
    def respawn(self):
        """
        Called when we die and need to make a new vehicle.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        self.center_x = SCREEN_WIDTH / 2
        self.center_y = SCREEN_HEIGHT / 2

    def update(self):
        
        # Acceleration
        if self.speed  > self.max_speed :
            self.speed = self.max_speed
        self.change_y = self.change_y + self.speed
                
        #print("X: %s" % self.change_x)
        #print("Y: %s" % self.change_y)
        self.center_x += self.change_x
        self.center_y += self.change_y
        
        # DEBUG:
        # See if the obj hit the edge of the screen. 
        # If so, change direction
        if self.center_x < 250:
            self.center_x = 250
        if self.center_x > SCREEN_WIDTH - 250:
            self.center_x = SCREEN_WIDTH - 250
        if self.center_y < 1:
            self.center_y = 1
        if self.center_y > SCREEN_HEIGHT - 1:
            self.center_y = SCREEN_HEIGHT - 1
        
        """ Call the parent class. """
        super().update()        

        

class OthersSprite(arcade.Sprite):
    """ Sprite that represents a competitors"""
    
    def __init__(self, image, scale):
        super().__init__(image, scale=scale)
        self.size = 0

    def update(self):
        """ Move the object around. """
        super().update()
        if self.center_y > TOP_LIMIT:
            self.center_y = BOTTOM_LIMIT
        if self.center_y < BOTTOM_LIMIT:
            self.center_y = TOP_LIMIT
        if self.center_x < 250:
            self.change_x = random.random() * OBJECTS_SPEED 
            self.center_x = 250
        if self.center_x > SCREEN_WIDTH - 250:
            self.center_x = SCREEN_WIDTH - 250
            self.change_x = (random.random() * OBJECTS_SPEED) * -1
        
class Coin(arcade.Sprite):
    """
    This class represents the coins on our screen. 
    """

    def reset_pos(self):

        # Reset the coin to a random spot above the screen
        self.center_y = random.randrange(BOTTOM_LIMIT,
                                         TOP_LIMIT)
        self.center_x = random.randrange(250, SCREEN_WIDTH-250)

    def update(self):

        # Move the coin
        self.center_y -= 1

        # See if the coin has fallen off the bottom of the screen.
        # If so, reset it.
        if self.top < 0:
            self.reset_pos()

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
        self.gameover = None
        self.score = None
        self.lives = None
        self.collision_time = None
        self.numobj = None
        self.ncoins = None
        
        # All Sprites
        self.all_sprites_list = None

        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        self.background = None
        
        self.coin_list = None
        self.wall_list = None
        self.player_list = None
        self.myobject_list = None
        self.coin_list = None

        # Separate variable that holds the player sprite
        self.player_sprite = None

        # Our physics engine
        self.physics_engine = None

    # Make the enemies
    def create_buddies(self):
        image_list = ("images\\carcar.png",
                     "images\\carcar.png",
                     "images\\carcar.png",
                     "images\\carcar.png")
        
        for i in range(STARTING_OBJECTS_COUNT):
            image_no = random.randrange(4)
            enemy_sprite = OthersSprite(image_list[image_no], CHARACTER_SCALING)
            enemy_sprite.guid = "Competitors"
        
            enemy_sprite.center_y = random.randrange(BOTTOM_LIMIT, TOP_LIMIT)
            enemy_sprite.center_x = random.randrange(LEFT_LIMIT, RIGHT_LIMIT)
        
            if(random.random()%2):
                enemy_sprite.change_x = random.random() * OBJECTS_SPEED - 1
                enemy_sprite.change_y = random.random() * OBJECTS_SPEED - 1
            else:
                enemy_sprite.change_x = random.random() * OBJECTS_SPEED + 1
                enemy_sprite.change_y = random.random() * OBJECTS_SPEED + 1
        
            #enemy_sprite.change_angle = (random.random() - 0.5) * 2
            enemy_sprite.size = 4
            
            enemy_sprite.color = arcade.color.RED
            enemy_sprite.angle = 90
            
            self.all_sprites_list.append(enemy_sprite)
            self.myobject_list.append(enemy_sprite)      
            
            
    # Make treasure
    def create_treasure(self):
        for i in range(COIN_COUNT):
            # Create the coin instance
            # Coin image from kenney.nl
            coin_sprite = Coin("images/coin_01.png", SPRITE_SCALING_COIN)
    
            # Position the coin
            coin_sprite.center_x = random.randrange(SCREEN_WIDTH)
            coin_sprite.center_y = random.randrange(SCREEN_HEIGHT)
            
            # move it down the road
            coin_sprite.change_y -= 1
    
            # Add the coin to the lists
            self.all_sprites_list.append(coin_sprite)
            self.coin_list.append(coin_sprite)    
            
    def game_over(self):
        
        # doing something
        if self.gameover:
            self.background = arcade.load_texture("images/thereal.png")
            return
        
        # And now restart game from the begin
        self.setup()
        

    def setup(self):
        """ Set up the game here. Call this function to restart the game. """
        
        self.total_time = 0.0

        self.background = arcade.load_texture("images/backgroundRoad.npg")
        #self.background = arcade.load_texture("images/background.jpg")
        # Create the Sprite lists
        self.all_sprites_list = arcade.SpriteList()
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.myobject_list = arcade.SpriteList()
        
        # Set up the player
        self.gameover = 0
        self.score = 0
        self.lives = 3
        self.collision_time = 0
        self.numobj = STARTING_OBJECTS_COUNT
        self.ncoins = COIN_COUNT
        self.player_sprite = VehicleSprite("images/carcar.png",
                                            CHARACTER_SCALING)
        self.player_sprite.angle = 90
        #self.player_sprite.change_y = 1        
        self.all_sprites_list.append(self.player_sprite)
        
        self.create_buddies()
        self.create_treasure()
        
        # Make the mouse disappear when it is over the window.
        # So we just see our object, not the pointer.
        self.set_mouse_visible(False)

        # Set the background color
        arcade.set_background_color(arcade.color.ASH_GREY)
        

        # Set up the player, specifically placing it at these coordinates.
        #self.player_sprite = arcade.Sprite("images\\carcar.png", CHARACTER_SCALING)
        #self.player_sprite.center_x = 500
        #self.player_sprite.center_y = 110
        #self.player_sprite.angle = 90
        #self.player_sprite.change_y = 1
        #self.player_list.append(self.player_sprite)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, 
                                                         self.wall_list)

        # Set the viewport boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0
        
        # For draw
        self.line_start = 0        

    def on_draw(self):
        """ Render the screen. """

        # Clear the screen to the background color
        arcade.start_render()

        for x in range (0, 1) :
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 
                                    (SCREEN_HEIGHT // 2) - x - self.line_start,
                                    SCREEN_WIDTH, 
                                    SCREEN_HEIGHT, self.background-1_0)
            arcade.draw_texture_rectangle(SCREEN_WIDTH // 2, 
                                    (SCREEN_HEIGHT) - x - self.line_start,
                                    SCREEN_WIDTH, 
                                    SCREEN_HEIGHT, self.background)
                

        # Draw our sprites
        self.all_sprites_list.draw()         

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

        # Print Score
        output = f"Score: {self.score:05d}"
        arcade.draw_text(output, 10 + self.view_left, 45 + self.view_bottom,
                         arcade.color.AZURE, 24)

        # Print Lives
        output = f"Lives: {self.lives:01d}"
        arcade.draw_text(output, 10 + self.view_left, 75 + self.view_bottom,
                         arcade.color.RED, 24)

        
    def on_key_press(self, key, modifiers):
        """ Called whenever the user presses a key. """
        if key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED
        elif key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.SPACE:
            self.player_sprite.speed = self.player_sprite.speed + 1
        elif key == arcade.key.ESCAPE:
            self.gameover = 0   
            if self.gameover:
                self.gameover = 0            
                self.setup()
        
    
    def on_key_release(self, key, modifiers):
        """ Called whenever a user releases a key. """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0
        elif key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0    
        elif key == arcade.key.SPACE:
            self.player_sprite.speed = 0            
        elif key == arcade.key.ESCAPE:
            if self.gameover:
                self.gameover = 0            
                self.setup()


    def on_mouse_press(self, x, y, button, modifiers):
        """
        Called when the user presses a mouse button.
        """
        # DEBUG: print(f"You clicked button number: {button}")
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.color = arcade.color.BLACK

    def on_mouse_release(self, x, y, button, modifiers):
        """
        Called when a user releases a mouse button.
        """
        if button == arcade.MOUSE_BUTTON_LEFT:
            self.player_sprite.color = arcade.color.AUBURN

    def update(self, delta_time):
        
        """ Movement and game logic """
        
        if self.gameover:
            return
        
        self.all_sprites_list.update()    

        # Game Clock
        self.total_time += delta_time
        
        # flick if it was collision
        if self.collision_time:
            if self.collision_time % 2 :
                self.player_sprite.color = arcade.color.AMAZON
            else:
                self.player_sprite.color = arcade.color.WHITE
            
        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        #self.physics_engine.update()
        
        # Generate a list of all enemies that collided with the player.
        ene_hit_list = arcade.check_for_collision_with_list(self.player_sprite, 
                                                        self.myobject_list)
        
        # Loop through each colliding sprite, remove it, and add to the score.
        for myobject in ene_hit_list:
            myobject.remove_from_sprite_lists()
            self.numobj -= 1
            self.lives -= 1
            self.collision_time = 50
            self.player_sprite.color = arcade.color.AMAZON
        if(self.numobj < 1):
            self.numobj = STARTING_OBJECTS_COUNT
            self.create_buddies()
            
        if self.lives < 1:
            self.gameover = 1
            self.game_over()

        # Generate a list of coins that collided with the player.
        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, 
                                                            self.coin_list)
        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score += 10
            self.ncoins -= 1
        if self.ncoins < 1:
            self.ncoins = COIN_COUNT
            self.create_treasure()

        
        # --- Manage Scrolling ---

        if self.line_start == SCREEN_HEIGHT // 2:
            self.line_start = 0
        else:
            self.line_start = self.line_start + 1        



def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
