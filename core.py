from generals import General, Player
from territory import GenericLand
from gui import GUI
from gui_core import GUICore

class GameCore(object):
    def __init__(self):
        self.territories = []
        self.generals = []
        self.rulers = []
        self.player = Player(self)
        self.player.name = 'Bob'
        self.player.color = color=(255, 255, 0, 255)
        
        self.territories.append(GenericLand(self.player, 0, 'Bob land' ))
        self.territories.append(GenericLand(General(self, name='R2', id=1), 1, 'R2 land'))
        #self.territories.append(GenericLand(General(self, name='R3', id=2)), 2, 'R3 land')
        
        self.GUI = GUI(GUICore, self)
        for item in self.territories:
            self.GUI.root.territoryDisplay.changeOwnership(item.id, item.owner)
        #self.GUI.root.AddWidget(self.GUI.root.territoryDisplay)
        #self.GUI.root.territoryDisplay.activate()

    def begin(self):
        self.GUI.mainLoop()
        return
        
