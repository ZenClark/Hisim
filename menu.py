from terminal import Term
import sys

class Menu(object):
    
    def __init__(self, player):
        self.player = player
        self.location = player.activeLocation
        self.core = self.player.core

    def eval(self, choices, prompt):
        try:
            Input = raw_input(Term.format(prompt))
            if Input is '0' or Input is '':
                return False
            choice = choices[Input]
            return choice
        except KeyError:
            Term.fprint('[crThat is not a valid choice.[cc\n')
            del Input
            return Menu.eval(self, choices, prompt)
        except:
            print 'What? {0}'.format(sys.exc_info()[0])
            sys.exit()
            return False
            
class RootMenu(Menu):
    
    def __init__(self, player):
        super(RootMenu, self).__init__(player)
        if self.player.core.DEBUG:
            Term.debugmode()
            
        self.player.MenuList['AttackWho'] = AttackWho(self.player, self)
        self.choiceList = {'1':self.attack, '2':self.next, '3':self.agriculture, '4':self.information, '5':self.train, '6':self.market,'quit':self.quit }
        self.status = StatusList(self.player)
        self.menu = Selection(self.player)
        Term.clear()

    def eval(self):
        self.status.StatusPrompt()
        self.prompt = Term.format('\n\n[cg1[cc: Attack \n[cg2[cc: Wait\n[cg3[cc: Improve Agriculture\n[cg4[cc: Information\n[cg5[cc: Train\n')
        choice = super(RootMenu, self).eval(self.choiceList, self.prompt)
        Term.clear()
        if choice is not False:
            choice()
        else:
            Term.clear()
            self.eval()
        
    def quit(self):
        sys.exit()
        
    def train(self):
        Term.fprint('\nChose a general to train his army (costs [cr30 strength[cc)\n')
        choice = self.menu.selectGeneral()
        if choice is False:
            self.eval()
        elif choice.strength < 30:
            Term.fprint('\n[cr30 strength[cc is required, but [cb{0}[cc only has [cr{1} strength[cc left.'.format(choice.name, str(choice.strength)))
            self.train()
        else:
            improvement = choice.stats.Leadership()
            choice.army.experience += improvement
            choice.strength -= 30
            Term.fprint('[cb{0}[cc has increased their army\'s experience by {1}, and is now {2}'.format(choice.name, str(improvement), str(choice.army.experience)))
            Term.wait()
            self.eval()
    
    def information(self):
        self.status.menu()
        
        Term.wait()
        self.eval()

        
    def attack(self):
        print 'You chose attack'
        if self.player.MenuList['AttackWho'].eval():
            Term.wait()
            self.next(False)
        self.eval()
    
    def next(self, message=True):
        if message:
            print 'You chose wait'
        self.player.core.next(self.player.activeLocation)

    def agriculture(self):
        Term.fprint('You chose to improve agriculture (costs [cr10 strength[cc)\n')
        choice = self.menu.selectGeneral()
        
        if choice is not False:
            if  choice.strength > 10:
                improvement = self.activeLocation.iAgriculture(choice)
                Term.fprint('Agriculture of [cb{0}[cc improved by [cr{1}[cc.\n'.format(self.activeLocation.name, str(improvement)))
                
                Term.wait()
                self.next()
            else:
                Term.fprint('[cr10 strength[cc is required, but [cb{0}[cc only had [cr{1} strength[cc left.\n'.format(choice.name, choice.strength))
                Term.wait()
                self.eval()

    def market(self):
        Term.fprint('You chose to improve the market (costs [cr10 strength[cc)\n')

        if choice is not False:
            if  choice.strength > 10:
                improvement = self.activeLocation.iMarket(choice)
                Term.fprint('Market of [cb{0}[cc improved by [cr{1}[cc.\n'.format(self.activeLocation.name, str(improvement)))
                
                Term.wait()
                self.next()
            else:
                Term.fprint('[cr10 strength[cc is required, but [cb{0}[cc only had [cr{1} strength[cc left.\n'.format(choice.name, choice.strength))
                Term.wait()
                self.eval()


    def __call__(self):
        return self.eval()

