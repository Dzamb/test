import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "17-th update"

# PLAYER_MOVEMENT_SPEED = 5
PLAYER_MOVEMENT_SPEED = 7
GRAVITY = 1.5
PLAYER_JUMP_SPEED = 15

CHARACTER_SCALING = 1

SPRITE_PIXEL_SIZE = 128
TILE_SCALING = 0.5
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

LEFT_VIEWPORT_MARGIN = 200
RIGHT_VIEWPORT_MARGIN = 200
BOTTOM_VIEWPORT_MARGIN = 150
TOP_VIEWPORT_MARGIN = 100

RIGHT_FACING = 0
LEFT_FACING = 1





class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)


        self.player_list = None
        self.player = None

        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False



#!============================================================================================
        # These are 'lists' that keep track of our sprites. Each sprite should
        # go into a list.
        # self.coin_list = None
        self.wall_list = None
        # self.background_list = None
        # self.ladder_list = None
        # self.player_list = None
        self.physics_engine = None

        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
#!============================================================================================



#! 00000000000000000000
# Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        self.idle_textures = []
        for i in range(15):
            right_idle_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightIdle_strip.png", x=i*64, y=0, width=64, height=64)
            self.idle_textures.append(right_idle_texture)
            left_idle_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightIdle_strip.png", x=i*64, y=0, width=64, height=64, mirrored=True)
            self.idle_textures.append(left_idle_texture)

        self.jump_textures = []
        for i in range(14):
            right_jump_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightJumpAndFall_strip.png", x=i*144, y=0, width=144, height=64)
            self.jump_textures.append(right_jump_texture)
            left_jump_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightJumpAndFall_strip.png", x=i*144, y=0, width=144, height=64, mirrored=True)
            self.jump_textures.append(left_jump_texture)

        self.fall_textures = []
        for i in range(14):
            right_fall_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightJumpAndFall_strip.png", x=i*144, y=0, width=144, height=64)
            self.fall_textures.append(right_fall_texture)
            left_fall_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightJumpAndFall_strip.png", x=i*144, y=0, width=144, height=64, mirrored=True)
            self.fall_textures.append(left_fall_texture)

        self.walk_textures = []
        for i in range(8):
            right_walk_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightRun_strip.png", x=i*64, y=0, width=64, height=64)
            self.walk_textures.append(right_walk_texture)
            left_walk_texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightRun_strip.png", x=i*64, y=0, width=64, height=64, mirrored=True)
            self.walk_textures.append(left_walk_texture)

        # Load textures for climbing
        self.climbing_textures = []
        texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightIdle_strip.png")
        self.climbing_textures.append(texture)
        texture = arcade.load_texture("sprites/player/Knight/noBKG_KnightIdle_strip.png")
        self.climbing_textures.append(texture)

        # Set the initial texture
        self.texture = self.idle_textures[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        # self.set_hit_box(self.texture.hit_box_points)
#! 00000000000000000000



        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedTimeSprite()
        self.player.textures = []

#! 111111111111111111111
        self.change_x = 50
        self.change_y = 50

# Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing and abs(self.change_y) > 1:
            self.cur_texture += 1
            if self.cur_texture > 7:
                self.cur_texture = 0
        if self.climbing:
            self.texture = self.climbing_textures[self.cur_texture // 4]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_textures[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_textures[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_textures[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture += 1
        if self.cur_texture > 7:
            self.cur_texture = 0
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]
#! 111111111111111111111





        #!===================================================================

        self.wall_list = arcade.SpriteList()

        self.view_bottom = 0
        self.view_left = 0

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        moving_platforms_layer_name = 'Moving Platforms'

        # Name of the layer that has items for pick-up
        # coins_layer_name = 'Coins'

        # Map name
        map_name = f":resources:tmx_maps/map_with_ladders.tmx"

        # Read in the tiled map
        my_map = arcade.tilemap.read_tmx(map_name)

        # Calculate the right edge of the my_map in pixels
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, platforms_layer_name, TILE_SCALING)

        # -- Moving Platforms
        # moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer_name, TILE_SCALING)
        # for sprite in moving_platforms_list:
        #     self.wall_list.append(sprite)

        # -- Background objects
        self.background_list = arcade.tilemap.process_layer(my_map, "Background", TILE_SCALING)

        # -- Background objects
        # self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", TILE_SCALING)

        # -- Coins
        # self.coin_list = arcade.tilemap.process_layer(my_map, coins_layer_name, TILE_SCALING)

        # --- Other stuff
        # Set the background color
        if my_map.background_color:
            arcade.set_background_color(my_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY,
                                                             )   # ladders=self.ladder_list
        #!===================================================================











