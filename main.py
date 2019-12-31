from modules.parentnamescreen import ParentNameScreen
from modules.capsule import Capsule
from modules.navigation import Navigation
from modules.screenbase import ScreenBase
from modules.scanscreen import ScanScreen
from modules.checkscanscreen import CheckScanScreen
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
# from wifimgr import WifiInterface
from kivy.uix.image import Image, AsyncImage
from time import sleep
from kivy.uix.settings import SettingsWithSidebar
from PIL import Image


class AACCaptureScreen(ScreenBase):
    fullscreen = BooleanProperty(False)
    
    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(AACCaptureScreen, self).add_widget(*args)


class AACCaptureApp(App):
    capsule = Capsule()
    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        # config = self.config
        self.title = 'hello world'

        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.

        self.settings_cls = SettingsWithSidebar

        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = [
            'Start', 'ParentName', 'ShippingAddress', 'ParentEmail', 'GridSize',
            'Instructions', 'Capture', 'ImageCheck', 'Confirmation']
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'data', 'screens',
             '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        #self.hide_widget(self.root.ids.sourcecode)
        self.go_next_screen()

    def getserial(self):
        #Extract serial from cpuinfo file
        cpuserial = "0000000000000000"
        try:
          f = open('/proc/cpuinfo','r')
          for line in f:
            if line[0:6]=='Serial':
              cpuserial = line[10:26]
          f.close()
        except:
          cpuserial = "ERROR000000000"
        return cpuserial

    def fill_address(self):
        pass
    
    def rotate_image(self):
        img = Image.open("/home/pi/AACcapture/data/captures/capture.jpg")
        img = img.rotate(180)
        img.save("/home/pi/AACcapture/data/captures/capture.jpg")

    def resize_image(self):
        img = Image.open('/home/pi/AACcapture/data/captures/capture.jpg')
        new_img = img.resize((400,300))
        new_img.save("/home/pi/AACcapture/data/captures/lowrescapture.jpg", "JPEG", optimize=True)

    def build_config(self, config):
        config.setdefaults('Clinic', {
            'name': '',
            'address1': '',
            'address2': '',
            'city': '',
            'state': '',
            'zip': 00000})
        config.setdefaults('Device', {
            'deviceid': self.getserial()
        })

        
    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        
        settings.add_json_panel('Clinic', self.config, 'clinic_settings.json')
        settings.add_json_panel('Wifi', self.config, 'wifi_settings.json')
        # settings.add_json_panel('section2', self.config, data=json)

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        #self.update_sourcecode()

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        #self.update_sourcecode()    

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])

        if issubclass(type(screen), ScreenBase):
            screen.navigation = self
            screen.capsule = self.capsule

        self.screens[index] = screen
        return screen

    def _update_clock(self, dt):
        self.time = time()
        
if __name__ == '__main__':
    AACCaptureApp().run()