class AttackWho(Menu):
    def __init__(self, player, root):
        self.root = root
        super(AttackWho, self).__init__(player)
    
    def eval(self):
        x = 1
        list = []
        menu = Selection(self.player)
        prompt = 'Who are you going to attack?\n'
        target = menu.selectBorder(Loyal=False)
        
        if not target:
            return False
        
        Term.fprint('Who shall attack? (Costs [cr20 strength[cc)\n')

        choice = menu.selectGeneral()
        del menu
        if choice is not False and target is not False:
            if choice.strength < 20:
                Term.fprint ('[cr20 strength[cc is required, but [cr{0}[cc only had [cr{1} strength[cc left.\n'.format(choice.name, choice.strength))
            else:
                choice.Attack(target)
                choice.strength -= 20
                return True
        else:
                return False
        
class AssignGovernor(Menu):
    def eval(self, territory):
        message = '{0} is without a governor. Please choose a general to govern.\n'.format(territory.name)
        menu = Selection(self.player)
        choice = menu.selectGeneral()
        if not choice.promote(territory):
            self.eval(territory)
        
class Selection(Menu):

    def selectBorder(self, Loyal=None, location=None):
        if location != None:
            self.location = location
        list = {}
        length = self.location.borders.__len__()
        prompt = 'Choose a bordering territory: [cg(1-{0})[cc\n'.format(length)
        
        if Loyal is None:
            for i in range(length):
                list[str(i)] = self.core.territories[self.location.borders[i]]
        elif type(Loyal) is type(False):
            x = 0
            for i in range(length):
                if self.core.territories[self.location.borders[i]].checkLoyalty(self.player) == Loyal:
                    x += 1
                    list[str(x)] = self.core.territories[self.location.borders[i]]
                    prompt += Term.format("\n[cg{0}[cc: [cb{1}[cc".format(str(x), list[str(x)].name))
            if list.__len__() is 0:
                return False
        prompt += '\n'
        prompt = Term.format(prompt)
        
        return self.eval(list, prompt)
    
    def selectGeneral(self, Loyal=True, location=None):
        if location is not None:
            self.location = location
        list = {}
        x = 0
        prompt = 'Choose a general from the following list: [cg(1-{0})[cc\n'.format(self.location.generals.__len__())
        for i in range(self.location.generals.__len__()):
            if self.location.generals[i].checkLoyalty(self.player) or not Loyal:
                x += 1
                list[str(x)] = self.location.generals[i]
                prompt += '[cg' + str(x) + '[cc: [cb' + list[str(x)].name + ' [cr(' + str(list[str(x)].strength) + ')[cc\n'
         
        prompt += '\n'
        prompt = Term.format(prompt)
        
        input = self.eval(list,  prompt)
        
        if not input:
            return False
        return input
            
class StatusList(object):
    def __init__(self, player):
        self.player = player
        self.core = self.player.core
        self.location = self.player.activeLocation

    def StatusPrompt(self):
        self.update()
        Term.clear()
        status    = "Territory:[cb {0} [cc\n\nAgriculture:[cb {1} [cc\n".format(self.location.name, str(self.location.agriculture))
        
        generals = 0
        for i in range(self.location.generals.__len__()):
            if self.location.generals[i].checkLoyalty(self.player):
                generals += 1
        status += "Loyalty: [cb{0} [ccGenerals: [cb{1}[cc\n".format(str(self.location.loyalty), str(generals))
        
        status += "Population: [cb{0}[cc Market: [cb{1}[cc\n".format(str(self.location.population), str(self.location.market))
        
        Term.fprint(status)
        return

    def update(self):
        self.location = self.player.activeLocation

    def menu(self):
        self.update()
        selectionmenu = Selection(self.player)
        
        choice = selectionmenu.selectGeneral()
        master = choice.master
        if master is None:
            masterName = 'None'
        else:
            masterName = master.name
        Term.fprint('\nName: [cb{0}[cc\nMaster: [cb{1}[cc\nStrength [cb{2}[cc\n'.format(choice.name, masterName, str(choice.strength)))
        Term.fprint('Men: [cb{0}[cc\n ')
        return True
