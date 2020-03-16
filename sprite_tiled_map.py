
import arcade
import os
import time

TILE_SCALING = 0.5
PLAYER_SCALING = 1
PLAYER_START_X = 196
PLAYER_START_Y = 200

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
UPDATES_PER_FRAME = 7
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

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        #* устанавливаем куда смотрит лицо по-умолчанию
        self.character_face_direction = RIGHT_FACING

        #* Переключение между последовательностями изображений
        self.cur_texture = 0
        self.scale = CHARACTER_SCALING

        #* Отслеживание наших состояний
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        # self.is_death = False

#!        self.points = [[-22, -64], [22, -64], [22, 28], [-22, 28]]

#*   ===Загрузка текстур===

        #* Указываем папку содержащую все изображения
        main_path = "sprites/player/adventurer"

        #* Загрузка текстур стояния для левого и правого состояния
        self.idle_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}-idle-{i}.png")
            self.idle_texture_pair.append(texture)

        #* Загрузка текстур бега для левого и правого состояния
        self.run_texture_pair = []
        for i in range(6):
            texture = load_texture_pair(f"{main_path}-run-{i}.png")
            self.run_texture_pair.append(texture)

        #* Загрузка текстур прыжка для левого и правого состояния
        self.jump_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}-jump-{i}.png")
            self.jump_texture_pair.append(texture)

        #* Загрузка текстур каста заклинания для левого и правого состояния
        self.cast_texture_pair = []
        for i in range(4):
            texture = load_texture_pair(f"{main_path}-cast-{i}.png")
            self.cast_texture_pair.append(texture)

        #* Загрузка текстур атаки мечём для левого и правого состояния
        self.attack_texture_pair = []
        for i in range(5):
            texture = load_texture_pair(f"{main_path}-swordAttack-{i}.png")
            self.attack_texture_pair.append(texture)

        #* Загрузка текстур смерти персонажа для левого и правого состояния
        self.die_texture_pair = []
        for i in range(7):
            texture = load_texture_pair(f"{main_path}-die-{i}.png")
            self.die_texture_pair.append(texture)

        #* Инициализируем начальную текстуру
        self.texture = self.idle_texture_pair[0]

        #? Что такое хит-боксы я пока не разобрался, но вроде нужно
        self.set_hit_box(self.texture.hit_box_points)


    def update_animation(self, delta_time=1 /60):

        #* анимация простоя
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        #* анимация бега
        self.cur_texture += 1
        if self.cur_texture > 5:
            self.cur_texture = 0
        self.texture = self.run_texture_pair[self.set_texture][self.character_face_direction]

        #* анимация прыжка
        self.cur_texture +=1
        if self.cur_texture >3:
            self.cur_texture = 0
        self.texture = self.jump_texture_pair[self.cur_texture][self.character_face_direction]

        #* анимация каста заклинания
        self.cur_texture += 1
        if self.cur_texture > 3:
            self.cur_texture = 0
        self.texture = self.cast_texture_pair[self.cur_texture][self.character_face_direction]

        #* анимация атаки мечём
        self.cur_texture +=1
        if self.cur_texture > 4:
            self.cur_texture = 0
        self.texture = self.attack_texture_pair[self.cur_texture][self.character_face_direction]

        #* анимация смерти
        self.cur_texture += 1
        if self.cur_texture > 6:
            self.cur_texture = 0
        self.texture = self.die_texture_pair[self.cur_texture][self.character_face_direction]

