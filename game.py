#!/usr/bin/env python3
import pickle
import arcade
import random
import math
import time
import os
import sys
import collections
import constants as C
from player import Player
from physics_engine import PhysicsEngine
from generator_data import GeneratorData
from time import sleep


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def load_tile_table(filename, largeur, hauteur):
    locations = []
    for image_y in range(0, int(512 / hauteur)):
        for image_x in range(0, int(512 / largeur)):
            locations.append((image_x * largeur, image_y * hauteur, largeur, hauteur))
    images = arcade.load_textures(filename, locations)
    return images


def one_tile_platform(tiles: list, spritelist, x, y, type=0):
    tile = arcade.Sprite()
    tile.center_x = x
    tile.center_y = y
    if type == 0:
        tile.texture = tiles[1]
    else:
        tile.texture = tiles[9]

    spritelist.append(tile)


def multitile_platform(tiles: list, spritelist, x, y, number_of_platforms=0, type=0):
    current_x = x
    tile = arcade.Sprite()
    tile.center_x = x
    tile.center_y = y
    if type == 0:
        tile.texture = tiles[20]
    else:
        tile.texture = tiles[28]
    spritelist.append(tile)
    for i in range(number_of_platforms):
        tile = arcade.Sprite()
        tile.center_x = x + (i * 32) + 32
        tile.center_y = y
        current_x = tile.center_x
        if type == 0:
            tile.texture = tiles[21]
        else:
            tile.texture = tiles[29]
        spritelist.append(tile)
    tile = arcade.Sprite()
    tile.center_x = current_x + 32
    tile.center_y = y
    if type == 0:
        tile.texture = tiles[22]
    else:
        tile.texture = tiles[30]
    spritelist.append(tile)


def procedural_generator(gen_data: GeneratorData) -> (arcade.SpriteList, arcade.SpriteList):
    tiles = load_tile_table(resource_path('images/tileset.png'), 32, 32)
    ennemies = arcade.SpriteList()
    platforms = arcade.SpriteList(True)

    if not gen_data.seed:
        gen_data.seed = random.randint(0, 10000)
    # 2226
    # 3529 is a really fun seed, but has a few glitches at the end
    # 4384
    rng = random.Random(gen_data.seed)
    platform = arcade.Sprite(resource_path('images/Platform.png'))
    platform.center_x = 800
    platform.center_y = rng.randint(1500, gen_data.max_height)
    platform.color = arcade.color.WHITE
    platforms.append(platform)
    current_x = 800
    current_y = int(platform.center_y)
    platform_number = 1

    while current_y > 90:
        platform = arcade.Sprite(resource_path('images/Platform.png'))
        x_offset = rng.randint(30, 160)
        if rng.random() < gen_data.mv_chance and len(platforms) > 1:
            x_chance = rng.random()
            y_chance = rng.random()
            x_offset = rng.randint(300, 550)
            generated_y = rng.randint(current_y - 300, current_y - 150)
            for platform_num in range(-1, -platform_number - 2, -1):

                if not platforms[platform_num].change_x or not platforms[platform_num].change_y:
                    if platform_number == 0:
                        platforms[platform_num].texture = tiles[9]
                    else:
                        if platform_num == -1:
                            platforms[platform_num].texture = tiles[30]
                        elif platform_num == -platform_number - 1:
                            platforms[platform_num].texture = tiles[28]
                        else:
                            platforms[platform_num].texture = tiles[29]
                    if x_chance < gen_data.mv_chance_x:
                        platforms[platform_num].boundary_left = platforms[platform_num].center_x
                        platforms[platform_num].boundary_right = platforms[platform_num].center_x + x_offset
                        platforms[platform_num].change_x = 3
                        current_x = platforms[platform_num].boundary_right
                    if y_chance < gen_data.mv_chance_y:
                        platforms[platform_num].boundary_top = platforms[platform_num].center_y
                        platforms[platform_num].boundary_bottom = generated_y
                        platforms[platform_num].change_y = -3
                        current_y = platforms[platform_num].boundary_bottom
                    if platforms[platform_num].change_x and platforms[platform_num].change_y and gen_data.mv_chance_xy:
                        x_distance = platforms[platform_num].boundary_right - platforms[platform_num].boundary_left
                        y_distance = platforms[platform_num].boundary_top - platforms[platform_num].boundary_bottom
                        ratio = x_distance / y_distance
                        platforms[platform_num].change_x = 3
                        platforms[platform_num].change_y = -(3 / ratio)
        else:
            right_x = platforms[-1].center_x
            platform_number = rng.randint(0, gen_data.pl_num)
            platform_size = platform_number * 32
            if rng.random() < 0.5:
                actual_offset = x_offset + rng.randint(0, platform_size)
                generated_x = current_x - actual_offset
                actual_offset -= platform_size
            else:
                if platform_number != 0:
                    actual_offset = rng.choice((rng.randint(-platform_size + 16, 0), rng.randint(45, 160)))
                else:
                    actual_offset = rng.randint(45, 160)
                generated_x = right_x + actual_offset
            if actual_offset > 100:
                mathx = actual_offset / 4
                jump_height = -0.25 * (mathx ** 2) + 10 * mathx

                generated_y = rng.randint(int(current_y - jump_height), current_y)
            else:
                generated_y = rng.randint(current_y - 90, current_y - 77)
            if platforms[-1].change_y:
                generated_y += 20
            platform.center_x = generated_x
            platform.center_y = generated_y
            check_meshing = arcade.check_for_collision_with_list(platform, platforms)
            if not check_meshing:
                if platform.center_y < 56:
                    platform.center_y = 56
                if platform_number == 0:
                    one_tile_platform(tiles, platforms, platform.center_x, platform.center_y, rng.choice((0, 0)))
                else:
                    multitile_platform(tiles, platforms, platform.center_x, platform.center_y, platform_number - 1)
            current_y = platform.center_y
            current_x = platform.center_x

            # if rng.random() < 0.05:
            #    ennemy = arcade.Sprite(":resources:images/space_shooter/playerShip1_green.png", 0.3)
            #    ennemy.center_x = platform.center_x
            #    ennemy.center_y = platform.center_y + 50
            #    ennemy.angle = 90
            #    ennemies.append(ennemy)

    return platforms, ennemies


