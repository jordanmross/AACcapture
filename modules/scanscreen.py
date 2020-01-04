#!/usr/bin/env python

from modules.screenbase import ScreenBase
import sane
from PIL import Image
from time import sleep
from modules.popup import MyPopup
from kivy.lang.builder import Builder

kv_popupstring = """
GridLayout:
    orientation: 'vertical'
    name: 'pops'
    height: '300'
    padding: '100dp'
    cols: 1
    rows: 4
    padding: 10
    spacing: 10

    Label:
        id: text_stage
        text: 'Stage 0'
        

    Label:
        id: text_progress
        text: '100% not started'
        

    ProgressBar:
        id: prog_main
        value: 0
        max: 100
        
        
    Button:
        id: button_cancel
        size_hint_y: None
        height: '30dp'
        width: '100dp'
        text: 'Cancel'
        font_size: 20
        on_release: root.cancel()"""

from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar


from kivy.clock import Clock, _default_time as time  # ok, no better way to use the same clock as kivy, hmm
from threading import Thread
from time import sleep

from enum import Enum


MAX_TIME = 1/60.

class ScanBgWorkerStates(Enum):
    Errored = -1
    Invalid = 0
    Initializing = 1
    Scanning = 2
    Creating_preview = 3
    Saving = 4
    Stopped = 5

    def __str__(self):
        return self.name

class StateHolder:
    state = ScanBgWorkerStates(0)
    state_pct = None

    def __init__(self, state, state_pct = None):
        self.state = state
        self.state_pct = state_pct

class ScanBgWorker():
    state = StateHolder(ScanBgWorkerStates.Invalid)
    
    def run(self, wait = False, progress = None):
        ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Initializing)
        
        do_progress = False
        if progress != None:
            if not callable(progress):
                raise Exception('progress when provided must be callable.')
            do_progress = True

        Thread(target=self.worker).start()

        if wait:
            while not ScanBgWorker.state.state == ScanBgWorkerStates.Stopped:
                if(time() < (Clock.get_time() + MAX_TIME)):
                    continue
                if do_progress:
                    progress(ScanBgWorker.state)
        else:
            if do_progress:
                ScanBgWorker.progress = progress
                ScanBgWorker.event = Clock.schedule_interval(self.consume, 0)

    def consume(self, *args):
        if (ScanBgWorker.state.state == ScanBgWorkerStates.Stopped):
            #TODO add if errored
            ScanBgWorker.event.cancel()
            ScanBgWorker.progress(ScanBgWorker.state)
            return

        while time() < (Clock.get_time() + MAX_TIME):
            ScanBgWorker.progress(ScanBgWorker.state)

    def scan_progress(a, b):
        curstate_pct=int((a/b)*100)

        if ScanBgWorker.state != ScanBgWorkerStates.Scanning or (not ScanBgWorker.state.state_pct is None and curstate_pct > ScanBgWorker.state.state_pct):
            ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Scanning, state_pct=int((a/b)*100))
           
    def worker(self):

        #
        # Change these for 16bit / grayscale scans
        #
        depth = 8
        mode = 'color'

        #
        # Initialize sane
        #
        #print(sane.version())
        ver = sane.init()
        print('SANE version:', ver)

        #
        # Get devices
        #
        devices = sane.get_devices()
        print('Available devices:', devices)

        

        #
        # Open first device
        #
        dev = sane.open(devices[0][0])

        # 
        # Set scan resolution to 600 DPI
        #
        dev.resolution=600

        #
        # Set some options
        #
        params = dev.get_parameters()
        try:
            dev.depth = depth
        except:
            print('Cannot set depth, defaulting to %d' % params[3])

        try:
            dev.mode = mode
        except:
            print('Cannot set mode, defaulting to %s' % params[0])

        # try:
        #     dev.br_x = 320.
        #     dev.br_y = 240.
        # except:
        #     print('Cannot set scan area, using default')

        params = dev.get_parameters()
        print('Device parameters:', params)

        #
        # Start a scan and get and PIL.Image object
        #
        ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Scanning)
        dev.start()
        im = dev.snap(progress=ScanBgWorker.scan_progress)
        

        ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Saving, state_pct=0)

        #
        # Rotate Image 90 *
        #
        im = im.transpose(Image.ROTATE_90)

        #
        # Save the full image
        #
        im.save('full.png', compress_level=1)

        ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Saving, state_pct=50)

        #
        # Resize for preview and save save
        #
        im.resize((885,636)).save('test_pil.png', compress_level=1)
        
        ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Saving, state_pct=100)

        #
        # close the scanner device
        #
        dev.close()

        ScanBgWorker.state = StateHolder(ScanBgWorkerStates.Stopped)

        #TODO make sure thread is dead


class MyPopup():
    
    def A(self):
        contents = Builder.load_string(kv_popupstring)



        # create content and add to the popup
        
        self.popup = Popup(title="Progress", content=contents, auto_dismiss=False, size_hint = (None, None), size=(500, 300))

        # bind the on_press event of the button to the dismiss function
        #content.bind(on_press=popup.dismiss)

        # open the popup
        self.popup.open()

    def cancel(self):
        #TODO: set this to call cancel function, don't just dismiss
        self.popup.dismiss()

class ScanScreen(ScreenBase):

    def doPopup(self):
        
        self.contents = Builder.load_string(kv_popupstring)

        # create content and add to the popup
        
        self.popup = Popup(title="Progress", content=self.contents, auto_dismiss=False, size_hint = (None, None), size=(500, 300))

        # bind the on_press event of the button to the dismiss function
        #content.bind(on_press=popup.dismiss)

        # open the popup
        self.popup.open()

    def cancel(self):
        self.popup.dismiss()

    def doScan(self): 
        worker = ScanBgWorker()

        self.doPopup()
        
        worker.run(progress=self.on_progress)
        
        

    def on_progress(self, state):
        self.contents.ids.text_stage.text = str(state.state)

        if not state.state_pct is None:
            self.contents.ids.text_progress.text = str(state.state_pct)
            self.contents.ids.prog_main.value = state.state_pct

        if state.state == ScanBgWorkerStates.Stopped:
            
            self.popup.dismiss()

            # Go to the next screen (preview)
            self.go_next_screen()
            print('done')
