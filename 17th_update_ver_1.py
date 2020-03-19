
import arcade
import os

TILE_SCALING = 1
PLAYER_SCALING = 1
PLAYER_START_X = 100
PLAYER_START_Y = 100
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 30

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "17-TH UPDATE"
SPRITE_PIXEL_SIZE = 32

VIEWPORT_MARGIN_TOP = 60
VIEWPORT_MARGIN_BOTTOM = 60
VIEWPORT_RIGHT_MARGIN = 270
VIEWPORT_LEFT_MARGIN = 270

# Physics
MOVEMENT_SPEED = 5
JUMP_SPEED = 23
GRAVITY = 1.1
UPDATES_PER_FRAME = 7
CHARACTER_SCALING = 1

RIGHT_FACING = 0
LEFT_FACING = 1



class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)


        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)


        self.player_list = None
        self.player = None
        
        self.setup()
        


    def setup(self):
        
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedWalkingSprite()
        self.player_list.append(self.player)
        

        main_path = "sprites/player/adventurer"

        self.player.stand_right_textures = []
        for i in range(4):
            self.player.stand_right_textures.append(arcade.load_texture(f"{main_path}-idle-{i}.png"))

        self.player.stand_left_textures = []
        for i in range(4):
            self.player.stand_left_textures.append(arcade.load_texture(f"{main_path}-idle-{i}.png", mirrored=True))

        self.player.run_right_texture = []
        for i in range(6):
            self.player.run_right_texture.append(arcade.load_texture(f"{main_path}-run-{i}.png"))

        self.player.run_left_texture = []
        for i in range(6):
            self.player.run_left_texture.append(arcade.load_texture(f"{main_path}-run-{i}.png", mirrored=True))

        self.player.jump_right_texture = []
        for i in range(4):
            self.player.jump_right_texture.append(arcade.load_texture(f"{main_path}-jump-{i}.png"))

        self.player.jump_left_texture = []
        for i in range(4):
            self.player.jump_left_texture.append(arcade.load_texture(f"{main_path}-jump-{i}.png", mirrored=True))

        self.player.cast_right_texture = []
        for i in range(4):
            self.player.cast_right_texture.append(arcade.load_texture(f"{main_path}-cast-{i}.png"))

        self.player.cast_left_texture = []
        for i in range(4):
            self.player.cast_left_texture.append(arcade.load_texture(f"{main_path}-cast-{i}.png", mirrored=True))

        self.player.attack_right_texture = []
        for i in range(5):
            self.player.attack_right_texture.append(arcade.load_texture(f"{main_path}-swordAttack-{i}.png"))

        self.player.attack_left_texture = []
        for i in range(5):
            self.player.attack_left_texture.append(arcade.load_texture(f"{main_path}-swordAttack-{i}.png", mirrored=True))

        self.player.die_right_texture = []
        for i in range(7):
            self.player.die_right_texture.append(arcade.load_texture(f"{main_path}-die-{i}.png"))

        self.player.die_left_texture = []
        for i in range(7):
            self.player.die_left_texture.append(arcade.load_texture(f"{main_path}-die-{i}.png", mirrored=True))

        self.player.scale = 0.5
        self.player.center_x = SCREEN_WIDTH // 2
        self.player.center_y = SCREEN_HEIGHT // 2

        self.player_list.append(self.player)



    def on_draw(self):

        arcade.start_render()

        self.player_list.on_draw()


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key ==arcade.key.RIGHT or arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
    
    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0
    

    def update(self, delta_time):
        self.player_list.update_animation()

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()