import arcade


class Player(arcade.Sprite):
    
    def __init__(self, image, image_scaling):
        super(Player, self).__init__(image, image_scaling)

        self.speed_multiplier = 1
        self.current_background = None
        self.momentum = 0
