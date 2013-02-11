
class generic(object):
    def __init__(self):
        self.test = True
        return
    
    def handle(self):
        return False
    
def eval(obj):
    if obj.test == True:
        return False
    else:
        return True
        
