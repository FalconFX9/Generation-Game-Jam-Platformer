import arcade
import constants as C


def _move_sprite(moving_sprite: arcade.Sprite, platforms: arcade.SpriteList):

    if moving_sprite.bottom <= 0 and moving_sprite.change_y < 0:
        moving_sprite.change_y = 0
        moving_sprite.bottom = 0

    moving_sprite.center_y += moving_sprite.change_y * moving_sprite.speed_multiplier

    hit_list_y = arcade.check_for_collision_with_list(moving_sprite, platforms)

    for platform in hit_list_y:
        if platform.color != moving_sprite.current_background:
            if moving_sprite.change_y > 0:
                if not platform.change_y:
                    moving_sprite.top = platform.bottom
                    moving_sprite.change_y = 0

            elif moving_sprite.change_y < 0:
                moving_sprite.bottom = platform.top
                if platform.change_y > 0:
                    moving_sprite.change_y = 0
                else:
                    moving_sprite.change_y = -3
                if platform.change_x:
                    moving_sprite.momentum = platform.change_x

    moving_sprite.center_x += (moving_sprite.change_x + moving_sprite.momentum) * moving_sprite.speed_multiplier

    hit_list_x = arcade.check_for_collision_with_list(moving_sprite, platforms)

    for platform in hit_list_x:
        if platform.color != moving_sprite.current_background and platform not in hit_list_y:
            if moving_sprite.change_x > 0 and not platform.change_x:
                moving_sprite.right = platform.left
            elif moving_sprite.change_x < 0 and not platform.change_x:
                moving_sprite.left = platform.right

            moving_sprite.change_x = 0

    if len(hit_list_y) <= 0 and moving_sprite.momentum != 0:
        moving_sprite.change_x += moving_sprite.momentum
        moving_sprite.momentum = 0


class PhysicsEngine:

    def __init__(self, player: arcade.Sprite, platforms: arcade.SpriteList, gravity_constant: float = 0.5, ladders: arcade.SpriteList = None):
        self.player = player
        self.platforms = platforms
        self.gravity_constant = gravity_constant
        self.ladders = ladders

    def is_on_ladder(self) -> bool:
        if self.ladders:
            hit_list = arcade.check_for_collision_with_list(self.player, self.ladders)

            if len(hit_list) > 0:
                return True
            else:
                return False

    def can_jump(self, y_distance=5) -> (bool, float):
        self.player.center_y -= y_distance

        hit_list = arcade.check_for_collision_with_list(self.player, self.platforms)

        self.player.center_y += y_distance

        if (len(hit_list) > 0 and hit_list[0].color != self.player.current_background) or self.player.bottom <= 0:
            if self.player.bottom <= 0:
                return True, 0
            else:
                return True, hit_list[0].change_y
        else:
            return False, 0

    def jump(self, velocity: int):
        self.player.change_y = velocity

    def can_hang(self, hang_timer: int, y_distance=5) -> (bool, arcade.SpriteList):
        self.player.center_y += y_distance
        hit_list = arcade.check_for_collision_with_list(self.player, self.platforms)
        self.player.center_y -= y_distance

        if len(hit_list) > 0 and hit_list[0].color != self.player.current_background and hang_timer > 0:
            return True, hit_list
        else:
            return False, arcade.SpriteList

    def hang(self, hit_platform: arcade.SpriteList, hang_timer: int) -> int:
        self.player.change_y = 0
        self.player.top = hit_platform[0].bottom
        hang_timer -= 1
        return hang_timer

    def can_switch(self):
        hit_list = arcade.check_for_collision_with_list(self.player, self.platforms)

        if hit_list:
            return False
        else:
            return True

    def update(self):
        if not self.is_on_ladder():
            self.player.change_y -= self.gravity_constant * self.player.speed_multiplier

        _move_sprite(self.player, self.platforms)

        for platform in self.platforms:
            if platform.change_x != 0 or platform.change_y != 0:
                platform.center_x += platform.change_x * self.player.speed_multiplier

                if platform.boundary_left is not None \
                        and platform.center_x <= platform.boundary_left:
                    platform.center_x = platform.boundary_left
                    if platform.change_x < 0:
                        platform.change_x *= -1

                if platform.boundary_right is not None \
                        and platform.center_x >= platform.boundary_right:
                    platform.center_x = platform.boundary_right
                    if platform.change_x > 0:
                        platform.change_x *= -1

                collision = arcade.check_for_collision(self.player, platform)
                if collision and not platform.change_y:
                    if platform.change_x < 0:
                        self.player.right = platform.left
                    if platform.change_x > 0:
                        self.player.left = platform.right

                platform.center_y += platform.change_y * self.player.speed_multiplier

                if platform.boundary_top is not None \
                        and platform.center_y >= platform.boundary_top:
                    platform.center_y = platform.boundary_top
                    if platform.change_y > 0:
                        platform.change_y *= -1

                if platform.boundary_bottom is not None \
                        and platform.center_y <= platform.boundary_bottom:
                    platform.center_y = platform.boundary_bottom
                    if platform.change_y < 0:
                        platform.change_y *= -1

                collision = arcade.check_for_collision(self.player, platform)
                if collision:
                    if platform.change_y < 0 and self.player.change_y > 0:
                        self.player.top = platform.bottom
                        self.player.change_y = -3
