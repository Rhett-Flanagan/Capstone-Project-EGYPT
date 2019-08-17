from mesa import Agent
import numpy as np
import math

# Class to setup the agents for the model:
# Tile: A psudeo agent used primarily as a container for data, can be a river, settlement or field
# Household: The active agent in the simulation. Dwells in a settlement, and farms fields

class Tile(Agent):
    """
    Class implementing the functionality of an patch in a NetLogo.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    # Variable declarations for non python programmer sanity
    pos = (0,0)
    fertility = 0.0
    settlementTeritory = False
    owned = False
    color = None

    def __init__(self, unique_id, model, pos: tuple):
        '''
        Create a new Tile

        Args:
            pos: Tuple representing the position of the agent on a grid
            model: The model in which the agent is being used
        '''
        super().__init__(unique_id, model)
        self.pos = pos
    
    def step(self):
        pass

class River(Tile):
    """
    River agent, currently does nothing and is used only as an identifier
    """ 
    def __init__(self, unique_id, model, pos: tuple):
        '''
        Create a new River

        Args:
            pos: Tuple representing the position of the agent on a grid
            model: The model in which the agent is being used
        '''
        super().__init__(unique_id, model, pos)


class Field(Tile):
    """
    Fields agent, can be farmed by households and have changing fertility values and owners
    
    """

    # Variable declarations for non python programmer sanity
    avf = 0.0
    yearsFallow = 0

    def __init__(self, unique_id: int, model, pos: tuple = (0,0), fertility: float = 0.0):
        '''
        Create a new Field

        Args:
            pos: Tuple representing the position of the agent on a grid
            model: The model in which the agent is being used
            fertility: The starting fertility of the field
        '''
        super().__init__(unique_id, model, pos)
        self.fertility = fertility
        self.avf = fertility
        self.yearsFallow = 0
    
    def flood(self):
        """
        Changes the fertility value simulating annual flood
        """
        mu = self.model.mu
        #sigma = self.model.sigma
        alpha = self.model.alpha
        beta = self.model.beta
        ticks = self.model.currentTime

        self.fertility = 17 * ( beta * (math.exp(0 - (self.pos[0] - mu) ** 2 /  alpha)))
        self.avf = ((ticks * self.avf) + self.fertility)/(ticks + 1)
        self.harvested = False

    def step(self):
        self.flood()
    
    

class Settlement(Tile):
    """
    Settlement agent, contains households and has changing population and number of households
    """

    # Variable declarations for non python programmer sanity
    population = 0
    noHouseholds = 0

    def __init__(self, unique_id: int, model, pos: tuple, population: int, noHouseholds: int):
        '''
        Create a new Settlement

        Args:
            pos: Tuple representing the position of the agent on a grid
            model: The model in which the agent is being used
            population: The starting population of the setllement (Number of Households * Household Population)
            noHouseholds: The number of Households in the Settlement
        '''
        super().__init__(unique_id, model, pos)
        self.population = population
        self.noHouseholds = noHouseholds

    def fission(self):
        # TODO
        pass

    def step(self):
        self.fission()



class Household(Agent):
    """
    Household agent, the active agent in the simulation, contains information relevant to descision making and metrics
    """

    # Variable declarations for non python programmer sanity
    pos = (0, 0)
    grain = 0
    workers = 0
    ambition = 0.0
    competency = 0.0
    workersWorked = 0
    generationCountdown = 0
    fieldsOwned = 0
    fieldsHarvested = 0
    fields = []

    def __init__(self, unique_id: int, model, pos: tuple, grain: int,
                 workers: int, ambition: float, competency: float, 
                 generationCountdown: int):
        '''
        Create a new Settlement

        Args:
            pos: Tuple representing the position of the agent on a grid
            model: The model in which the agent is being used
            grain: The grain that the settlement has
            workers: The number of workers in the Household
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.grain = grain
        self.workers = workers
        self.ambition = ambition
        self.competency = competency
        self.generationCountdown = generationCountdown
        self.fieldsOwned = 0
        self.fieldsHarvested = 0
        self.fields = []

    def claimFields(self):
        """
        This method allows households to *decide* whether or not to claim fields that fall within their knowledge-radii.
        The decision to claim is a function the productivity of the field compared to existing fields and ambition.
        """
        chance = np.random.uniform(0, 1)
        if (chance > self.ambition and self.workers > self.fieldsOwned) or (self.fieldsOwned <= 1):
            bestFertility = 0
            bestField = None

            # Iterate through fields on the grid
            neighbours = self.model.grid.get_neighbors(self.pos, False, self.model.knowledgeRadius)
            for a in neighbours:
                if (a.fertility > bestFertility and type(a).__name__ == "Field" 
                    and a.owned == False and a.settlementTeritory == False):
                    bestFertility = a.fertility
                    bestField = a
            
            # Make claim
            if bestField != None:
                # Redundancy checks
                if(type(bestField).__name__ == "Field" and bestField.owned == False 
                    and bestField.settlementTeritory == False):
                    bestField.owned = True
                    bestField.harvested = False
                    bestField.yearsFallow = 0
                    self.fieldsOwned += 1
                    self.fields.append(bestField)
    
    def farm(self):
        totalHarvest = 0
        maxYield = 2475
        self.workersWorked = 0
        self.fieldsHarvested = 0

        for i in range(self.workers // 2):
            # Determine best field
            bestHarvest = 0
            bestField = None
            for f in self.fields:
                if not f.harvested:
                    harvest  = ((f.fertility * maxYield * self.competency) - (((abs(self.pos[0]) - f.pos[0]) + abs(self.pos[1] - f.pos[1])) * self.model.distanceCost))
                    if harvest > bestHarvest:
                        bestHarvest = harvest
                        bestField = f
            # Farm best field
            chance = np.random.uniform(0,1)
            if ((self.grain > (self.workers * 160)) or (chance < self.ambition * self.competency)) and (bestField is not None):
                bestField.harvested = True
                totalHarvest += bestHarvest - 300 # -300 for planting
                self.workersWorked += 2
        # Complete farming    
        self.grain += totalHarvest
        self.model.totalGrain += totalHarvest


    def rent(self):
        # TODO
        pass
    
    def consumeGrain(self):
        # TODO
        pass

    def storageLoss(self):
        # TODO
        pass

    def populationShif(self):
        # TODO
        pass

    def genChangeover(self):
        # TODO
        pass

    def fieldChangeover(self):
        # TODO
        pass

    def step(self):
        self.claimFields()
        self.farm()
        pass