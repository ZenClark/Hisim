from random import randint

#An Opinion, 
class Opinion(object):
    
    __doc__ = \
    """
    
    a tuple object containing the disposition and mood for a named item
    
    :param name: The name of the opinion
    
    """
    __name__ = 'Opinion'
    
    def __init__(self, name, disposition=None, mood=100):

        __name__ = name
        self.name = name
        if disposition is None:
            disposition = randint(60, 100)
        self.disposition = disposition
        self.mood = mood
        
        self.flags = {}
        
    def priority(self):
        if self.mood is 0:
            self.mood = 1
        return self.disposition*self.mood

    def __str__(self):
        return 'disposition: {0}, mood: {1}'.format(str(self.disposition), str(self.mood))

    def __sub__(self, y):
        if type(y) is type(0):
            self.mood -= y 
        else:
            return

    def __getitem__(self, y):
        if y is 0:
            return self.disposition
        elif y is 1:
            return self.mood
        elif type(y) is type(''):
            try:
                return self.flags[y]
            except KeyError:
                return None
        else:
            raise KeyError

    def __setitem__(self, i, y):
        if i is 0:
            self.disposition = y
        elif i is 1:
            self.mood = y
        elif type(i) is type(''):
            self.flags[i] = y

class GenericAI(object):
    def __init__(self, core, owner):
        self.name = 'generic'        
        self.owner = owner
        #Dictionary containing the disposition and mood for each general, with the key being the general's name
        # (disposition, mood)
        self.generals = {}
        
        self.core = core
            
        #Dictionary containing the disposition and mood for each aspect of the territory they are in
        self.land = {}
        
        #self.land['Loyalty'] = Opinion('Loyalty')
        #self.land['Loyalty']['STA'] = 0
        self.land['Market'] = Opinion('Market')
        self.land['Market']['STA'] = 20
        self.land['Market']['STAT'] = 'Strength'
        self.land['Agriculture'] = Opinion('Agriculture')
        self.land['Agriculture']['STA'] = 20 
        self.land['Defense'] = Opinion('Defense')
        self.land['Defense']['STA'] = 0
        self.land['Train'] = Opinion('Train')
        self.land['Train']['STA'] = 30

    def run(self):
        priority = self.priority()
        general = self.delegate(priority)
        if general is not None:
            if priority.name is 'Agriculture':
                self.owner.location.iAgriculture(general)
            elif priority.name is 'Market':
                self.owner.location.iMarket(general)
            elif priority.name is 'Train':
                general.army.experience += general.stats.Leadership()
            print '{0} Delegated {1} for {2}'.format(self.name, general.name, priority.name) 
            priority[1] -= 10
            if choice([1, 0]) is 1:
                self.refresh()        

    def log(self, msg):
        with open('./debug.out',  'a') as debugf:
            debugf.write('{0}: '.format(msg))
            list = {}
            for i in self.land:
                list[i] = str(self.land[i])
            debugf.write('\nLand:\n{0}\n'.format(str(list)))
            list = {}
            for i in self.generals:
                list[i] = str(self.generals[i])
            debugf.write('\nGenerals:\n{0}\n'.format(str(list)))
            
    def refresh(self):
        list = self.land.items()
        for i in range(self.land.__len__()):
            list[i][1][1] += list[i][1][0]/10

    def update(self):
        #Setting all moods to zero, and all dispositions to a random value between the max and min
        del self.generals
        self.generals = {}
        for i in range(self.core.generals.__len__()):
            name = self.core.generals[i].name
            self.generals[name] = Opinion(name)        
        return
        
    def priority(self):
        """ Picks an opinion from self.land with the highest disposition*mood."""
        Top = None
        Value = 0
        items = self.land.items()
        Top = items[0][1]
        for i in range(self.land.__len__()):
            if items[i][1].priority() >= Value:
                Top = items[i][1]
                Value = Top.priority()
        return Top

    def delegate(self, opinion):
        list = []
        for i in range(self.owner.location.generals.__len__()):
            general = self.owner.location.generals[i]
            
            loyal = general.checkLoyalty(self.owner)
            if loyal and (general.strength > opinion['STA']):
                list.append(general)
        
        if list.__len__() is 1:
            return list[0]
        elif list.__len__() is 0:
            return None
            
        candidate = list[0]
        priority = self.generals[candidate.name].priority()
        for i in range(list.__len__()):
            _priority = self.generals[list[i].name].priority()
            if _priority > priority:
                priority = _priority
                candidate = list[i]

        self.generals[general.name][1] -= opinion['STA']
        if self.owner.core.DEBUG:
            self.log('\n{0}\'s log'.format(self.owner.name))
        return general
