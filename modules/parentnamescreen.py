from modules.screenbase import ScreenBase

class ParentNameScreen(ScreenBase):

    def load(self):
        if not 'parent' in self.capsule.data:
            self.capsule.data["parent"] = {}
        
        parent = self.capsule.data["parent"]
        print(parent)
        self.ids.text_parentname.text = parent["name"]
    
    def unload(self):
        parent = self.capsule.data["parent"]

        parent["name"] = self.ids.text_parentname.text

    def check_can_next(self):
        return self.ids.text_parentname.text is not None
        