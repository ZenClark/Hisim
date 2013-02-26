import threading
from gui import pygameForm, GUI, InputWidget, TextDisplayWidget, territoryDisplay
from gui_menu import StartMenu

class GUICore(pygameForm):
    def func(self, obj):
        self.tbox.Print(obj.value)
        if obj.value == 'Attack':
            self.territoryDisplay.changeOwnership(1, self.parent.core.player)
        obj.value = ''

    def begin(self):        
        self.name = 'GUICore'
        self.Menu = StartMenu(self)
        self.AddSet(self.Menu.array)
        self.AddWidget(InputWidget(self, '', (0, 420), name='textbox one', OnEnter= lambda obj: self.func(obj)))
        self.tbox = TextDisplayWidget(self, 'buffer', (0, 400))
        self.tbox.Print('Testing...')
        self.tbox.Print('Testing2...')
        self.tbox.Print('Testing3...')
        self.tbox.activate()
        self.AddWidget(self.tbox)  
        #self._widgets[2].activate()
        self.tbox.Print('Testing3...')
        self.territoryDisplay = territoryDisplay(self, 'lands')
        self.AddWidget(self.territoryDisplay)
        self.territoryDisplay.activate()
        return True
        
print __name__

