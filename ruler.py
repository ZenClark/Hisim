from random import choice, randint

from land import Land
from army import Army
from menu import AssignGovernor
from ai import GenericAI
from terminal import Term

class Attribute(object):
    def __init__(self, value, name):
        self.value = value
        self.name = name

    def __call__(self):
        roll = 0
        for i in range(self.value):
            roll += randint(1, 6)
    
        return roll

class Attributes(object):

    def __init__(self):
        self.Stamina = Attribute(0, 'Stamina')
        self.Will = Attribute(0, 'Will')
        self.Personality =  Attribute(0, 'Personality')  
        self.Leadership = Attribute(0, 'Leadership')
        
class general(object):
    
    __name__ = 'Generic General'
    
    def __init__(self, core, name='Empty', isPlayer=False, isRuler=False, isGovernor=False, master=None):
        self.core = core
        
        self.name = name
        self.__name__ = name
        
        self.isPlayer = isPlayer
        self.stats = Attributes()
        ranstats = lambda: choice([1, 2, 2, 3, 3, 3, 4, 4, 5])

        self.stats.Will.value = ranstats()
        self.stats.Stamina.value = ranstats()
        self.stats.Personality.value = ranstats()
        self.stats.Leadership.value = ranstats()
        
        self.strength  = self.stats.Stamina()
        
        if isPlayer == False:
            self.army = Army(self, choice([100, 200, 300]))
        else:
            self.army = Army(self, 300)
    
        self.master = master
    
        self.core.generals.append(self)
        if isRuler or isPlayer:
            self.isRuler = True
            self.core.rulers.append(self)
        else:
            self.isRuler = False
        if isRuler and not isPlayer:
            self.AI = GenericAI(self.core, self)
            
    def promote(self, place):
        if self.checkLoyalty(place.owner) == False:
            print 'The general must be loyal to the territory\'s owner.'
            return False
        elif self not in place.generals:
            print 'The general must be in the territory that he is suppose to lead'
            return False
        else:
            place.governor = self
            return True
    
    def checkLoyalty(self, target):
        if self == target:
            return True
        if self.master != None:
            x = self
            while x.master != target and x.master != None:
                print '{0}\'s master is {1}'.format(x.name, x.master.name)
                x = x.master
            if x is target or x.master is target:
                return True
            else:
                return False
        else:
            return False
    
    def Attack(self, target):
        if self.army == None:
            return

        elif isinstance(target, Land):
            targetStrength = target.population
            atk = (self.stats.Leadership() + self.army.experience)*self.army.strength*self.army.men
            dfn = (target.loyalty * target.defence)/targetStrength
            if target.population > atk-dfn:
                target.population -= atk-dfn
                Term.fprint('[cb{0}[cc attacks [cb{1}[cc, bringing their population down from [cr{2}[cc to [cr{3}[cc'.format(self.name, target.name, str(targetStrength), str(target.population)))
                #print 'atk:(' + str(atk) + ')\n'
            else:
                print self.name + ' has conquered ' + target.name + ' with an attack of ' + str(atk)
                oldLocation = self.location
                target.owner = self
                target.governor = self
                target.generals.append(self)
                oldLocation.generals.remove(self)
                if self.isPlayer or self.location.governor == self:
                    if oldLocation.generals.__len__() == 0:
                        oldLocation.governor = None
                    else:
                        for x in range(oldLocation.generals.__len__()):
                            if oldLocation.generals[x].checkLoyalty(self):
                                
                                assigngov = AssignGovernor(self)
                                assigngov.eval(oldLocation)
                                del assigngov
                                self.location = target
                                return
                        oldLocation.governor = oldLocation.generals[0]
                
        elif isinstance(target, general):
            atk = (self.stats.Leadership() + self.army.experience)*self.army.strength*self.army.men
            dfn = target.Defend(self, atk)
        
            print 'atk:(' + str(atk) + ') dfn:(' + str(dfn[0]) + ') total damage:(' + str(dfn[1]) + ')\n' 
                
    def Defend(self, target, atk):
        if isinstance(target, general):
            defence = (self.stats.Leadership() + self.army.experience)
            defence *= self.army.experience
            defence *= self.army.men
            defence *= 2
            
            damage = atk - defence
            
            if damage <= 0:
                print 'failure, ' + self.name + '\'s defence was too high, ' + target.name + ' could not damage them\n'
            else:
                print target.name + ' has attacked ' + self.name + ' with a damage of ' + str(damage) + ', bringing them down from ' + str(self.army.men) + ' men to ' + str(self.army.men-damage)  + '\n\n'
                
                return [defence, damage]
            
    def NextTurn(self):
        if self.isRuler and not self.isPlayer:
            self.AI.run()
        self.strength += self.stats.Stamina()/2 #I don't want them to gain strength too fast.
        
class player(general):
    
    def __init__(self, core):
        super(player, self).__init__(core, isPlayer=True)
        self.location = None
        self.activeLocation = None
        self.MenuList = {}

