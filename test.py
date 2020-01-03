from kivy.app import App
from kivy.clock import Clock, _default_time as time  # ok, no better way to use the same clock as kivy, hmm
from kivy.lang import Builder
from kivy.factory import Factory
from kivy.uix.button import Button
from kivy.properties import ListProperty

from threading import Thread
from time import sleep

MAX_TIME = 1/60.

kv = '''
BoxLayout:
    ScrollView:
        GridLayout:
            cols: 1
            id: target
            size_hint: 1, None
            height: self.minimum_height

    MyButton:
        text: 'run'

<MyLabel@Label>:
    size_hint_y: None
    height: self.texture_size[1]
'''

class MyButton(Button):
    def on_press(self, *args):
        Thread(target=self.worker).start()

    def worker(self):
        sleep(5) # blocking operation
        App.get_running_app().consommables.append("done")

class PubConApp(App):
    consommables = ListProperty([])

    def build(self):
        Clock.schedule_interval(self.consume, 0)
        return Builder.load_string(kv)

    def consume(self, *args):
        while self.beep() and self.consommables and time() < (Clock.get_time() + MAX_TIME):
            item = self.consommables.pop(0)  # i want the first one
            label = Factory.MyLabel(text=item)
            self.root.ids.target.add_widget(label)

    def beep(self):
        print('h')
        return True

class StateHolder:
    state = 'invalid'

class ScanBg():
    states = {'running': 2, 'stopped': 0}
    state = 'stopped'
    
    def worker(self):
        sleep(5)
        print('working...')
        print('working...')
        print('working...')
        print('working...')
        print('working...')
        print('working...')
        print('working...')
        print('working...')
        print('working...')
        self.state = 'stopped'
        sleep(5)

    def run(self):
        sh = StateHolder()
        self.state = 'running'
        Thread(target=self.worker).start()

        while self.check(sh):
            if(time() < (Clock.get_time() + MAX_TIME)):
                continue
            self.showStatus(sh.state)

        print('here')
        self.showStatus(self.state)
        
    def check(self, stateHolder):
        stateHolder.state = self.state
        return stateHolder.state == 'running'

    def showStatus(self, safeState):
        print(safeState)

    def readStateSafe(self):
        return self.state


if __name__ == '__main__':
    ScanBg().run()