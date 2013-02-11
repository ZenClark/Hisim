
class Terminal(object):
    def __init__(self, debug=False):
        self.DEBUG = debug
        
        self.CLEAR = '\033[37m' #Clear changes the text to a white color
        self.CLEARTERM = '\x1b[2J\x1b[H' #Clears the terminal screen, and sets the cursor at the top
        
        self.RED = '\033[91m'
        self.GREEN = '\033[32m'
        self.BLUE = '\033[34m'
    
    def debugmode(self):
        self.DEBUG = True
    
    def fprint(self, string):
        string = self.format(string)
        
        print string
        print self.CLEAR
    
    def format(self, string):
        if not self.DEBUG:
            string = string.replace('[cb', self.BLUE)
            string = string.replace('[cg', self.GREEN)
            string = string.replace('[cr', self.RED)
            string = string.replace('[cc', self.CLEAR)
        else:
            string = string.replace('[cb', '')
            string = string.replace('[cg', '')
            string = string.replace('[cr', '')
            string = string.replace('[cc', '')            
        return string
    
    def clear(self):
        if not self.DEBUG:
            print self.CLEARTERM
    
    def wait(self):
        done = False
        while not done:
            input = raw_input('\n[Enter]')
            print '\n{0}\n'.format(input)
            if input is '' or input is u'':
                done = True
        return

