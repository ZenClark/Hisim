import pygame, threading, pickle, os
from hexagon.hexbase import HexagonMap
import events

class pygameForm():
    __doc__ = \
    """ 
    
    Base form class, which contains widgets, and possibly child forms. 
    
    :param pygame.time.clock clock: The topmost clock used by the program
    :param pygameForm parent: The parent form of this instance
    """
    
    def __init__(self, clock, parent, manager=None):
        self.parent = parent
        self.screen = parent.screen
        self.center = (self.screen.get_width()/2, self.screen.get_height()/2)
        if manager is not None:
            self.manager = manager
        else:
            self.manager = parent.guimanager
        self._widgets = []
        self.clock = clock
        self.name = 'pygameForm'
        self.begin()
    
    def begin(self):
        return #Generic form does nothing

    def draw(self, fps):

        self.screen.fill((50, 0, 0))
        for x in self._widgets:
            x.draw()
        
        self.clock.tick(fps)

        pygame.display.flip()

    def AddWidget(self, widget):
        if widget not in self._widgets:
            self._widgets.append(widget)
            self.manager.append(item=widget)
            return True
        else:
            return False

    def AddSet(self, list):
        if list is not None:
            for item in list:
                self.AddWidget(item)

    def RemoveWidget(self, widget):
        if widget in self._widgets:
            self._widgets.remove(widget)
            self.manager.remove(widget)
            
            return True
        else:
            return False
            
    def RemoveSet(self, list):
        if list is not None:
            for item in list:
                self._widgets.remove(item)
                self.manager.remove(item)

class pygameWidget(object):
    
    def setActive(self, y):
        with self.Lock:
            self._active = y
    
    def getActive(self):
        with self.Lock:
            return self._active
    
    def __init__(self, parent, image, (x, y), name='Unnamed Widget'):
        self.parent = parent
        self.screen = parent.screen
        self.image = image
        self.x = x
        self.y = y
        self._active = False
        self.active = property(self.getActive, self.setActive)
        self.Lock = threading.Lock()
    
        self.name = name
        
        self.eventTypes = []
        
    def activate(self):
        self.active = True
        return

    def deactivate(self):
        self.active = False
        return

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
    
    def __init__(self, parent, image, (x, y), name='Unnamed Button', OnClick=None):
        super(pygameButton, self).__init__(parent, image, (x, y), name=name)
        
        self.eventTypes = [pygame.MOUSEBUTTONUP]
        self.active = True
        
        if OnClick is None:
            self.OnClick = self.clicky
        else:
            self.OnClick = lambda: OnClick(self)

    def register(self):
        self.parent.parent.guimanager.append(item=self)

    def deregister(self):
        self.parent.parent.guimanager.remove(self)

    def draw(self):
        if self.active:
            self.screen.blit(self.image, (self.x, self.y))
    
    def Within(self, x, y):
        if self.x < x and x < self.x+self.image.get_width():
            if self.y < y and y <self.y+self.image.get_height():
                return True
        return False
        
class LabelWidget(pygameWidget):
    def __init__(self, parent, text, (x, y), name='Unnamed Label'):
        
        self.y = y
        self.name = name
        self.parent = parent
        self.screen = parent.screen
        self.eventTypes = []

        self.font = pygame.font.Font(pygame.font.get_default_font(),18)
        self.text = text
        
        self.image = self.font.render(self.text, True, (0xff, 0xff, 0xff))
        self.x = x - self.image.get_width()/2

        self.active = True

    def changeText(self, txt):
        self.text = txt
        self.image = self.font.render(self.text, True, (0xff, 0xff, 0xff))
        self.x = x - self.image.get_width()/2

class TextDisplayWidget(pygameWidget):
    def __init__(self, parent, text, (x, y), name='Unnamed Text Display Widget'):
        super(TextDisplayWidget, self).__init__(parent, None, (x, y), name=name)
        self.box = (600, 200)
        self.x = x
        self.y = y
        self.background = pygame.Rect(x, y, self.box[0], self.box[1])
        self.font = pygame.font.Font(pygame.font.get_default_font(),18)
        self.buffer = []
        self.lines = []
        self.line_size = self.font.get_linesize()
        self.lines_max = self.box[1]//self.line_size
        self.bufferSize = 300
        for x in range(self.bufferSize):
            self.buffer.append(WidgetGen.Label(''))

    def Print(self, text=''):
        self.lines.insert(0, WidgetGen.Label(text))
        self.buffer.insert(0, WidgetGen.Label(text))
        if self.lines.__len__() >= self.lines_max:
            del self.lines[self.lines.__len__()-1]
        if self.buffer.__len__() >= self.bufferSize:
            del self.buffer[self.buffer.__len__()-1]
    
    def Output(self, index=None):
        if index is None:
            index = self.bufferSize
            
        for i in range(self.lines_max):
            self.lines[self.lines_max - i] = self.buffer[index + i]
            
    def draw(self):
        if self.active:
            for i in range(self.lines_max):
                self.screen.blit(self.buffer[i], (self.x, self.y-((i+1)*self.line_size)))
            
