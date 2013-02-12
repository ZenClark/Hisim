import gui
from gui.WidgetGen import Label, ButtonArray

class StartMenu(object):
    def Quit(self):
        self.parent.quit()
    
    def Start(self):
        print 'Beginning new game'
    
    def __init__(self, parent):
        
        self._list = []
        self._list.append(('Quit', lambda obj: self.Quit()))
        self._list.append(('Start New Game', lambda obj: self.Start()))
        self.array = ButtonArray(list=self._list)
        
        return
        
