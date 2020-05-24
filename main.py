from random import shuffle

from kivy import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex

from dictionary import DICTIONARY
from utils import find_parent, write_text, check_char, check_wordish

ERROR = '#FF0000'
SUCCESS = '#008000'
BLACK = '#000000'


class TenFingerInputText(TextInput):
    is_forward = True

    def __init__(self, **kwargs):
        super(TenFingerInputText, self).__init__(**kwargs)
        self.error = False

    def detect_correct_word(self):
        if not self.error and self.text[-1] == ' ':
            root = find_parent(self, TenFingers)
            root.original_text = ''.join(root.original_text.split(' ', 1)[1:])
            root.initial_index = 0
            self.text = ''
            write_text(root)

    def on_parent(self, widget, parent):
        self.focus = True

    def insert_text(self, substring, from_undo=False):
        root = find_parent(self, TenFingers)
        if check_char(root.original_text[root.initial_index], substring) and not self.error:
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
        super(TenFingerInputText, self).do_backspace(from_undo=from_undo, mode='bkspc')
        root = find_parent(self, TenFingers)
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


class TenFingers(GridLayout):
    initial_index = 0
    dictionary = DICTIONARY.get('TR')
    shuffle(dictionary)
    original_text = '. '.join(dictionary)

    def __init__(self, *args, **kwargs):
        super(TenFingers, self).__init__(*args, **kwargs)
        prev = self.original_text[:0]
        rest = self.original_text[1:]
        self.upcoming_text.text = "{0}[u]{2}[/u]{1}".format(
            prev, rest, self.original_text[0],
        )


class TenFingersApp(App):
    def __init__(self, **kwargs):
        super(TenFingersApp, self).__init__(**kwargs)
        Builder.load_file('assets/10fingers.kv')
        self.title = 'Kivy 10 Fingers'
        # self.icon = 'assets/10fingers.ico'

    def build(self):
        ten_fingers = TenFingers()
        return ten_fingers


if __name__ == '__main__':
    Config.set('kivy', 'desktop', 1)
    Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
    Window.clearcolor = get_color_from_hex('E2DDD5')
    Window.size = 600, 600
    TenFingersApp().run()
