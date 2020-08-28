import pickle
import arcade
from arcade.gui import UIManager, UIFlatButton, UILabel, UIInputBox
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
        self.finished = False
        try:
            save_file = open(resource_path('data/current_level.save'), 'rb')
            lvl_id = pickle.load(save_file)
            if lvl_id == 21:
                self.current_level = self.levels[20]
                self.finished = True
            else:
                self.current_level = self.levels[lvl_id]
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
        if self.level_manager.finished:
            self.window.show_view(LevelMenu(self.window, self.level_manager))
        else:
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
            UILabel('Created by FalconFX9 for the timathon challenge', C.SCREEN_WIDTH // 2, 100))

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
        self.ui_manager = UIManager(window)
        self.level_stats = generator_data.GeneratorData()

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        seed_box = UIInputBox(100, C.SCREEN_HEIGHT - 100, 150, 40, 'Enter seed', 'seed_box')

        self.ui_manager.add_ui_element(seed_box)

        @seed_box.event('on_enter')
        def set_seed():
            self.level_stats.seed = self.ui_manager.find_by_id('seed_box').text

        self.create_input_box_mv('mv_chance_box', '20%', 'Value must be between 0 and 100%',
                                 [475, C.SCREEN_HEIGHT - 100, 500, 40], self.level_stats)

        self.create_input_box_mv('mv_chance_x', '50%', 'Value must be between 0 and 100%',
                                 [475, C.SCREEN_HEIGHT - 300, 500, 40], self.level_stats)

        self.create_input_box_mv('mv_chance_y', '50%', 'Value must be between 0 and 100%',
                                 [475, C.SCREEN_HEIGHT - 500, 500, 40], self.level_stats)

        mv_allowed_xy = UIFlatButton('True', 275, C.SCREEN_HEIGHT - 700, width=100, height=40, id='mv_allowed_xy')
        mv_allowed_xy.set_style_attrs(
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )
        self.ui_manager.add_ui_element(mv_allowed_xy)

        @mv_allowed_xy.event('on_click')
        def switch():
            button = self.ui_manager.find_by_id('mv_allowed_xy')
            if button.text == 'True':
                button.text = 'False'
                output = False
            else:
                button.text = 'True'
                output = True
            button.render()
            self.level_stats.mv_chance_xy = output
            print(self.level_stats.seed, self.level_stats.mv_chance, self.level_stats.mv_chance_x,
                  self.level_stats.mv_chance_y, self.level_stats.mv_chance_xy)

        max_gap = UIInputBox(975, C.SCREEN_HEIGHT - 100, 400, 40, '160', 'max_gap')

        self.ui_manager.add_ui_element(max_gap)

        @max_gap.event('on_enter')
        def update_gap():
            text_box = self.ui_manager.find_by_id('max_gap')
            try:
                gap = int(text_box.text)
                if not 30 < gap:
                    arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                    text_box.text = 'Must be over 30'
                    gap = 160
            except ValueError:
                arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                text_box.text = 'Must be an integer'
                gap = 160

            self.level_stats.max_gap = gap

        max_height = UIInputBox(975, C.SCREEN_HEIGHT - 300, 400, 40, '2500', 'max_height')

        self.ui_manager.add_ui_element(max_height)

        @max_height.event('on_enter')
        def update_height():
            text_box = self.ui_manager.find_by_id('max_height')
            try:
                height = int(text_box.text)
                if not 1500 < height:
                    arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                    text_box.text = 'Must be over 1500'
                    height = 2500
            except ValueError:
                arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                text_box.text = 'Must be an integer'
                height = 2500

            self.level_stats.max_height = height

        max_platforms = UIInputBox(975, C.SCREEN_HEIGHT - 500, 400, 40, '10', 'max_platforms')

        self.ui_manager.add_ui_element(max_platforms)

        @max_platforms.event('on_enter')
        def update_platforms():
            text_box = self.ui_manager.find_by_id('max_platforms')
            try:
                length = int(text_box.text)
                if not 0 < length:
                    arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                    text_box.text = 'Must be over 0'
                    length = 10
            except ValueError:
                arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                text_box.text = 'Must be an integer'
                length = 10

            self.level_stats.pl_num = length

        return_to_menu = UIFlatButton('BACK', 1400, 100, 150, 50, id='return')

        return_to_menu.set_style_attrs(
            border_color_hover=arcade.color.WHITE,
            border_color_press=arcade.color.WHITE
        )

        self.ui_manager.add_ui_element(return_to_menu)

        @return_to_menu.event('on_click')
        def return_to_menu():
            pickle_out = open('data/settings.info', 'wb')
            pickle.dump(self.level_stats, pickle_out)
            pickle_out.close()
            self.ui_manager.purge_ui_elements()
            self.window.show_view(MainMenu(self.window))

    def create_input_box_mv(self, id, base_text, error_text, position, level_stats):
        mv_chance_box = UIInputBox(position[0], position[1], position[2], position[3], base_text, id)

        self.ui_manager.add_ui_element(mv_chance_box)

        @mv_chance_box.event('on_enter')
        def get_mv_chance():
            mv_chance = self.ui_manager.find_by_id(id).text
            mv_chance = mv_chance.replace('%', '')
            try:
                mv_chance = float(mv_chance) / 100
                if not 0 <= mv_chance <= 1:
                    arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                    self.ui_manager.find_by_id(id).text = error_text
                    mv_chance = 0.2
            except ValueError:
                arcade.play_sound(arcade.load_sound(resource_path('sounds/erro.mp3')), 0.05)
                self.ui_manager.find_by_id(id).text = error_text
                mv_chance = 0.2
            if id == 'mv_chance':
                self.level_stats.mv_chance = mv_chance
            elif id == 'mv_chance_x':
                self.level_stats.mv_chance_x = mv_chance
            elif id == 'mv_chance_y':
                self.level_stats.mv_chance_y = mv_chance

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text('Seed:', 25, C.SCREEN_HEIGHT - 50, arcade.color.WHITE, 30)
        arcade.draw_text('Global moving platform chance:', 225, C.SCREEN_HEIGHT - 50, arcade.color.WHITE, 30)
        arcade.draw_text('Chance of X-axis movement:', 225, C.SCREEN_HEIGHT - 250, arcade.color.WHITE, 30)
        arcade.draw_text('Chance of Y-axis movement:', 225, C.SCREEN_HEIGHT - 450, arcade.color.WHITE, 30)
        arcade.draw_text('Are XY movements allowed:', 225, C.SCREEN_HEIGHT - 650, arcade.color.WHITE, 30)
        arcade.draw_text('Set the maximum gap between platforms:', 775, C.SCREEN_HEIGHT - 50, arcade.color.WHITE, 30)
        arcade.draw_text('Set the maximum height of the final platform:', 775, C.SCREEN_HEIGHT - 250,
                         arcade.color.WHITE, 30)
        arcade.draw_text('Set the maximum length of the platforms:', 775, C.SCREEN_HEIGHT - 450,
                         arcade.color.WHITE, 30)
        arcade.draw_text('Textbox values require ENTER to be pressed to be set.', 25, 25, arcade.color.WHITE, 30)

    def on_show_view(self):
        self.setup()


class Victory(arcade.View):

    def __init__(self, window: arcade.Window):
        super().__init__()
        self.window = window

    def setup(self):
        self.window.set_viewport(0, C.SCREEN_WIDTH, 0, C.SCREEN_HEIGHT)

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            'You beat the game!\nDamn, I\'m impressed.\nI really didn\'t think you\'d make it this far.\nBut since you did...\nWell good job!\n\nMade by: FalconFX9\nMusic and sounds by: FalconFX9\nTextures by: Zack Alvarado (OpenGameArt.org)\n\n\nESC to go back to main menu.',
            self.window.width // 2, self.window.height // 2, arcade.color.GOLD, 40, anchor_x='center',
            anchor_y='center')

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ESCAPE:
            self.window.show_view(MainMenu(self.window))


def main():
    window = arcade.Window(C.SCREEN_WIDTH, C.SCREEN_HEIGHT, C.TITLE, update_rate=1 / 120)
    window.show_view(MainMenu(window))
    arcade.run()


if __name__ == '__main__':
    main()
