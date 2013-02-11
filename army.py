from random import choice

class Army(object):
    
    def __init__(self, owner, number):
        """
        Constructor
        
        Army object
        
        @param owner The owner of the army, should be a subclass of the ruler.general class. (ruler.general)
        @param number The number of men making up the army
        """
        self.general = owner
        self.experience = 0
        self.type = 'Swords'
        self.men = number
        self.strength = 1
        
