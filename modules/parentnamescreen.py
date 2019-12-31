from modules.screenbase import ScreenBase

class ParentNameScreen(ScreenBase):

    def load(self):
        if 'parent' in self.capsule.data:
            self.capsule.data["parent"] = {}
        
        parent = self.capsule.data["parent"]

        self.ids.text_parentname.text = parent.name
    
    def close(self):
        parent = self.capsule.data["parent"]

        parent.name = self.ids.text_parentname.text

    def check_can_next(self):
        return self.ids.text_parentname.text is not None
        