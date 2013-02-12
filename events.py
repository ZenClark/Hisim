import pygame
import thread, threading

class Event(object):
    
    def __init__(self, handler, obj, evaluation):
        
        self.eval = lambda : evaluation(obj)
        self._owner = obj
        self._handler = handler
    
    def __call__(self):
        self._handler()
    
class EventManager(object):

    def OnSet(self, y):
        with self.OnLock:
            self._on = y

    def OnGet(self):
        with self.OnLock:
            on = self._on
        return on

    def OnDel(self):
        with self.OnLock:
            del self._on

    on = property(OnGet, OnSet, OnDel, 'Thread safe status property')

    def __init__(self, event_list=[]):
        self.OnLock = threading.Lock()
        self._events = event_list
        self._on = True
        
    def run(self):
        while self.on:
            for i in range(self._events.__len__()):
                if self._events[i].eval() == True:
                    self._events[i]()
        print 'Manager is now off'

    def Off(self):
        self.on = False
        thread.exit()

    def AddEvent(self, handler, obj, evaluation):
        new_event = Event(handler, obj, evaluation)
        self._events.append(new_event)    
        return new_event

    def RemoveHookHandler(self, event):
        self._events.remove(event)
        return
        
    def append(self, item):
        if isinstance(item, Event):
            self._events.append(item)
    
    def remove(self, item):
        if isinstance(item, Event):
            self._events.remove(item)
    
class LockedList(object):
        def __init__(self):
            self.Lock = threading.Lock()
            self._widgets = []
                
        def __getitem__(self, i):
            with self.Lock:
                return self.__dict__['_widgets'][i]
            
        def append(self, x):
            with self.Lock:
                self.__dict__['_widgets'].append(x)
                
        def remove(self, x):
                with self.Lock:
                    if x is not None:
                        if x in self.__dict__['_widgets']:
                            self.__dict__['_widgets'].remove(x)            
            
class GuiManager(EventManager):
    def __init__(self, tree_max=3):
        self.OnLock = threading.Lock()
        self._tree_max = tree_max
        self._widgets = LockedList()
        self._on = True
        for counter in range(tree_max-1):
            self._widgets.append([])
            
    def run(self):
        while self.on:
            for event in pygame.event.get():
                if event.type is pygame.MOUSEBUTTONUP:
                    x = event.pos[0]
                    y = event.pos[1]
                    for tree in self._widgets:
                        for widget in tree:
                            if widget.active and (widget.eventType is pygame.MOUSEBUTTONUP) and widget.Within(x, y):
                                widget.OnClick()
                                continue
                    print '({0},{1})\n'.format(str(x), str(y))
            
    def append(self, list=None, item=None, tree=0):
        if list is not None:
            if tree <= self._tree_max:
                for widget in list:
                    self._widgets[tree].append(item)
        elif item is not None:
            self._widgets[tree].append(item)
            
    def remove(self, widget, tree=0):
        try:
            with self.OnLock:
                self._widgets[tree].remove(widget)
            
        except ValueError:
            return False
        except IndexError:
            return False
            
        else:
            return True
