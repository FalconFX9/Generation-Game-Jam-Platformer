import arcade
from arcade.gui import UIManager, UIFlatButton, UIImageButton
from game import Game, resource_path
import constants as C


class PlayButton(UIFlatButton):

    def __init__(self, window: arcade.Window, ui_manager: UIManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        self.ui_manager = ui_manager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        self.window.show_view(Game())


class LevelMenuButton(UIFlatButton):

    def __init__(self, window: arcade.Window, ui_manager: UIManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        self.ui_manager = ui_manager

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        self.window.show_view(LevelMenu(self.window))


class ExitButton(UIFlatButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_click(self):
        exit()


class LevelButton(UIImageButton):

    def __init__(self, level_seed: int, window: arcade.Window, ui_manager: UIManager, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window = window
        self.ui_manager = ui_manager
        self.level_seed = level_seed

    def on_click(self):
        self.ui_manager.purge_ui_elements()
        self.window.show_view(Game(self.level_seed))


class MainMenu(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window

        self.ui_manager = UIManager(window)

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.ui_manager.purge_ui_elements()

        play_button = PlayButton(self.window, self.ui_manager, 'PLAY', self.window.width // 2, 500, 200, 50)
        play_button.set_style_attrs(font_color=arcade.color.BLACK,
                                    font_color_hover=arcade.color.BLACK,
                                    font_color_press=arcade.color.BLACK,
                                    bg_color=arcade.color.GREEN,
                                    bg_color_hover=(0, 150, 0),
                                    bg_color_press=arcade.color.DARK_GREEN,
                                    border_color=arcade.color.GREEN,
                                    border_color_hover=arcade.color.WHITE,
                                    border_color_press=arcade.color.WHITE)

        self.ui_manager.add_ui_element(play_button)

        level_button = LevelMenuButton(self.window, self.ui_manager, 'LEVEL MENU', self.window.width // 2, 300, 200, 50)
        level_button.set_style_attrs(font_color=arcade.color.BLACK,
                                     font_color_hover=arcade.color.BLACK,
                                     font_color_press=arcade.color.BLACK,
                                     bg_color=arcade.color.BLUE,
                                     bg_color_hover=(0, 0, 150),
                                     bg_color_press=arcade.color.DARK_BLUE,
                                     border_color=arcade.color.BLUE,
                                     border_color_hover=arcade.color.WHITE,
                                     border_color_press=arcade.color.WHITE)

        self.ui_manager.add_ui_element(level_button)

        exit_button = ExitButton('EXIT', self.window.width // 2, 200, 200, 50)
        exit_button.set_style_attrs(font_color=arcade.color.BLACK,
                                    font_color_hover=arcade.color.BLACK,
                                    font_color_press=arcade.color.BLACK,
                                    bg_color=arcade.color.RED,
                                    bg_color_hover=(150, 0, 0),
                                    bg_color_press=arcade.color.DARK_RED,
                                    border_color=arcade.color.RED,
                                    border_color_hover=arcade.color.WHITE,
                                    border_color_press=arcade.color.WHITE)

        self.ui_manager.add_ui_element(exit_button)

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()


class LevelMenu(arcade.View):

    def __init__(self, window):
        super().__init__()

        self.window = window

        self.ui_manager = UIManager(window)

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        level1_image = arcade.load_texture(resource_path('images/Level1.png'))
        level1_bordered_image = arcade.load_texture(resource_path('images/Level1Bordered.png'))
        self.ui_manager.add_ui_element(LevelButton(
            4384,
            self.window,
            self.ui_manager,
            center_x=200,
            center_y=800,
            normal_texture=level1_image,
            hover_texture=level1_bordered_image,
            press_texture=level1_bordered_image,
            text='Level 1'
        ))

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()


def main():
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.TITLE, update_rate=1 / 120)
    window.show_view(MainMenu(window))
    arcade.run()


if __name__ == '__main__':
    main()
