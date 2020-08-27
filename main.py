import pickle
import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel
from game import Game, resource_path
import constants as C
import generator_data
from time import sleep


def click_sound():
    arcade.play_sound(arcade.load_sound(resource_path('sounds/click.wav')), 0.05)


class LevelManager:

    def __init__(self, levels):
        self.current_level = None
        self.levels = levels
        try:
            save_file = open(resource_path('data/current_level.save'), 'rb')
            self.current_level = self.levels[pickle.load(save_file)]
        except FileNotFoundError:
            self.current_level = self.levels[0]


class PlayButton(UIFlatButton):

    def __init__(self, window: arcade.Window, ui_manager: UIManager, level_manager: LevelManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        self.ui_manager = ui_manager
        self.level_manager = level_manager

    def on_click(self):
        click_sound()
        self.ui_manager.purge_ui_elements()
        self.window.show_view(Game(self.level_manager.current_level, self.level_manager))


class PlayButtonEndless(UIFlatButton):

    def __init__(self, window: arcade.Window, ui_manager: UIManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        self.ui_manager = ui_manager

    def on_click(self):
        click_sound()
        self.ui_manager.purge_ui_elements()
        self.window.show_view(Game(generator_data.GeneratorData()))


class LevelMenuButton(UIFlatButton):

    def __init__(self, window: arcade.Window, ui_manager: UIManager, level_manager: LevelManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        self.ui_manager = ui_manager
        self.level_manager = level_manager

    def on_click(self):
        click_sound()
        self.ui_manager.purge_ui_elements()
        self.window.show_view(LevelMenu(self.window, self.level_manager))


class OptionsMenuButton(UIFlatButton):

    def __init__(self, window: arcade.Window, ui_manager: UIManager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window
        self.ui_manager = ui_manager

    def on_click(self):
        click_sound()
        self.ui_manager.purge_ui_elements()
        self.window.show_view(OptionsMenu(self.window))


class ExitButton(UIFlatButton):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def on_click(self):
        click_sound()
        arcade.close_window()


class LevelButton(UIFlatButton):

    def __init__(self, level_seed: generator_data.GeneratorData, window: arcade.Window, ui_manager: UIManager,
                 level_manager: LevelManager, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.window = window
        self.ui_manager = ui_manager
        self.level_seed = level_seed
        self.level_manager = level_manager

    def on_click(self):
        if self.level_seed.lvl_id <= self.level_manager.current_level.lvl_id:
            click_sound()
            self.ui_manager.purge_ui_elements()
            self.window.show_view(Game(self.level_seed, self.level_manager))
        else:
            arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)


class MainMenu(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()

        self.window = window

        self.ui_manager = UIManager(window)
        self.menu_music = None
        self.level_manager = None

    def setup(self):
        self.level_manager = LevelManager(generator_data.level_list)
        print(self.level_manager.current_level.lvl_id)
        arcade.set_background_color(arcade.color.BLACK)
        self.play_song()
        self.ui_manager.purge_ui_elements()
        self.window.set_viewport(0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT)
        play_button = PlayButton(self.window, self.ui_manager, self.level_manager, 'PLAY', self.window.width // 2, 500,
                                 200, 50)
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

        play_button_endless = PlayButtonEndless(self.window, self.ui_manager, 'PLAY ENDLESS',
                                                self.window.width // 2, 700,
                                                300, 70)
        play_button_endless.set_style_attrs(font_color=arcade.color.WHITE,
                                            bg_color=arcade.color.BLACK,
                                            border_color=arcade.color.BLACK,
                                            border_color_hover=arcade.color.WHITE,
                                            border_color_press=arcade.color.WHITE)

        self.ui_manager.add_ui_element(play_button_endless)

        level_button = LevelMenuButton(self.window, self.ui_manager, self.level_manager, 'LEVEL MENU',
                                       self.window.width // 2, 400, 200, 50)
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

        options_button = OptionsMenuButton(self.window, self.ui_manager, 'OPTIONS', self.window.width // 2, 300, 200,
                                           50)
        options_button.set_style_attrs(font_color=arcade.color.BLACK,
                                       font_color_hover=arcade.color.BLACK,
                                       font_color_press=arcade.color.BLACK,
                                       bg_color=arcade.color.BLUE,
                                       bg_color_hover=(0, 0, 150),
                                       bg_color_press=arcade.color.DARK_BLUE,
                                       border_color=arcade.color.BLUE,
                                       border_color_hover=arcade.color.WHITE,
                                       border_color_press=arcade.color.WHITE)

        self.ui_manager.add_ui_element(options_button)

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

        self.ui_manager.add_ui_element(
            UILabel('Created by FalconFX9 for the timathon challenge', self.window.width // 2, 100))

    def play_song(self):
        self.menu_music = arcade.Sound(resource_path('music/MenuSong.wav'), streaming=True)
        self.menu_music.play(0.1)
        sleep(0.03)

    def on_update(self, delta_time: float):
        position = self.menu_music.get_stream_position()

        if position == 0.0:
            self.play_song()

    def on_show_view(self):
        self.setup()

    def on_hide_view(self):
        self.ui_manager.purge_ui_elements()
        self.menu_music.stop()

    def on_draw(self):
        arcade.start_render()


class LevelMenu(arcade.View):

    def __init__(self, window, level_manager):
        super().__init__()

        self.window = window

        self.ui_manager = UIManager(window)
        self.level_manager = level_manager

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        for x, level in enumerate(generator_data.level_list):
            level_button = LevelButton(level, self.window, self.ui_manager, self.level_manager,
                                       f'Level {level.lvl_id + 1}:\n {level.lvl_description}', 175 + (x % 6) * 250,
                                       700 - (150 * (x // 6)), 200, 100)
            level_button.set_style_attrs(font_color=arcade.color.WHITE,
                                         font_color_hover=arcade.color.RED,
                                         font_color_press=arcade.color.WHITE,
                                         bg_color=arcade.color.BLACK,
                                         border_color=arcade.color.RED,
                                         border_color_hover=arcade.color.WHITE,
                                         border_color_press=arcade.color.WHITE)
            self.ui_manager.add_ui_element(level_button)

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.ui_manager.purge_ui_elements()
            self.window.show_view(MainMenu(self.window))


class OptionsMenu(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window

    def setup(self):
        pass

    def on_show_view(self):
        self.setup()


def main():
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.TITLE, update_rate=1 / 120)
    window.show_view(MainMenu(window))
    arcade.run()


if __name__ == '__main__':
    main()
