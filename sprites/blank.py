import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
SCREEN_TITLE = "17-th update"

PLAYER_MOVEMENT_SPEED = 5

CHARACTER_SCALING = 1





class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        self.player_list = None
        self.player = None
        self.physics_engine = None

        self.ground_list = None
        


    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = arcade.AnimatedTimeBasedSprite()


        #* тут прописываем физику поведения спрайтов персонажа и преград
        self.physics_engine = arcade.PhysicsEngineSimple("""дописать спрайты""")




    def on_draw(self):

        arcade.start_render()
    

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
        self.physics_engine.update()

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()