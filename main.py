from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from wifimgr import WifiInterface
from kivy.uix.image import Image, AsyncImage
from picamera import PiCamera
from time import sleep


class AACCaptureApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])


    def build(self):
        self.title = 'hello world'
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        # self.screens = {}
        # self.available_screens = [
        #     'Start', 'Next','Capture']
        # self.screen_names = self.available_screens
        # curdir = dirname(__file__)
        # self.available_screens = [join(curdir, 'data', 'screens',
        #     '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        # #self.hide_widget(self.root.ids.sourcecode)
        # self.go_next_screen()

    def _update_clock(self, dt):
        self.time = time()
        
if __name__ == '__main__':
    AACCaptureApp().run()