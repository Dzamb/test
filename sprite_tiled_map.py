
import arcade
import os
import time

TILE_SCALING = 0.5
PLAYER_SCALING = 1

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Sprite Tiled Map Example"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 23
GRAVITY = 1.1
UPDATES_PER_FRAME = 3
CHARACTER_SCALING = 1

RIGHT_FACING = 0
LEFT_FACING = 1

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING

        self.cur_texture = 0
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.scale = CHARACTER_SCALING

        # self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

        main_path = "sprites/player/adventurer"

        self.idle_texture = load_texture_pair(f"{main_path}-idle-0.png")
        self.idle_textures = []
        for i in range(16):
            texture = load_texture_pair(f"{main_path}-idle-{i}.png")
            self.idle_textures.append(texture)

        self.run_textures = []
        for i in range(6):
            texture = load_texture_pair(f"{main_path}-run-{i}.png")
            self.run_textures.append(texture)

        # self.jump_textures = []
        # for i in range(4):
        #     texture = load_texture_pair(f"{main_path}-jump-{i}.png")
        #     self.jump_textures.append(texture)
        
        # self.cast_textures = []
        # for i in range(4):
        #     texture = load_texture_pair(f"{main_path}-cast-{i}.png")
        #     self.cast_textures.append(texture)
        
        # self.attack_textures = []
        # for i in range(5):
        #     texture = load_texture_pair(f"{main_path}-swordAttack-{i}.png")
        #     self.attack_textures.append(texture)

        # self.die_textures = []
        # for i in range(7):
        #     texture = load_texture_pair(f"{main_path}-die-{i}.png")
        #     self.die_textures.append(texture)
        
        self.texture = self.idle_texture[0]

    def update_animation(self, delta_time):
        # pass
        if self.change_x == 0:
            self.cur_texture += 1
            if self.cur_texture > 14:
                self.cur_texture = 0
            
            self.texture = self.idle_textures[self.cur_texture][self.character_face_direction]

        
        # if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
        #     self.character_face_direction = LEFT_FACING
        # elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
        #     self.character_face_direction = RIGHT_FACING

        # if self.change_y > 0:
        #     self.texture = self.jump_textures[]
        #     return
        # #* анимация стояния
        # self.cur_texture += 1
        # if self.cur_texture > 3 * UPDATES_PER_FRAME:
        #     self.cur_texture = 0
        # self.texture = self.idle_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        #* анимация бега
        # self.cur_texture += 1
        # if self.cur_texture > 5:
        #     self.cur_texture = 0
        # self.texture = self.run_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        # #* анимация прыжка
        # self.cur_texture += 1
        # if self.cur_texture > 3 * UPDATES_PER_FRAME:
        #     self.cur_texture = 0
        # self.texture = self.jump_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        # #* анимация каста
        # self.cur_texture += 1
        # if self.cur_texture > 3 * UPDATES_PER_FRAME:
        #     self.cur_texture = 0
        # self.texture = self.cast_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        # #* анимация атаки
        # self.cur_texture += 1
        # if self.cur_texture > 4 * UPDATES_PER_FRAME:
        #     self.cur_texture = 0
        # self.texture = self.attack_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        # #* анимация смерти
        # self.cur_texture += 1
        # if self.cur_texture > 6 * UPDATES_PER_FRAME:
        #     self.cur_texture = 0
        # self.texture = self.die_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]



class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self):
        """
        Initializer
        """
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Sprite lists
        self.wall_list = None
        self.player_list = None
        # self.coin_list = None

        # Set up the player
        self.score = 0
        self.player = None

        self.physics_engine = None
        self.view_left = 0
        self.view_bottom = 0
        self.end_of_map = 0
        self.game_over = False
        self.last_time = None
        self.frame_count = 0
        self.fps_message = None
        self.background = None

    def setup(self):
        """ Set up the game and initialize the variables. """

        self.background = arcade.load_texture("sprites/background.png")

        # Sprite lists
        self.player_list = arcade.SpriteList()
        # self.coin_list = arcade.SpriteList()

        self.player = PlayerCharacter()

        self.player.center_x = 196
        self.player.center_y = 270
        self.player.scale = 1

        self.player_list.append(self.player)

        # Set up the player
        # self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
        #                                    PLAYER_SCALING)

        # Starting position of the player
        # self.player_sprite.center_x = 196
        # self.player_sprite.center_y = 270
        # self.player_list.append(self.player_sprite)

        # map_name = ":resources:/tmx_maps/map.tmx"
        map_name = "test4.tmx"


        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # --- Platforms ---
        self.wall_list = arcade.tilemap.process_layer(my_map, 'ground', 1)

    
        # Keep player from running through the wall_list layer
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.game_over = False

    def on_draw(self):
        """
        Render the screen.
        """
        # scale = SCREEN_WIDTH / self.background.width
        # arcade.draw_lrwh_rectangle_textured(0, 0,
        #                                     SCREEN_WIDTH, SCREEN_HEIGHT,
        #                                     self.background)


        self.frame_count += 1

        # This command has to happen before we start drawing
        arcade.start_render()

        scale = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            4800, 1280,
                                            self.background)


        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        # self.coin_list.draw()

        # if self.last_time and self.frame_count % 60 == 0:
        #     fps = 1.0 / (time.time() - self.last_time) * 60
        #     self.fps_message = f"FPS: {fps:5.0f}"

        # if self.fps_message:
        #     arcade.draw_text(self.fps_message, self.view_left + 10, self.view_bottom + 40, arcade.color.BLACK, 14)

        # if self.frame_count % 60 == 0:
        #     self.last_time = time.time()

        # Put the text on the screen.
        # Adjust the text position based on the view port so that we don't
        # scroll the text too.
        distance = self.player.right
        output = f"Distance: {distance}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcade.color.BLACK, 14)
        print("HERE")
        if self.game_over:
            arcade.draw_text("Game Over", self.view_left + 200, self.view_bottom + 200, arcade.color.BLACK, 30)

    def on_key_press(self, key, modifiers):
        """
        Called whenever the mouse moves.
        """
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player.change_y = JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        """
        Called when the user presses a mouse button.
        """
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def on_update(self, delta_time):
        """ Movement and game logic """

        self.player_list.update_animation(delta_time)

        if self.player.right >= self.end_of_map:
            self.game_over = True

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        if not self.game_over:
            self.physics_engine.update()

        # coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        # for coin in coins_hit:
        #     coin.remove_from_sprite_lists()
        #     self.score += 1

        # --- Manage Scrolling ---

        # Track if we need to change the view port

        changed = False

        # Scroll left
        left_bndry = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player.left < left_bndry:
            self.view_left -= left_bndry - self.player.left
            changed = True

        # Scroll right
        right_bndry = self.view_left + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player.right > right_bndry:
            self.view_left += self.player.right - right_bndry
            changed = True

        # Scroll up
        top_bndry = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN_TOP
        if self.player.top > top_bndry:
            self.view_bottom += self.player.top - top_bndry
            changed = True

        # Scroll down
        bottom_bndry = self.view_bottom + VIEWPORT_MARGIN_BOTTOM
        if self.player.bottom < bottom_bndry:
            self.view_bottom -= bottom_bndry - self.player.bottom
            changed = True

        # If we need to scroll, go ahead and do it.
        if changed:
            self.view_left = int(self.view_left)
            self.view_bottom = int(self.view_bottom)
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()
