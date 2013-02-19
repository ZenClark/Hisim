#from generals import player
from gui import WidgetGen, LabelWidget, InputWidget
ButtonArray = WidgetGen.ButtonArray

class StartMenu(object):
    def Quit(self):
        self.parent.parent.quit()
    
    def Start(self):
        print 'Beginning new game'
    
    def __init__(self, parent):
        self.parent = parent
        self._list = []
        self._list.append(('Quit', lambda obj: self.Quit()))
        self._list.append(('Start New Game', lambda obj: self.Start()))
        self.array = ButtonArray(parent, list=self._list)
        
        return
        
class NewCharacter(object):
    def inputHandler(self, obj):
        self.player = obj.value
        obj.value = 0
        return
        
    def __init__(self, parent):
        self.parent = parent
        self.array = []
        self.array.append(InputWidget(self.parent, 'Name', parent.center, name='Player name', OnEnter=lambda obj: self.inputHandler(obj)))
        self.array.append(LabelWidget(self.parent, 'Creating a new character', (parent.center[0], 0), name='Title'))

        self.player = player
