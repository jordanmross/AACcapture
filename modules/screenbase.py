#from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from modules.navigation import Navigation
from modules.capsule import Capsule

class ScreenBase(Screen, Navigation):
    navigation = Navigation()
    capsule = Capsule()

    print(navigation)

    # Call the load and unload functions
    def on_pre_enter(self):
        self.load()
    def on_pre_leave(self):
        self.unload()

    def load(self):
        pass #load data from screen here

    def unload(self):
        pass

    def check_can_next(self):
        return True
        
    def go_next_screen(self):
        self.navigation.go_next_screen()
    def go_previous_screen(self):
        self.navigation.go_previous_screen()