class InputWidget(pygameWidget):
    def __init__(self, parent, text, (x, y), name='Unnamed Input', OnEnter=None):
        image = WidgetGen.Label(text)
        super(InputWidget, self).__init__(parent, image, (x, y), name=name)
        
        if OnEnter is not None:
            self.OnEnter = lambda: OnEnter(self)
        else:
            self.OnEnter = lambda: self.deactivate()
            
        """ The string value containing the current input data (Textbox value). """
        self.value = ''
        self.valueImage = WidgetGen.Label(self.value)
        
        self.y2 = self.y+self.image.get_height()+2
        
        self.eventTypes = [pygame.KEYUP]
        self.activate()
        self.show = True

    def OnKey(self, key=None, mod=None):
        if key is not None:
            if key >= 97 and key <= 122:#Letters
                if 1 & mod:
                    self.value += pygame.key.name(key).upper()                    
                else:
                    self.value += pygame.key.name(key)
            
            elif key >= 48 and key <= 57: #Number
                self.value += pygame.key.name(key)
            
            elif key is 8: #Delete
                value = ''
                for i in range(self.value.__len__()-1):
                    value += self.value[i]
                self.value = value
                
            elif key is 32: #Space
                self.value += ' '
                
            elif key is 13: #Enter/return
                self.OnEnter()
                return
                
            self.valueImage = WidgetGen.Label(self.value)                

    def draw(self):
        if self.show:
            self.screen.blit(self.image, (self.x, self.y))
            self.screen.blit(self.valueImage, (self.x, self.y2))

class territoryDisplay(pygameWidget):
    def __init__(self, parent, directory, name='Unnamed territory display'):
        super(territoryDisplay, self).__init__(parent, None, (320, 240), name=name)
        self.territories = events.LockedList()
        self.originalBorders = events.LockedList()
        black = '(0, 0, 0, 255)'
        territory = ''
        border = ''
        for id in range(2):
            surPath ='./{0}/land_{1}.sur'.format(directory, str(id))
            borPath ='./{0}/land_{1}.bor'.format(directory, str(id))
            try:
                if not os.path.isfile(surPath):
                    print 'Surface file does not exist.\n'
                    raise IOError
                else:
                    contents = ''
                    with open(surPath, 'r') as file:
                        for line in file:            
                            contents += line
                    territory = pygame.image.fromstring(contents, (200, 200), 'RGBA')
                    del contents
                    
                    if not os.path.isfile(borPath):
                        print 'Border file does not exist.\n'
                        raise IOError
                    else:
                        border = pickle.load(open(borPath, 'r'))
            except:
                territory = pygame.image.load('./{0}/land_{1}.png'.format(directory, str(id)))
                border = []
                for x in range(200):
                    for y in range(200):
                        color = territory.get_at((x, y))
                        if str(color) == black:
                            border.append((x, y))
                with open(surPath.format(directory, str(id)), 'w') as file:
                     file.write(pygame.image.tostring(territory, 'RGBA'))
                with open(borPath, 'w') as file:
                    pickle.dump(border, file)
            finally:
                self.territories.append(territory)
                self.originalBorders.append(border)
        
    def changeOwnership(self, territoryID, newowner):
        while newowner.master is not None:
                newowner = newowner.master
        with self.territories as Territories, self.originalBorders as Borders:
            for borderValue in Borders[territoryID]:
                Territories[territoryID].set_at(borderValue, newowner.color)
    
    def draw(self):
        if self.active:
            with self.territories as Territories:
                for place in Territories:
                    self.screen.blit(place, (self.x, self.y))

class WidgetGen(object):
    @staticmethod
    def Label(text):
        """ 
        A static method that generates and returns a text image without creating a full label widget
        :param string text: The text for the label to display 
        :return Surface: A surface containing the text rendered with the default font at size 18
        """
        font = pygame.font.Font(pygame.font.get_default_font(),18)
        return font.render(text, True, (0xff, 0xff, 0xff))

    @staticmethod
    def ButtonArray(parent, list=[], (x, y)=(0, 0)):
        widgets = []
        for choice in list:
            text = choice[0]
            image = WidgetGen.Label(text)
            func = choice[1]
            button = pygameButton(parent, image, (x, y), OnClick=func, name=text)
            widgets.append(button)
            y += 20
            
        return widgets
            
class RootForm(pygameForm):   
    def begin(self):
        self.name = 'RootForm'
        self.background = self.parent.tileSet[0][0]
        
        centerScreen = self.screen.get_width()/2
        
        self.parent.guimanager.append(self._widgets, 0)
        
    def quit(self):
        self.parent.quit()

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
    
    def __init__(self, root, core):
        self._status = True
        self.StatusLock = threading.Lock()        
        pygame.init()    
        self.screen = pygame.display.set_mode((640, 480),1)
        self.clock = pygame.time.Clock()        
        
        self.evalStatus = lambda obj: obj.status
        
        self.eventmanager = events.EventManager([])
        #self.quitEvent = events.Event(self.quit, self, self.evalStatus)
        
        self.guimanager = events.GuiManager(3)
        self.thread_guiManager = threading.Thread(target=self.guimanager.run, name='GUI Event Manager')
        self.thread_eventManager = threading.Thread(target=self.eventmanager.run, name='Event Manager')

        self.tileSet = []
        self.tileSet.append([])
        firstSet = ['./hexagon/hextile.png', './hexagon/hexcursor.png']
        for i in firstSet:
            self.tileSet[0].append(pygame.image.load(i).convert())
        
        self.root = root(self.clock, self, self.guimanager)

        self.core = core

    def mainLoop(self):
        self.thread_guiManager.start()
        self.thread_eventManager.start()
        while self.status:
            self.root.draw(30)

        print 'Main Loop Terminated'
        pygame.quit()
        return
