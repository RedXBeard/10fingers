from copy import copy
from datetime import datetime
from random import shuffle

from kivy import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import BooleanProperty, Clock, StringProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

from dictionary import DICTIONARY
from utils import find_parent, write_text, check_char, check_wordish, get_char, DB


ERROR = '#FF0000'
SUCCESS = '#008000'
BLACK = '#000000'


class TenFingerInputText(TextInput):
    is_forward = True
    is_focusable = True
    unfocus_on_touch = False
    text_validate_unfocus = False

    def __init__(self, **kwargs):
        super(TenFingerInputText, self).__init__(**kwargs)
        self.error = False

    def detect_correct_word(self):
        if not self.error and self.text[-1] == ' ':
            root = find_parent(self, TenFingersPlay)
            root.score += 1
            root.original_text = ''.join(root.original_text.split(' ', 1)[1:])
            root.initial_index = 0
            self.text = ''
            write_text(root)

    def on_parent(self, widget, parent):
        self.focus = True

    def insert_text(self, substring, from_undo=False):
        root = find_parent(self, TenFingersPlay)

        if check_char(get_char(root.original_text, root.initial_index), substring) and not self.error:
            write_text(root, SUCCESS)
            if not self.is_forward:
                self.is_forward = True
            root.initial_index += 1
            self.error = False
        else:
            self.error = True
            write_text(root, ERROR)
        super(TenFingerInputText, self).insert_text(substring, from_undo=from_undo)
        self.detect_correct_word()
        self.focus = True

    def do_backspace(self, from_undo=False, mode='bkspc'):
        try:
            super(TenFingerInputText, self).do_backspace(from_undo=from_undo, mode='bkspc')
        except IndexError:
            return
        root = find_parent(self, TenFingersPlay)
        if self.is_forward:
            self.is_forward = False
        if not self.error:
            root.initial_index = max(0, root.initial_index-1)

        if not root.original_text[:root.initial_index]:
            color = BLACK
            self.error = False
        elif check_wordish(root.original_text[:root.initial_index+1], self.text):
            color = SUCCESS
            self.error = False
        else:
            color = ERROR
            self.error = True
        write_text(root, color)
        self.focus = True


class TenFingers(ScreenManager):
    best_score = StringProperty()
    last_score = StringProperty()

    def __init__(self, **kwargs):
        super(TenFingers, self).__init__(**kwargs)
        self.base_screens = copy(self.screens)
        self.best()
        self.last()

    def best(self):
        DB.store_load()
        self.best_score = str(max(*list(filter(lambda x: isinstance(x, int), DB._data.values()))))

    def last(self):
        key = str(sorted(list(map(lambda x: float(x), filter(
            lambda x: x[0].isdigit(), DB.keys()))), reverse=True)[0])
        self.last_score = str(DB.store_get(key))

    def switch_play_window(self, direction='left'):
        screen = self.base_screens[1]
        self.switch_to(screen, direction=direction)
        self.current_screen.children[0].prepare_screen()

    def switch_final_window(self, direction='left'):
        screen = self.base_screens[2]
        self.switch_to(screen, direction=direction)

    def switch_welcome_window(self, direction='left'):
        screen = self.base_screens[0]
        root = find_parent(self, TenFingers)
        self.switch_to(screen, direction=direction)
        root.play.children[0].game_on = False
        self.best()
        self.last()


class TenFingersPlay(GridLayout):
    game_on = BooleanProperty(False)
    game_at = None
    score = 0

    initial_index = 0

    def __init__(self, **kwargs):
        super(TenFingersPlay, self).__init__(**kwargs)
        self.original_text = ''

    def counter(self):
        if self.game_on:
            time_diff = datetime.now() - self.game_at
            self.game_since.text = str(time_diff).rsplit(".", 1)[0][3:]
            if time_diff.total_seconds() >= 60:
                root = find_parent(self, TenFingers)
                root.switch_final_window()
                DB.store_put(datetime.now().timestamp(), self.score)
                DB.store_sync()
                root.current_screen.children[0].score.text = '{} wpm'.format(self.score)
            else:
                Clock.schedule_once(lambda dt: self.counter(), .1)

    def prepare_screen(self):
        dictionary = DICTIONARY.get('TR')
        shuffle(dictionary)
        self.original_text = '. '.join(dictionary)
        prev = self.original_text[:0]
        rest = self.original_text[1:]
        self.upcoming_text.text = "{0}[u]{2}[/u]{1}".format(
            prev, rest, self.original_text[0],
        )
        self.input_text.text = ''
        self.game_on = True
        self.game_at = datetime.now()
        self.score = 0
        self.counter()

    def direct_welcome_screen(self, direction='left'):
        root = find_parent(self, TenFingers)
        root.switch_welcome_window(direction=direction)


class TenFingersApp(App):
    def __init__(self, **kwargs):
        super(TenFingersApp, self).__init__(**kwargs)
        Builder.load_file('assets/10fingers.kv')
        self.title = 'Kivy 10 Fingers'
        # self.icon = 'assets/10fingers.ico'

        # def _image_loaded(self, proxyImage):
        #     if proxyImage.image.texture:
        #         self.image.texture = proxyImage.image.texture

    def build(self):
        ten_fingers = TenFingers()
        return ten_fingers

    # def ping_google(self):
    #     time.sleep(12)
    #     print(1)
    #     self.app_version_checker()
    #
    # def app_version_checker(self):
    #     time.sleep(12)
    #     print(2)
    #     self.vocab_version_checker()
    #
    # def vocab_version_checker(self):
    #     time.sleep(12)
    #     print(3)


if __name__ == '__main__':
    Config.set('kivy', 'desktop', 1)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Window.clearcolor = get_color_from_hex('E2DDD5')
    Window.size = 600, 600
    TenFingersApp().run()
