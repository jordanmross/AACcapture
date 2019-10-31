

from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty,\
    ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
#from wifimgr import WifiInterface
from kivy.uix.image import Image, AsyncImage
from picamera import PiCamera
from time import sleep
from kivy.uix.settings import SettingsWithSidebar


class AACCaptureApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])


    def build(self):
        #config = self.config
        self.title = 'hello world'
        
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = SettingsWithSidebar

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

    def getserial(self):
        # Extract serial from cpuinfo file
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

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        #     settings.add_json_panel('My Label', self.config, 'settings.json')
        
        settings.add_json_panel('Clinic', self.config, 'clinic_settings.json')
        #settings.add_json_panel('section2', self.config, data=json)

    def _update_clock(self, dt):
        self.time = time()
        
if __name__ == '__main__':
    AACCaptureApp().run()