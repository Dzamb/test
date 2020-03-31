
import arcade
import os
import time
import math
import sys
import random

TILE_SCALING = 0.5
PLAYER_SCALING = 1
PLAYER_START_X = 196
PLAYER_START_Y = 200
PLAYER_MOVEMENT_SPEED = 7
PLAYER_JUMP_SPEED = 25
FIREBOLL_SPEED = 5

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
SCREEN_TITLE = "17-th Update"
SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# How many pixels to keep as a minimum margin between the character
# and the edge of the screen.
VIEWPORT_MARGIN_TOP = 90
VIEWPORT_MARGIN_BOTTOM = 90
VIEWPORT_RIGHT_MARGIN = 300
VIEWPORT_LEFT_MARGIN = 300

# Physics
MOVEMENT_SPEED = 6
JUMP_SPEED = 6
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

        self.running_sound = arcade.load_sound("sprites/sounds/beg.mp3")
        self.jumping_sound = arcade.load_sound("sprites/sounds/Jump3.wav")

        #* Отслеживание наших состояний
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False
        self.is_death = False
        self.is_attack = False
        self.is_casting = False

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

        #* Загрузка текстур падения для левого и правого состояния
        self.fall_texture_pair = []
        for i in range(2):
            texture = load_texture_pair(f"{main_path}-fall-{i}.png")
            self.fall_texture_pair.append(texture)

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
        self.texture = self.idle_texture_pair[0][0]

        #? Что такое хит-боксы я пока не разобрался, но вроде нужно
        self.set_hit_box(self.texture.hit_box_points)


    def update_animation(self, delta_time=1 /60):

        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        #* анимация простоя
        if self.change_x == 0 and self.change_y == 0:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATES_PER_FRAME:
                self.cur_texture = 0
            self.texture = self.idle_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return

        #* анимация прыжка и падения
        if self.change_y > 0 and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture > 3 * UPDATES_PER_FRAME:
                arcade.play_sound(self.jumping_sound)
                self.cur_texture = 0
            self.texture = self.jump_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.cur_texture += 1
            if self.cur_texture > 1:
                self.cur_texture = 0
            self.texture = self.fall_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
            return


        #* анимация бега
        self.cur_texture += 1 and self.change_y == 0
        if self.cur_texture > 5 * UPDATES_PER_FRAME:
            arcade.play_sound(self.running_sound)
            self.cur_texture = 0
        self.texture = self.run_texture_pair[self.cur_texture // UPDATES_PER_FRAME][self.character_face_direction]
        # arcade.play_sound(self.running_sound)
        return


        #* анимация каста заклинания
        self.cur_texture += 1
        if self.cur_texture > 3:
            self.cur_texture = 0
        self.texture = self.cast_texture_pair[self.cur_texture][self.character_face_direction]
        return

        #* анимация атаки мечём
        self.cur_texture +=1
        if self.cur_texture > 4:
            self.cur_texture = 0
        self.texture = self.attack_texture_pair[self.cur_texture][self.character_face_direction]
        return

        #* анимация смерти
        self.cur_texture += 1
        if self.cur_texture > 6:
            self.cur_texture = 0
        self.texture = self.die_texture_pair[self.cur_texture][self.character_face_direction]
        return










class Arrow(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y


class Fireball(arcade.Sprite):
    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += 20


class Enemy(arcade.Sprite):
    def _init_(self):
        super().__init__()
        self.player = None
        self.curtime = 0
        self.delay = 0
        self.growl = False
        self.fireball_list = None
        self.sound_list = None
        self.coin_list = None
        self.health = 100
        self.death_animation = 0

    def shoot(self):
        if self.player.alive:
            # arcade.play_sound(self.sound_list[4])

            fireball = Fireball("sprites/effects/fireboll/1_0.png")
            fireball.center_x = self.center_x
            fireball.center_y = self.center_y
            fireball.reflected = False

            local_speed = 4
            x_diff = self.player.center_x - self.center_x
            y_diff = self.player.center_y - self.center_y
            angle = math.atan2(y_diff, x_diff)
            fireball.angle = math.degrees(angle)
            fireball.change_x = math.cos(angle) * local_speed
            fireball.change_y = math.sin(angle) * local_speed

            self.fireball_list.append(fireball)

    def update(self):
        self.curtime += 1

        # If enemy dies play death animation
        if self.health <= 0 and self.death_animation == 0:
            self.death_animation = self.curtime + 30
        if self.death_animation - 20 > self.curtime:
            self.set_texture(1)
        elif self.death_animation - 10 > self.curtime:
            self.set_texture(2)
        elif self.death_animation > self.curtime:
            # Spawn a coin on death
            coin = arcade.Sprite("images/coin.png", 0.1)
            coin.center_x = self.center_x
            coin.center_y = self.center_y
            coin.force = 0
            self.coin_list.append(coin)
            self.kill()


        # If player is nearby shoot at him every 100-200 frames
        d = math.sqrt(((self.center_x - self.player.center_x) ** 2) + ((self.center_y - self.player.center_y) ** 2))
        if d < 150 and self.health > 0:
            if not self.growl:
                self.growl = True
                arcade.play_sound(self.sound_list[5])

            x_diff = self.player.center_x - self.center_x
            y_diff = self.player.center_y - self.center_y
            self.angle = math.degrees(math.atan2(y_diff, x_diff)) - 90

            if self.curtime > self.delay:
                self.delay = self.curtime + random.randint(100, 200)
                self.shoot()
        else:
            # Prevent detection noise from playing every frame
            self.growl = False





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

        self.set_mouse_visible(False)


        #* отслеживаем текущее состояние нажатой клавиши
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False
        self.jump_needs_reset = False
        self.cast_pressed = False
        self.attack_pressed = False

        self.ammo_list = None
        self.arrow_list = None
        self.enemy_list = None
        self.fireball_list = None

        self.health = 100
        self.ammo = 5
        self.knife_delay = 0
        self.knife_rate = 0

        #* Это списки которые отслеживают наши спрайты. Каждый спрайт должен войти в список.
        #TODO: self.coin_list = None
        self.wall_list = None
        #? self.background_list = None
        #TODO: self.ladder_list = None
        self.player_list = None
        self.background = None
        self.fireboll_list = None

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
        self.running_sound = arcade.load_sound("sprites/sounds/running_og1.wav")
        self.fireboll_sound = arcade.load_sound("sprites/sounds/shoot3.wav")
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
        self.player_list = arcade.SpriteList()
        self.player_sprite = arcade.SpriteList()

        self.ammo_list = arcade.SpriteList()
        self.arrow_list = arcade.SpriteList()
        self.enemy_list = arcade.SpriteList()
        self.fireball_list = arcade.SpriteList()
        #TODO: self.coin_list = arcade.SpriteList()

        self.demon_die_1 = arcade.load_texture("sprites/enemies/goblin/goblin_death_0.png")
        self.demon_die_2 = arcade.load_texture("sprites/enemies/goblin/goblin_death_1.png")
        self.demon_slash = arcade.load_texture("images/demon_slash.png")

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
        self.player_list.draw()
        self.fireboll_list.draw()

        #* Рисуем наши спрайты.
        self.wall_list.draw()
        self.background.draw()
        
        #TODO: self.background_list.draw()
        #TODO: self.ladder_list.draw()
        #TODO: self.coin_list.draw()

        #* Отрисовка очков на экране, прокрутка по области просмотра
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10 + self.view_left, 10 + view_bottom, arcade.scccolor.BLACK, 18)


    def on_mouse_press(self, x, y, button, modifiers):
        fireboll = arcade.Sprite("sprites/effects/anim_fireboll/fireboll_0.png", SPRITE_PIXEL_SIZE)

        start_x = self.player_sprite.center_x
        start_y = self.player_sprite.center_y
        fireboll.center_x = start_x
        fireboll.center_y = start_y

        dest_x = x
        dest_y = y

        x_diff = dest_x - start_x
        y_diff = dest_y - start_y
        angle = math.atan2(y_diff, x_diff)

        fireboll.angle = math.degrees(angle)
        print(f"fireboll angle: {fireboll.angle:.2f}")

        fireboll.change_x = math.cos(angle) * FIREBOLL_SPEED
        fireboll.change_y = math.sin(angle) * FIREBOLL_SPEED

        self.fireboll_list.append(fireboll)



    def process_keychange(self):
        #* Вызывается когда мы надимаем клавиши вверх/вниз или когда мы включаем/ выключаем лестницы

        #* Процесс движения вверх/вниз
        if self.up_pressed and not self.down_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
            elif self.physics_engine.can_jump() and not self.jump_needs_reset:
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                self.jump_needs_reset = True
                # arcade.play_sound(self.jump_sound)
        elif self.down_pressed and not self.up_pressed:
            if self.physics_engine.is_on_ladder():
                self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED

        #* Процесс движения вверх/вниз когда мы на лестнице и не двигаемся
        if self.physics_engine.is_on_ladder():
            if not self.up_pressed and not self.down_pressed:
                self.player_sprite.change_y = 0
            elif self.up_pressed and self.down_pressed:
                self.player_sprite.change_y = 0
        
        #* Процесс движения влево/вправо
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

        if self.attack_pressed and self.right_pressed == True:
            self.player_sprite.attack_texture_pair[0]
        elif self.attack_pressed and self.left_pressed == True:
            self.player_sprite.attack_texture_pair[1]



    def on_key_press(self, key, modifiers):
        #* Вызывается когда мы клавиша нажата.
        if key ==arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True
        elif key == arcade.key.C:
            self.attack_pressed = True

        self.process_keychange()


    def on_key_release(self, key, modifiers):
        #* Вызывается когда пользователь отпускает клавишу.

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False
        elif key == arcade.key.C:
            self.attack_pressed = False
        
        self.process_keychange()


    def on_update(self, delta_time):
        self.player_list.update_animation()
        self.wall_list.update()

        #* Движение игрока с физическим движком
        self.physics_engine.update()

        self.fireboll_list.update()

        # for fireboll in self.fireboll_list:
        #     hit_list = arcade.check_for_collision_with_list(fireboll, self.coin_list)

        #     if len(hit_list) > 0:
        #         fireboll.remove_from_sprite_lists()

        #     for coin in hit_list:
        #         coin.remove_from_sprite_lists()
        #         self.score += 1

        #     if fireboll.bottom > self.width or fireboll.top < 0 or fireboll.right < 0 or fireboll.left > self.width:
        #         fireboll.remove_from_sprite_lists()
        

        #* Обновление анимации
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True
        
        #? Дальше мне немного не понятен процесс того что я описываю
        if self.physics_engine.is_on_ladder() and not self.physics_engine.can_jump():
            self.player_sprite.is_on_ladder = True
            self.process_keychange()
        else:
            self.player_sprite.is_on_ladder = False
            self.process_keychange()

        

        #TODO: self.coin_list.update_animation(delta_time)
        #TODO: self.background_list.update_animation(delta_time)
        

        #* Обновление преград с движущимися платформами
        

        #* Логика отображающая не наткнулась ли движущаяся платформа
        #* на преграду и не надо ли повернуть движение.
        for wall in self.wall_list:

            if wall.boundary_right and wall.right > wall.boundary_right and wall.change_x > 0:
                wall.change_x *= -1
            if wall.boundary_left and wall.left < wall.boundary_left and wall.change_y < 0:
                wall.change_x *= -1
            if wall.boundary_top and wall.top > wall.boundary_top and wall.change_y > 0:
                wall.change_y *= -1
            if wall.boundary_bottom and wall.bottom < wall.boundary_bottom and wall.change_y < 0:
                wall.change_y *= -1

        #* Отслеживание столкновений с монетками.
        # coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        #* Цикл отслеживает со сколькими монетами мы столкнулись и удаляет их
        # for coin in coin_hit_list:

        #     #* Выясняем сколько очков стоит монетка
        #     if 'Points' not in coin.properties:
        #         print("Внимание собранная монетка не имеет характеристику очков")
        #     else:
        #         points = int(coin.properties['Points'])
        #         self.score += points

        #     #* Удаление монетки.
        #     coin.remove_from_sprite_lists()
        #     arcade.play_sound(self.collect_coin_sound)

        #* Отслеживание нужно ли нам поменять обзор(viewport)
        changed_viewport = False

            #* ===Скролинг===

            #* Скролинг влево
        left_boundary = self.view_left + VIEWPORT_LEFT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_viewport = True

        #* Скролинг вправо
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_viewport = True

        #* Скролинг вверх
        top_boundary = self.view_bottom + SCREEN_WIDTH - VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - right_boundary
            changed_viewport = True

        #* Скролинг вниз
        bottom_boundary = self.view_bottom + VIEWPORT_RIGHT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed_viewport = True

        if changed_viewport:
            #* Прокрутка только до целых чисел. Иначе мы получим пиксели 
            #* которые не выстраиваются в линию на экране.
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            #* Скролинг
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
