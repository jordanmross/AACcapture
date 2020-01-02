from modules.screenbase import ScreenBase

class ConfirmationScreen(ScreenBase):

    def load(self):
        parent = self.capsule.data.get("parent",{})
        parentname = parent.get('name', "")
        print(parentname)
        lblpn = 'Parent Name: %s' % parentname
        self.ids.label_parentname.text = lblpn

        