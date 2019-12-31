#from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from navigation import Navigation
from capsule import Capsule

class ScreenBase(Screen, Navigation):
    navigation = Navigation()
    capsule = Capsule()

    print(navigation)

    def load(self):
        pass #load data from screen here

    def close(self):
        pass

    def check_can_next(self):
        return True
        
    def go_next_screen(self):
        self.navigation.go_next_screen()
    def go_previous_screen(self):
        self.navigation.go_previous_screen()