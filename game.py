import threading

import ruler
import army as army
import menu
from events import Event, EventManager
from land import Land

import generic

DEBUG = True
""" A boolean value that switches certain behaviors over to a debug setup. """

__doc__ = \
"""

    Core Module

    .. autoclass:: core
        :members:
        :undoc-members:
    
"""

__name__ = 'Game'

class core(object):
    __doc__ = \
    """

    Core management object class

    """

    def __init__(self):

        self._id = 'Core Object'
        
        self.territories = []
        self.generals = []
        self.rulers = []
        
        self.player = self.chargen()       
        
        genOne = ruler.general(self, 'Test General One',  master=self.player)
        rulerTwo = ruler.general(self, name='Nobunaga', isRuler=True)
        genTwo = ruler.general(self, 'Test General Two',  master=rulerTwo)        
        rulerThree = ruler.general(self, name='Viper', isRuler=True)
        genThree = ruler.general(self, 'Test General Three',  master=rulerThree)   
        
        self.territories.append(Land(self.player, 0, 'Player\'s land', generals=[self.player, genOne], governor=self.player, borders=[1, 2]))
        self.player.location = self.territories[0]        
        self.player.activeLocation = self.player.location       
        self.generals[1].location = self.player.location
        
        self.territories.aMenuListppend(Land(rulerTwo, 1, 'Owari', generals=[rulerTwo, genTwo], borders=[0, 2]))
        self.generals[2].location = self.territories[1]
        self.generals[3].location = self.territories[1]
        del rulerTwo
        
        self.territories.append(Land(rulerThree, 2, 'Mino', generals=[rulerThree, genThree], borders=[0, 1]))
        self.generals[4].location = self.territories[2]
        self.generals[5].location = self.territories[2]
        self.territories[2].population = 100000
        del rulerThree
        
        for i in range(self.generals.__len__()):
            if self.generals[i].isRuler and not self.generals[i].isPlayer:
                self.generals[i].AI.update()
        
        ### Testing for event manager, using a generic event object
        #self.eventManager = EventManager()
        #empty = generic.generic()
        #self.eventManager.AddHookHandler(self.handle, self, generic.eval)
        #self.thread_eventManager = threading.Thread(target=self.eventManager.run(), name='Event Manager')
        #self.thread_eventManager.start()

        print 'Character made'

        self.player.MenuList['Root'] = menu.RootMenu(self.player)
        self.player.MenuList['Root'].eval()

        end = raw_input('Enter anything to continue')

    def turn(self):
        for x in self.territories:
            if x.governor.checkLoyalty(self.player) :
                self.player.activeLocation = x
            
                for x in self.generals:
                    x.NextTurn()
                self.player.MenuList['Root'].eval()
        
    def next(self, territory):
        """
        
        Used for the player to pass to the next territory under their control

        :param territory: The player's current activeLocation
            
        """

        list = [] # List of player loyal governors
        for x in self.territories:
            if x.governor.checkLoyalty(self.player) :
                list.append(x)

        i = list.index(territory)
        length = list.__len__()
        if i == length-1 or length == 1:
            self.turn()
        else:
            self.player.activeLocation = list[i+1]
            self.player.MenuList['Root'].location = self.player.activeLocation

    def chargen(self):

            character = ruler.player(self)
            if DEBUG:
                character.name = 'Bob'
            
                return character

            test = False #Testing loop for name

            while test == False:

                name = raw_input('What is thy name?\n')

                ask = raw_input('You chose {0}, is that correct? (Y/n)\n'.format(name))

                test2 = False #Testing loop for confirmation of name
                while test2 == False:

                    if ask == 'Y':

                        print 'Welcome {0}, to this historical simulation.\n'.format(name)
                        test2 = True
                        test = True

                    elif ask == 'n':
                        del character
                        return self.chargen()

                    else:
                        ask = raw_input('Please use \'Y\' or \'n\' as an answer.\n') 

            character.name = name          

            return character

    def handle(self):
        print 'Core Event occurred'
