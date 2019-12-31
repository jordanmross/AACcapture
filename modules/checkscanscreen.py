from modules.screenbase import ScreenBase

class CheckScanScreen(ScreenBase):

    def on_pre_enter(self):
        self.ids.image.reload()