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
                moving_sprite.top = platform.bottom
            elif moving_sprite.change_y < 0:
                moving_sprite.bottom = platform.top

            if platform.change_x:
                if moving_sprite.momentum == 0:
                    moving_sprite.change_x += platform.change_x
                elif moving_sprite.momentum == platform.change_x * -1:
                    moving_sprite.change_x += platform.change_x * 2
                moving_sprite.momentum = platform.change_x

            moving_sprite.change_y = 0

    if len(hit_list_y) == 0:
        moving_sprite.momentum = 0

    moving_sprite.center_x += moving_sprite.change_x * moving_sprite.speed_multiplier

    hit_list_x = arcade.check_for_collision_with_list(moving_sprite, platforms)

    for platform in hit_list_x:
        if platform.color != moving_sprite.current_background:
            if moving_sprite.change_x > 0:
                moving_sprite.right = platform.left
            elif moving_sprite.change_x < 0:
                moving_sprite.left = platform.right

            moving_sprite.change_x = 0


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

    def can_jump(self, y_distance=5) -> bool:
        self.player.center_y -= y_distance

        hit_list = arcade.check_for_collision_with_list(self.player, self.platforms)

        self.player.center_y += y_distance

        if (len(hit_list) > 0 and hit_list[0].color != self.player.current_background) or self.player.bottom <= 0:
            return True
        else:
            return False

    def jump(self, velocity: int):
        self.player.change_y = velocity
        self.player.momentum = 0

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
