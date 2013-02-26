
class GenericLand(object):
    
    __doc__ = \
    """
    :param ruler.general owner: The current ruler that the land's governor is loyal to.
    :param int id: Numerical value unique to the land, usually the land's place in the core.territories array.
    :param string name: The string value name of the land.
    :param int size: The physical size of the land, measured as its max population limit.
    :param patron: The patron spirit that the natives venerate. Type class has not been written yet.
    :param list generals: The starting list of generals present in the land.
    :param ruler.general governor: The original leader of the land. If left undefined, generals[0] becomes the governor.
    :param int agriculture: The starting agricultural value of the land.
    :param int market: The starting economic value of the land.
    :param int loyalty: The starting loyalty of the population towards their governor.
    :param list borders: The list of land ids that denote what share their borders with it.
    """
    
    def __init__(self, owner, id, name, size=2000, population=2000, patron=None, generals=[], governor=None, agriculture=30, market=30, loyalty=45, borders=[]):
        self.id = id
        self.original_owner = owner
        self.owner = owner
        self.name = name
        
        self.size = size
        self.population = population
                
        self.patron = patron
        """ .. todo:: Implement patron spirits. """
        
        self.generals = generals
        
        if owner in self.generals:
            self.governor = self.owner
        else:
            self.governor = governor
        self.borders = borders
        
        self.agriculture = agriculture
        self.market = market
        self.loyalty = loyalty
        self.defence = 1
        self.borderColor = owner.color

    def iAgriculture(self, general):
        """
        :param general: The general who is going to perform the improvement
        """
        
        amount = general.stats.Leadership()
        self.agriculture += amount
        self.loyalty += 1
        general.strength -= 10
        return amount

    def iMarket(self, general):
        """
        :param general: The general who is going to perform the improvement
        """
        
        amount = general.stats.Leadership()        
        general.strength -= 10
        return amount

    def checkLoyalty(self, target):
        return self.owner.checkLoyalty(target)
        
    def NextTurn(self):
        self.population *= 1+(self.loyalty/10)
        
