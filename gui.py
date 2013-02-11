import pygame, threading
from hexagon.hexbase import HexagonMap
import events


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

        pygame.display.flip()

    def AddWidget(self, widget):
        if widget not in self._widgets:
            self._widgets.append(widget)
            return True
        else:
            return False

    def RemoveWidget(self, widget):
        if widget in self._widgets:
            #self._widgets.remove(widget)
            del self._widgets[self._widgets.index(widget)]
            return True
        else:
            return False

class pygameWidget(object):
    def __init__(self, parent, image, x, y, name='Unnamed Widget'):
        self.parent = parent
        self.screen = parent.screen
        self.image = image
        self.x = x
        self.y = y
        self.active = False
    
        self.name = name
        
        self.eventType = None
        
        
    def __del__(self):
        self.deactivate()
        
    def activate(self):
        self.activate = True
        return

    def deactivate(self):
        self.activate = False

    def draw(self):
        if self.active:
            self.screen.blit(self.image, (self.x, self.y))
    
    def Within(self, x, y):
        if self.x < x and x < self.x+self.image.get_width():
            if self.y < y and y <self.y+self.image.get_height():
                return True
        return False

class pygameButton(pygameWidget):
    def clicky(self):
        """ Debugging function for non-button widgets"""
        
        print self.name            
    
    def __init__(self, parent, image, x, y, name='Unnamed Button', OnClick=None):
        super(pygameButton, self).__init__(parent, image, x, y, name=name)
        
        self.eventType = pygame.MOUSEBUTTONUP
        self.active = True
        
        if OnClick is None:
            self.OnClick = self.clicky
        else:
            self.OnClick = lambda: OnClick(self)

    def __del__(self):
        self.parent.parent.guimanager.remove(self)
        self.deactivate

    def draw(self):
        if self.active:
            self.screen.blit(self.image, (self.x, self.y))
    
    def Within(self, x, y):
        if self.x < x and x < self.x+self.image.get_width():
            if self.y < y and y <self.y+self.image.get_height():
                return True
        return False
        
class LabelWidget(pygameWidget):
    def __init__(self, parent, text, x, y, name='Unnamed Label'):
        
        self.y = y
        self.name = name
        self.parent = parent
        self.screen = parent.screen
        self.eventType = None

        self.font = pygame.font.Font(pygame.font.get_default_font(),18)
        self.text = text
        
        self.image = self.font.render(self.text, True, (0xff, 0xff, 0xff))
        self.x = x - self.image.get_width()/2

        self.active = True

    @staticmethod
    def GenerateLabel(text):
        """ 
        A static method that generates and returns a text image without creating a full label widget
        :param string text: The text for the label to display 
        
        """
        font = pygame.font.Font(pygame.font.get_default_font(),18)
        return font.render(text, True, (0xff, 0xff, 0xff))

class WidgetGen(object):
    @staticmethod
    def Label(text):
        """ 
        A static method that generates and returns a text image without creating a full label widget
        :param string text: The text for the label to display 
        
        """
        font = pygame.font.Font(pygame.font.get_default_font(),18)
        return font.render(text, True, (0xff, 0xff, 0xff))

    @staticmethod
    def ButtonArray(parent, list={}, (x, y)=(0, 0)):
        widgets = []
        for choice in list.items():
            text = choice[0]
            image = WidgetGen.Label(text)
            func = choice[1]
            button = pygameButton(parent, image, x, y, OnClick=func, name=text)
            widgets.append(button)
            y += 20
            
        return widgets
            
class RootForm(pygameForm):   
    def begin(self):
        self.name = 'RootForm'
        self.background = self.parent.tileSet[0][0]
        
        centerScreen = self.screen.get_width()/2
        
        #self.AddWidget(pygameButton(self, self.background, 0, 0, name='Widget One'))
        #self.AddWidget(pygameButton(self, self.parent.tileSet[0][1], 38, 0, name='Widget Two'))
        #self.AddWidget(LabelWidget(self, 'Welcome to the Hisim Engine', centerScreen, 0, name='LabelOne'))
        #self.AddWidget(LabelWidget(self, 'Sorry, but no content at the moment.', centerScreen, 20, name='LabelTwo'))
            
        widgets = {}
        for i in range(3):
            def pname(obj):
                print "I am called " + obj.name
            widgets['{0}: I am {0}'.format(str(i))] = lambda obj: pname(obj)

        wid = WidgetGen.ButtonArray(self, list=widgets)
        for i in range(wid.__len__()):
            self.AddWidget(wid[i])
        f = lambda x: self.RemoveWidget(wid[1])
        lbl = LabelWidget.GenerateLabel('Remove')
        
        self.AddWidget(pygameButton(self, lbl, centerScreen, 260, name='RemoveButton', OnClick=f))
        
        lbl = LabelWidget.GenerateLabel('Quit')
        quit = lambda  obj: self.parent.quit()
        self.AddWidget(pygameButton(self, lbl, centerScreen, 240, name='QuitButton', OnClick=quit))
        
        del lbl
        
        self.parent.guimanager.append(self._widgets, 0)

class GUI(object):
    def quit(self):
        self.status = False
        #self.eventmanager.Off()
        self.guimanager.Off()
        pygame.display.quit()
        return
    
    def statusGet(self):
        with self.StatusLock:
            status = self._status
        return status
    
    def statusSet(self, y):
        with self.StatusLock:
            self._status = y
    
    def statusDel(self):
        with self.StatusLock:
            del self._status 
        return
    
    status = property(statusGet, statusSet, statusDel, 'Thread safe status property')    
    
    def __init__(self):
        self._status = True
        self.StatusLock = threading.Lock()        
        pygame.init()    
        self.screen = pygame.display.set_mode((640, 480),1)
        self.clock = pygame.time.Clock()        
        
        self.evalStatus = lambda obj: obj.status
        
        #self.eventmanager = events.EventManager([])
        #self.quitEvent = events.Event(self.quit, self, self.evalStatus)
        
        self.guimanager = events.GuiManager(3)
        self.thread_guiManager = threading.Thread(target=self.guimanager.run, name='Event Manager')

        self.tileSet = []
        self.tileSet.append([])
        firstSet = ['./hexagon/hextile.png', './hexagon/hexcursor.png']
        for i in firstSet:
            self.tileSet[0].append(pygame.image.load(i).convert())
        
        self.root = RootForm(self.clock, self)

    def mainLoop(self):
        self.thread_guiManager.start()
        while self.status:
            self.root.draw(30)

        print 'Main Loop Terminated'
        pygame.quit()
        return

print __name__

if __name__ == '__main__':
        core = GUI()
        core.mainLoop()
