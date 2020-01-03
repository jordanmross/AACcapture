from kivy.uix.popup import Popup
from kivy.uix.button import Button
from kivy.uix.progressbar import ProgressBar

class MyPopup():
    
    def A(self):

        # create content and add to the popup
        content = Button(text='Close me!')
        
        popup = Popup(content=content, auto_dismiss=False, size_hint = (None, None), size=(200, 200))

        # bind the on_press event of the button to the dismiss function
        content.bind(on_press=popup.dismiss)

        # open the popup
        popup.open()