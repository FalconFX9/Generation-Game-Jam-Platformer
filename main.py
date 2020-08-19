#!/usr/bin/env python3
import arcade
import random
import math
import time
import collections
import constants as C
from player import Player
from physics_engine import PhysicsEngine


def procedural_generator() -> (arcade.SpriteList, arcade.SpriteList):
    ennemies = arcade.SpriteList()
    platforms = arcade.SpriteList(True)

    seed = random.randint(0, 10000)
    print(seed)
    # 2226
    rng = random.Random(seed)
    platform = arcade.Sprite('Platform.png')
    platform.center_x = 800
    platform.center_y = rng.randint(1500, 2500)
    platform.color = arcade.color.WHITE
    platforms.append(platform)
    current_x = 800
    current_y = int(platform.center_y)
    print(current_y)

    while current_y > 85:
        platform = arcade.Sprite('Platform.png')
        x_offset = rng.randint(30, 210)
        if rng.random() < 0.1 and (not platforms[-1].change_x or not platforms[-1].change_y):
            if rng.random() < 0.5:
                x_offset = rng.randint(300, 550)
                platforms[-1].boundary_left = platforms[-1].center_x
                platforms[-1].boundary_right = current_x + x_offset
                platforms[-1].change_x = 3
                current_x = platforms[-1].boundary_right
            if rng.random() < 0.5:
                generated_y = rng.randint(current_y - 300, current_y - 150)
                platforms[-1].boundary_top = platforms[-1].center_y
                platforms[-1].boundary_bottom = generated_y
                platforms[-1].change_y = -3
                current_y = platforms[-1].boundary_bottom
            if platforms[-1].change_x and platforms[-1].change_y:
                x_distance = platforms[-1].boundary_right - platforms[-1].boundary_left
                y_distance = platforms[-1].boundary_top - platforms[-1].boundary_bottom
                ratio = x_distance / y_distance
                platforms[-1].change_x = 3
                platforms[-1].change_y = -(3 / ratio)
                print(x_distance, y_distance, ratio, x_distance/3, y_distance/(3/ratio))
        else:
            generated_y = rng.randint(current_y - 90, current_y - 58)
            if platforms[-1].change_y:
                generated_y += 20
            generated_x = current_x - rng.choice((x_offset, -x_offset))
            platform.center_x = generated_x
            platform.center_y = generated_y
            platform.color = rng.choice((arcade.color.WHITE, arcade.color.BLUE, arcade.color.YELLOW))
            platforms.append(platform)
            current_y = platform.center_y
            current_x = platform.center_x
            #if rng.random() < 0.05:
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

    def __init__(self):
        super().__init__()

        self.player_sprite = None
        self.platforms = None
        self.ennemies = None
        self.bullet_list = None
        self.physics_engine = None

        self.w_pressed = False
        self.a_pressed = False
        self.d_pressed = False
        self.jump_needs_reset = False

        self.mouse_press = False

        self.prev_color = None

        self.frame_count = 0

        self.view_bottom = 0
        self.view_left = 0
        self.fps = FPSCounter()

        self.window.background_color = arcade.color.BLACK

    def setup(self):
        self.view_bottom = 0
        self.view_left = 0
        arcade.set_viewport(0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT)
        self.player_sprite = Player('Player.png', 1)

        self.platforms, self.ennemies = procedural_generator()
        self.bullet_list = arcade.SpriteList()

        self.player_sprite.center_x = self.platforms[-1].center_x
        self.player_sprite.bottom = 0
        self.physics_engine = PhysicsEngine(self.player_sprite, self.platforms)

    def on_draw(self):
        arcade.start_render()

        self.platforms.draw()
        self.player_sprite.draw()
        self.ennemies.draw()
        self.bullet_list.draw()
        if self.mouse_press:
            arcade.draw_arc_outline(800 + self.view_left, 450 + self.view_bottom, 300, 300, arcade.color.YELLOW, 0, 180, 15)
            arcade.draw_arc_outline(800 + self.view_left, 450 + self.view_bottom, 300, 300, arcade.color.BLUE, 180, 360, 15)

        fps = self.fps.get_fps()
        output = f"FPS: {fps:3.0f}"
        arcade.draw_text(output, 20 + self.view_left, C.SCREEN_HEIGHT - 80, arcade.color.WHITE, 16)

    def on_update(self, delta_time: float):
        self.frame_count += 1
        self.player_sprite.current_background = self.window.background_color

        if self.w_pressed:
            jump_test = self.physics_engine.can_jump()
            if jump_test[0] and not self.jump_needs_reset:
                self.physics_engine.jump(10 + jump_test[1])
                self.jump_needs_reset = True
        if self.a_pressed and not self.d_pressed:
            if self.player_sprite.change_x > - (C.MAX_SPEED + self.player_sprite.momentum):
                self.player_sprite.change_x -= 0.1 * self.player_sprite.speed_multiplier
        elif self.d_pressed and not self.a_pressed:
            if self.player_sprite.change_x < C.MAX_SPEED + self.player_sprite.momentum:
                self.player_sprite.change_x += 0.1 * self.player_sprite.speed_multiplier
        else:
            if self.player_sprite.change_x > C.FRICTION * self.player_sprite.speed_multiplier:
                self.player_sprite.change_x -= C.FRICTION * self.player_sprite.speed_multiplier
            elif self.player_sprite.change_x < - C.FRICTION * self.player_sprite.speed_multiplier:
                self.player_sprite.change_x += C.FRICTION * self.player_sprite.speed_multiplier
            else:
                self.player_sprite.change_x = 0

        self.physics_engine.update()

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

                #if self.frame_count % 30 == 0:
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

        if self.player_sprite.top >= self.platforms[0].center_y + 95:
            self.setup()

        self.fps.tick()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.w_pressed = True
        elif symbol == arcade.key.A:
            self.a_pressed = True
        elif symbol == arcade.key.D:
            self.d_pressed = True
        elif symbol == arcade.key.R:
            self.setup()

    def on_key_release(self, symbol: int, modifiers: int):
        if symbol == arcade.key.W:
            self.w_pressed = False
            self.jump_needs_reset = False
        elif symbol == arcade.key.A:
            self.a_pressed = False
        elif symbol == arcade.key.D:
            self.d_pressed = False

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


def main():
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.TITLE, update_rate=1/120)
    start_view = Game()
    window.show_view(start_view)
    start_view.setup()
    arcade.run()


if __name__ == '__main__':
    main()
