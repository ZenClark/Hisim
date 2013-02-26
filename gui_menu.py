#from generals import player
from gui import WidgetGen, LabelWidget, InputWidget
ButtonArray = WidgetGen.ButtonArray

class NewCharacter(object):
    def inputHandler(self, obj):
        if self.stage is 0:
            self.player_name = obj.value
            self.stage = 1
            self.parent.tbox.Print('Name of starting territory')
            
        elif self.stage is 1:
            self.territory_name = obj.value
            self.stage = 2
            
        obj.value = ''
        return
        
    def __init__(self, parent):
        self.parent = parent
        #self.array.append(InputWidget(self.parent, '', (parent.center[0], parent.center[1]+20), name='Player gen', OnEnter=lambda obj: self.inputHandler(obj)))
        self.parent.tbox.Print('Enter the name of your character')
        self.stage = 0

        self.player_name = ''
        self.territory_name = ''

    def Finished(self):
        if self.stage is 2:
            return (self.player_name, self.territory_name)
    
        else:
            return False

class StartMenu(object):
    def Quit(self):
        self.parent.parent.quit()
    
    def Start(self):
        print 'Beginning new game'
        self.start_choice = True
        
    def __init__(self, parent):
        self.parent = parent
        self._list = []
        self._list.append(('Quit', lambda obj: self.Quit()))
        self._list.append(('Start New Game', lambda obj: self.Start()))
        self.array = ButtonArray(parent, list=self._list)
        self.start_choice = False
        
        return
 
    def Finished(self):
        if self.start_choice:
            return NewCharacter(self.parent)
        else:
            return self.start_choice
