from kivy import Config
from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.utils import get_color_from_hex
from random import shuffle

from dictionary import DICTIONARY

ERROR = '#FF0000'
SUCCESS = '#008000'


class TenFingerInputText(TextInput):
    def on_text(instance, value, vs):
        print('The widget', instance, 'value:', value, 'vs', vs)


class TenFingers(GridLayout):
    def __init__(self, *args, **kwargs):
        super(TenFingers, self).__init__(*args, **kwargs)
        self.dictionary = DICTIONARY.get('TR')
        shuffle(self.dictionary)
        self.upcoming_text.text = '[u][color={}]{}[/color][/u]'.format(ERROR, '. '.join(self.dictionary))


class TenFingersApp(App):
    def __init__(self, **kwargs):
        super(TenFingersApp, self).__init__(**kwargs)
        Builder.load_file('assets/10fingers.kv')
        self.title = '10Fingers'
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