class FPSCounter:
    def __init__(self):
        self.time = time.perf_counter()
        self.frame_times = collections.deque(maxlen=60)

    def tick(self):
        t1 = time.perf_counter()
        dt = t1 - self.time
        self.time = t1
        self.frame_times.append(dt)

    def get_fps(self):
        total_time = sum(self.frame_times)
        if total_time == 0:
            return 0
        else:
            return len(self.frame_times) / sum(self.frame_times)


class Game(arcade.View):

    def __init__(self, seed=None, level_manager=None):
        super().__init__()

        self.player_sprite = None
        self.platforms = None
        self.ennemies = None
        self.bullet_list = None
        self.primitive_list = None
        self.physics_engine = None

        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.space_pressed = False
        self.jump_needs_reset = False
        self.hang_timer = 40
        self.seed = seed
        self.level_manager = level_manager

        self.mouse_press = False

        self.prev_color = None

        self.frame_count = 0

        self.view_bottom = 0
        self.view_left = 0
        self.fps = FPSCounter()

        self.window.background_color = arcade.color.BLACK

        self.jump_sound = None
        self.hang_sound = None

        self.music = None

        self.music_enabled = True
        self.sounds_enabled = True

    def play_song(self):
        if not self.music:
            self.music = arcade.Sound(resource_path(random.choice(
                ['music/MenuSong.wav', 'music/S1-Beep.wav', 'music/S2-FastBeep.wav', 'music/S3-Nyoom.wav'])),
                                      streaming=True)
        self.music.play(0.1)
        sleep(0.03)

    def setup(self):
        try:
            file = open(resource_path('data/settings.info'), 'rb')
            info = pickle.load(file)
            self.music_enabled = info[1]
            self.sounds_enabled = info[2]
        except FileNotFoundError:
            self.music_enabled = True
            self.sounds_enabled = True
        if self.music:
            self.music.stop()
        self.music = None
        if self.music_enabled:
            self.play_song()
        self.primitive_list = arcade.ShapeElementList()
        self.view_bottom = 0
        self.view_left = 0
        arcade.set_viewport(0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT)
        self.player_sprite = Player(resource_path('images/Player.png'), 1)

        self.platforms, self.ennemies = procedural_generator(self.seed)
        self.bullet_list = arcade.SpriteList()

        self.player_sprite.center_x = self.platforms[-1].center_x + 40
        self.player_sprite.bottom = 0
        self.physics_engine = PhysicsEngine(self.player_sprite, self.platforms)
        self.jump_sound = arcade.load_sound(resource_path('sounds/jump.wav'))
        self.hang_sound = arcade.load_sound(resource_path('sounds/cling.wav'))

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()

        if self.seed.tutorial:
            arcade.draw_text(self.seed.tutorial, self.platforms[-1].center_x + 40, 100, arcade.color.WHITE, 30)

        if self.seed.lvl_id or self.seed.lvl_id == 0:
            arcade.draw_text(f'Level: {self.seed.lvl_id + 1}', self.view_left + C.SCREEN_WIDTH - 20,
                             self.view_bottom + C.SCREEN_HEIGHT - 40, arcade.color.WHITE, 20, anchor_x='right')
        else:
            arcade.draw_text(f'Seed: {self.seed.seed}', self.view_left + C.SCREEN_WIDTH - 20,
                             self.view_bottom + C.SCREEN_HEIGHT - 40, arcade.color.WHITE, 20, anchor_x='right')

        self.platforms.draw()
        self.player_sprite.draw()
        self.ennemies.draw()
        if self.hang_timer > 0 and self.space_pressed and len(self.primitive_list) > 0:
            self.primitive_list.draw()
        self.bullet_list.draw()
        if False is True:
            arcade.draw_arc_outline(800 + self.view_left, 450 + self.view_bottom, 300, 300, arcade.color.YELLOW, 0, 180,
                                    15)
            arcade.draw_arc_outline(800 + self.view_left, 450 + self.view_bottom, 300, 300, arcade.color.BLUE, 180, 360,
                                    15)

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(output, 20 + self.view_left, C.SCREEN_HEIGHT + self.view_bottom - 40, arcade.color.WHITE, 16)

    def on_update(self, delta_time: float):
        if self.music:
            position = self.music.get_stream_position()

            if position == 0.0:
                self.play_song()
        hang_test = [False, 0]
        self.frame_count += 1
        self.player_sprite.current_background = self.window.background_color
        for item in self.primitive_list:
            self.primitive_list.remove(item)
        if self.w_pressed:
            jump_test = self.physics_engine.can_jump()
            if jump_test[0] and not self.jump_needs_reset:
                self.physics_engine.jump(12 + jump_test[1])
                if self.sounds_enabled:
                    arcade.play_sound(self.jump_sound, 0.01)
                self.jump_needs_reset = True
                self.hang_timer = 40
        if self.space_pressed:
            hang_test = self.physics_engine.can_hang(self.hang_timer)
            if hang_test[0]:
                if self.hang_timer == 40:
                    if self.sounds_enabled:
                        arcade.play_sound(self.hang_sound, 0.05)
                self.hang_timer = self.physics_engine.hang(hang_test[1], self.hang_timer)
        if self.a_pressed and not self.d_pressed:
            if self.player_sprite.change_x > - C.MAX_SPEED:
                self.player_sprite.change_x -= 0.1 * self.player_sprite.speed_multiplier
        elif self.d_pressed and not self.a_pressed:
            if self.player_sprite.change_x < C.MAX_SPEED:
                self.player_sprite.change_x += 0.1 * self.player_sprite.speed_multiplier
        else:
            if self.player_sprite.change_x > C.FRICTION * self.player_sprite.speed_multiplier:
                self.player_sprite.change_x -= C.FRICTION * self.player_sprite.speed_multiplier
            elif self.player_sprite.change_x < - C.FRICTION * self.player_sprite.speed_multiplier:
                self.player_sprite.change_x += C.FRICTION * self.player_sprite.speed_multiplier
            else:
                self.player_sprite.change_x = 0

        self.physics_engine.update(delta_time)

        if hang_test[0]:
            if self.player_sprite.change_x > 0:
                x_offset = self.player_sprite.change_x
            else:
                x_offset = 0
            self.primitive_list.append(arcade.create_rectangle_filled(
                self.player_sprite.center_x + 20 + (self.hang_timer // 2) + x_offset,
                self.player_sprite.center_y + 30,
                self.hang_timer,
                5,
                (255 - int(self.hang_timer * (255 / 40)), int(self.hang_timer * (255 / 40)), 0)))
            self.primitive_list.append(arcade.create_rectangle_outline(
                self.player_sprite.center_x + 40,
                self.player_sprite.center_y + 30,
                40,
                5,
                arcade.color.WHITE))

        for enemy in self.ennemies:
            if arcade.has_line_of_sight(enemy.position, self.player_sprite.position, self.platforms):
                start_x = enemy.center_x
                start_y = enemy.center_y

                dest_x = self.player_sprite.center_x
                dest_y = self.player_sprite.center_y

                x_diff = dest_x - start_x
                y_diff = dest_y - start_y
                angle = math.atan2(y_diff, x_diff)

                enemy.angle = math.degrees(angle) - 90

                # if self.frame_count % 30 == 0:
                #    bullet = arcade.Sprite(":resources:images/space_shooter/laserBlue01.png", 0.5)
                #    bullet.center_x = start_x
                #    bullet.center_y = start_y

                #    bullet.angle = math.degrees(angle)

                #    bullet.change_x = math.cos(angle) * C.BULLET_SPEED
                #    bullet.change_y = math.sin(angle) * C.BULLET_SPEED

                #    self.bullet_list.append(bullet)

        for bullet in self.bullet_list:
            if self.view_left > bullet.center_x or bullet.center_x > C.SCREEN_WIDTH + self.view_left or \
                    self.view_bottom > bullet.center_y or bullet.center_y > C.SCREEN_HEIGHT + self.view_bottom:
                bullet.remove_from_sprite_lists()

        self.bullet_list.update()
        changed = False

        # Scroll left
        left_boundary = self.view_left + C.LEFT_VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + C.SCREEN_WIDTH - C.RIGHT_VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + C.SCREEN_HEIGHT - C.TOP_VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                C.SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                C.SCREEN_HEIGHT + self.view_bottom)

        if self.player_sprite.top >= self.platforms[0].center_y + 125 and self.platforms[
            0].left < self.player_sprite.center_x < self.platforms[0].right:
            if self.level_manager:
                if self.seed.lvl_id + 1 < len(self.level_manager.levels):
                    self.seed = self.level_manager.levels[self.seed.lvl_id + 1]
                    if self.seed.lvl_id == self.level_manager.current_level.lvl_id + 1:
                        self.level_manager.current_level = self.level_manager.levels[self.seed.lvl_id]
                        pickle_out = open(resource_path('data/current_level.save'), 'wb')
                        pickle.dump(self.seed.lvl_id, pickle_out)
                        pickle_out.close()
                    self.setup()
                else:
                    from main import Victory
                    pickle_out = open(resource_path('data/current_level.save'), 'wb')
                    pickle.dump(self.seed.lvl_id + 1, pickle_out)
                    pickle_out.close()
                    self.window.show_view(Victory(self.window))
            else:
                self.seed.seed = None
                self.setup()

        if self.player_sprite.top <= self.view_bottom:
            self.setup()

        self.fps.tick()

    def on_hide_view(self):
        if self.music:
            self.music.stop()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.w_pressed = True
        elif symbol == arcade.key.A:
            self.a_pressed = True
        elif symbol == arcade.key.D:
            self.d_pressed = True
        elif symbol == arcade.key.R:
            self.setup()
        elif symbol == arcade.key.SPACE:
            if self.seed.lvl_id is None:
                self.space_pressed = True
            else:
                if self.seed.lvl_id >= 11:
                    self.space_pressed = True
        elif symbol == arcade.key.ESCAPE:
            from main import MainMenu
            self.window.show_view(MainMenu(self.window))

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.w_pressed = False
            self.jump_needs_reset = False
        elif symbol == arcade.key.A:
            self.a_pressed = False
        elif symbol == arcade.key.D:
            self.d_pressed = False
        elif symbol == arcade.key.SPACE:
            self.space_pressed = False

    '''

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_press = True
        self.player_sprite.speed_multiplier = 0.2
        self.window.background_color = arcade.color.BLACK

    def on_mouse_release(self, x: float, y: float, button: int, modifiers: int):
        self.mouse_press = False
        self.player_sprite.speed_multiplier = 1
        if self.physics_engine.can_switch():
            angle = math.degrees(math.atan2(y - 450, x - 800))
            distance = math.sqrt((x - 800)**2 + (y - 450)**2)
            if distance > 150:
                if 180 > angle > 0:
                    self.window.background_color = arcade.color.YELLOW
                else:
                    self.window.background_color = arcade.color.BLUE
                self.prev_color = self.window.background_color
                
    '''