"""        #* анимация стояния
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.idle_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        #* анимация бега
        self.cur_texture += 1
        if self.cur_texture > 5 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.run_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        #* анимация прыжка
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.jump_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        #* анимация каста
        self.cur_texture += 1
        if self.cur_texture > 3 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.cast_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        #* анимация атаки
        self.cur_texture += 1
        if self.cur_texture > 4 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.attack_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]

        #* анимация смерти
        self.cur_texture += 1
        if self.cur_texture > 6 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        self.texture = self.die_textures[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
"""


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

        #* отслеживаем текущее состояние нажатой клавиши
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_need_reset = False

        #* Это списки которые отслеживают наши спрайты. Каждый спрайт должен войти в список.
        #TODO: self.coin_list = None
        self.wall_list = None
        #? self.background_list = None
        #TODO: self.ladder_list = None
        self.player_list = None
        self.background = None

        #* Отдельная переменная которая содержит спрайт игрока
        self.player_sprite = None

        #* Инициализируем физический движок
        self.physics_engine = None

        #* Используем для отслеживания нашего скролинга
        self.view_bottom = 0
        self.view_left = 0
        #TODO: self.view_right = 0
        #TODO: self.view_top = 0

        #* Настраиваем конец карты
        self.end_of_map = 0

        #* Отслеживание очков
        self.score = 0

        #* Ещё несколько параметров для реализации
        #TODO: self.game_over = False
        #TODO: self.last_time = None
        #TODO: self.frame_count = 0
        #TODO: self.fps_message = None

        #* Загрузка свуковых эффектов
        #TODO: self.collect_coin_sound = arcade.load_sound("указываем расположение файла")
        #TODO: self.jump_sound = arcade.load_sound("указываем расположение файла")
        #TODO: self.game_over = arcade.load_sound("указываем расположение файла")


    def setup(self):
        """ Настройка игры и инициализация переменных. """

        #* Устанавливаем задний фон для нашей карты
        self.background = arcade.load_texture("sprites/background.png")

        #? Нужно ли опять писать это тут когда написано выше? Но делаю по примеру.
        self.view_bottom = 0
        self.view_left = 0
        #TODO: self. view_score = 0

        #* Создаём спрайт листы
        self.player_sprite = arcade.SpriteList()
        #TODO: self.coin_list = arcade.SpriteList()

        #* Ссылаемся что список игрока равен классу что мы уже описали
        self.player_sprite = PlayerCharacter()

        #* Задаём начальные координаты старта персонажа, его размеры.
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.player_sprite.scale = PLAYER_SCALING
        self.player_list.append(self.player_sprite)

        #* Задаём какую карту загружать и где она расположена
        map_name = "test4.tmx"

        #* Читаем тайловую карту
        my_map = arcade.tilemap.read_tmx(map_name)
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        #* Вычисляем правый конец карты в пикселях
        self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        #* --- Слой земли ---
        self.wall_list = arcade.tilemap.process_layer(my_map, 'ground', 1)

        #* --- Слой монеток (пока не реализовано) ---
        #TODO: self.coin_list = arcade.tilemap.process_layer(my_map, coin_layer_name, TILE_SCALING)

        #* Движущиеся платформы
        #TODO: moving_platforms_list = arcade.tilemap.process_layer(my_map, moving_platforms_layer, TILE_SCALING)
        #TODO: for sprite in moving_platforms_list:
        #TODO:    self.wall_list.append(sprite)

        #* Объекты заднего фона
        #TODO: self.background_list = arcade.tilemap.process_layer(my_map, "Background", TILE_SCALING)

        #* Лестницы
        #TODO: self.ladder_list = arcade.tilemap.process_layer(my_map, "Ladders", TILE_SCALING)

        
        # --- Other stuff
        # Set the background color
        # if my_map.background_color:
        #     arcade.set_background_color(my_map.background_color)

        #* Создаём физический движок
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite,
                                                             self.wall_list,
                                                             gravity_constant=GRAVITY)   #TODO: ещё нужно будет добавить ladder=self.ladder_list


    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        #* Рисуем наши спрайты.
        self.wall_list.draw()
        self.background.draw()
        #TODO: self.background_list.draw()
        #TODO: self.ladder_list.draw()
        #TODO: self.coin_list.draw()
        self.player_list.draw()







        #self.frame_count += 1

        # This command has to happen before we start drawing
        

        scale = SCREEN_WIDTH / self.background.width
        arcade.draw_lrwh_rectangle_textured(0, 0,
                                            4800, 1280,
                                            self.background)


        # Draw all the sprites.
        self.player_list.draw()
        self.wall_list.draw()
        self.coin_list.draw()

        if self.last_time and self.frame_count % 60 == 0:
            fps = 1.0 / (time.time() - self.last_time) * 60
            self.fps_message = f"FPS: {fps:5.0f}"

        if self.fps_message:
            arcade.draw_text(self.fps_message, self.view_left + 10, self.view_bottom + 40, arcade.color.BLACK, 14)

        if self.frame_count % 60 == 0:
            self.last_time = time.time()

        # Put the text on the screen.
        # Adjust the text position based on the view port so that we don't
        # scroll the text too.
        distance = self.player.right
        output = f"Distance: {distance}"
        arcade.draw_text(output, self.view_left + 10, self.view_bottom + 20, arcade.color.BLACK, 14)

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

        if self.player.right >= self.end_of_map:
            self.game_over = True

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        if not self.game_over:
            self.physics_engine.update()

        coins_hit = arcade.check_for_collision_with_list(self.player, self.coin_list)
        for coin in coins_hit:
            coin.remove_from_sprite_lists()
            self.score += 1

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