#!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  РОДНАЯ АНИМАЦИЯ  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        #* анимация стояния
        for i in range(15):
            self.player.textures.append(arcade.load_texture("sprites/player/knight/noBKG_KnightIdle_strip.png",
                                                                    x=i*64, y=0, width=64, height=64
                                                                    ))

        # for i in range():

        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_list.append(self.player)

    def on_draw(self):
        arcade.start_render()
        self.player_list.draw()
#!%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  КОНЕЦ РОДНОЙ АНИМАЦИИ  %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


#!+++++++++++++++++++++++++++++++++++++++++
        self.wall_list.draw()
        self.background_list.draw()
        # self.ladder_list.draw()
        # self.coin_list.draw()
        # self.player_list.draw()
#!+++++++++++++++++++++++++++++++++++++++++




    def on_update(self, delta_time):
        self.player_list.update()
        # self.player_list.update_animation()



#!================================
        self.physics_engine.update()

        # Update animations
        if self.physics_engine.can_jump():
            self.player.can_jump = False
        else:
            self.player.can_jump = True

        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player.is_on_ladder = True
            self.process_keychange()
        else:
            self.player.is_on_ladder = False
            self.process_keychange()

        # self.coin_list.update_animation(delta_time)
        self.background_list.update_animation(delta_time)
        self.player_list.update_animation(delta_time)

        # Update walls, used with moving platforms
        self.wall_list.update()

        # See if the moving wall hit a boundary and needs to reverse direction.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_x < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1

        # See if we hit any coins
        # coin_hit_list = arcade.check_for_collision_with_list(self.player,
        #                                                      self.coin_list)

        # Loop through each coin we hit (if any) and remove it
        # for coin in coin_hit_list:

        #     # Figure out how many points this coin is worth
        #     if 'Points' not in coin.properties:
        #         print("Warning, collected a coin without a Points property.")
        #     else:
        #         points = int(coin.properties['Points'])
        #         self.score += points

        #     # Remove the coin
        #     coin.remove_from_sprite_lists()
        #     arcade.play_sound(self.collect_coin_sound)

        # Track if we need to change the viewport
        changed_viewport = False

        # --- Manage Scrolling ---

        #Scroll left
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            changed_viewport = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed_viewport = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed_viewport = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed_viewport = True

        if changed_viewport:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
#!=================================









#!-------------------------------------------
    def process_keychange(self):
        """
        Called when we change a key up/down or we move on/off a ladder.
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVEMENT_SPEED

        # Process up/down when on a ladder and no movement
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()
#!-------------------------------------------







    # def on_key_press(self, key, modifiers):
    #     if key == arcade.key.UP or arcade.key.W:
    #         self.player.change_y = PLAYER_MOVEMENT_SPEED
    #     elif key == arcade.key.DOWN or arcade.key.S:
    #         self.player.change_y = -PLAYER_MOVEMENT_SPEED
    #     elif key == arcade.key.LEFT or arcade.key.A:
    #         self.player.change_x = -PLAYER_MOVEMENT_SPEED
    #     elif key ==arcade.key.RIGHT or arcade.key.D:
    #         self.player.change_x = PLAYER_MOVEMENT_SPEED
    
    # def on_key_release(self, key, modifiers):
    #     if key == arcade.key.UP or key == arcade.key.W:
    #         self.player.change_y = 0
    #     elif key == arcade.key.DOWN or key == arcade.key.S:
    #         self.player.change_y = 0
    #     elif key == arcade.key.LEFT or key == arcade.key.A:
    #         self.player.change_x = 0
    #     elif key == arcade.key.RIGHT or key == arcade.key.D:
    #         self.player.change_x = 0



def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()