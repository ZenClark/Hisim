import pygame, threading
from hexagon.HexagonExample import HexagonMap
import events

thislock = threading.Lock()

def refresh():
    with thislock:
        pygame.display.flip()

class pygameForm():
    __doc__ = \
    """ 
    
    Base form class, which contains widgets, and possibly child forms. 
    
    :param pygame.time.clock clock: The topmost clock used by the program
    :param pygameForm parent: The parent form of this instance
    """
    
    def __init__(self, clock, parent):
        self.parent = parent
        self.screen = parent.screen
        self._widgets = []
        self.clock = clock
        self.begin()
    
    def begin(self):
        self.name = 'pygameForm'
        return #Generic form does nothing

    def draw(self, fps):

        self.screen.fill((0, 0, 0))
        for x in self._widgets:
            x.draw()
        
        self.clock.tick(fps)
            
        refresh()

    def AddWidget(self, widget):
        if widget not in self._widgets:
            self._widgets.append(widget)
            return True
        else:
            return False

    def RemoveWidget(self, widget):
        if widget in self._widgets:
            self._widgets.remove(widget)
            return True
        else:
            return False

class pygameWidget(object):
    def __init__(self, parent, image, x, y):
        self.parent = parent
        self.screen = parent.screen
        self.image = image
        self.x = x
        self.y = y
        self.test = False
        self.test2 = False
        eval = lambda obj: obj.test
        event = events.Event(self.testhandle, self, eval)
        self.parent.parent.eventm.append(event)
        self.timer = threading.Timer(7.0, self.testswitch)
        self.timer.start()
    
    def testswitch(self):
        del self.timer
        self.test = True
        self.timer = threading.Timer(7.0, self.testswitch)
        self.timer.start()

    def testhandle(self):
        #print 'blink'
        self.test = False
        self.test2 = not self.test2
        #refresh()
        return

    def draw(self):
        if self.test2:
            self.screen.blit(self.image, (self.x, self.y))
        
class RootForm(pygameForm):
    def begin(self):
        self.name = 'RootForm'
        self.background = self.parent.tileSet[0][0]
        self.AddWidget(pygameWidget(self, self.background, 0, 0))
        self.AddWidget(pygameWidget(self, self.parent.tileSet[0][1], 38, 0))
        
class GUI(HexagonMap):
    def __init__(self):
        
        super(GUI, self).__init__()
        
        self.eventm = events.EventManager([])
        self.thread_eventManager = threading.Thread(target=self.eventm.run, name='Event Manager')

        self.tileSet = []
        self.tileSet.append([])
        firstSet = ['./hexagon/hextile.png', './hexagon/hexcursor.png']
        for i in firstSet:
            self.tileSet[0].append(pygame.image.load(i).convert())
        
        self.root = RootForm(self.clock, self)

    def mainLoop(self):
        self.thread_eventManager.start()
        while 1:
            self.root.draw(30)

        return

print __name__

if __name__ == '__main__':
        core = GUI()
        core.mainLoop()
