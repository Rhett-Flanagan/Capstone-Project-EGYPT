import math
import random
import numpy as np
from mesa import Agent


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
    pos = (0, 0)
    fertility = 0.0
    settlementTerritory = False
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

    def __init__(self, unique_id: int, model, pos: tuple = (0, 0), fertility: float = 0.0):
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
        # sigma = self.model.sigma
        alpha = self.model.alpha
        beta = self.model.beta
        ticks = self.model.currentTime

        self.fertility = 17 * (beta * (math.exp(0 - (self.pos[0] - mu) ** 2 / alpha)))
        self.avf = ((ticks * self.avf) + self.fertility) / (ticks + 1)
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
        print(self.population)
        self.fission()


class Household(Agent):
    """
    Household agent, the active agent in the simulation, contains information relevant to descision making and metrics
    """

    # Variable declarations for non python programmer sanity
    pos = (0, 0)
    settlement = None
    grain = 0
    workers = 0
    ambition = 0.0
    competency = 0.0
    workersWorked = 0
    generationCountdown = 0
    fieldsOwned = 0
    fieldsHarvested = 0
    fields = []

    def __init__(self, unique_id: int, model, settlement: Settlement, pos: tuple, grain: int,
                 workers: int, ambition: float, competency: float,
                 generationCountdown: int):
        '''
        Create a new Settlement

        Args:
            pos: Tuple representing the position of the agent on a grid
            settlement: The settlment in which the household resides
            model: The model in which the agent is being used
            grain: The grain that the settlement has
            workers: The number of workers in the Household
        '''
        super().__init__(unique_id, model)
        self.pos = pos
        self.settlement = settlement
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
            neighbours = self.model.grid.get_neighbors(pos = self.pos,moore = True, include_center =  False, radius = self.model.knowledgeRadius)
            for a in neighbours:
                if (a.fertility > bestFertility and type(a).__name__ == "Field"
                        and a.owned == False and a.settlementTerritory == False):
                    bestFertility = a.fertility
                    bestField = a

            # Make claim
            if bestField != None:
                # Redundancy checks
                if (type(bestField).__name__ == "Field" and bestField.owned == False
                        and bestField.settlementTerritory == False):
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
                    harvest = ((f.fertility * maxYield * self.competency) - 
                              (((abs(self.pos[0]) - f.pos[0]) + 
                                 abs(self.pos[1] - f.pos[1])) * 
                                 self.model.distanceCost))
                    if harvest > bestHarvest:
                        bestHarvest = harvest
                        bestField = f
            # Farm best field
            chance = np.random.uniform(0, 1)
            if ((self.grain > (self.workers * 160)) or (chance < self.ambition * self.competency)) and (
                    bestField is not None):
                bestField.harvested = True
                totalHarvest += bestHarvest - 300  # -300 for planting
                self.workersWorked += 2
        # Complete farming    
        self.grain += totalHarvest
        self.model.totalGrain += totalHarvest

    def rent(self):
        # TODO
        pass

    def consumeGrain(self):
        """
        This method allows households to consume grain based on the number of workers they have.
        Should a household have zero or fewer workers the household will then be removed from the simulation as it has died out.
        The amount of grain consumed is based off of ethnographic data which suggests an adult needs an average of 160kg of grain per year to survive.
        """
        # Consume grain for all workers
        self.model.totalGrain -= self.workers * 160
        self.grain -= self.workers * 160   
        
        # Decrement amount of workers if grain is less than or equal to zero (also impacts overall population numbers)
        if (self.grain <= 0):
            self.grain = 0
            self.workers -= 1
            self.settlement.population -= 1
            self.model.totalPopulation -= 1

            # Check if there are still workers in the Household
            if self.workers <= 0:
                # Removes ownership of all fields
                for i in self.fields:
                    i.owned = False
                # Decrements the amount of households and removes this household from the simulation
                self.settlement.noHouseholds -= 1
                self.settlement = None
                self.model.schedule.remove(self)

    def storageLoss(self):
        """
        This method removes grain from the households total to account for typical annual storage loss of agricultural product
        """
        self.model.totalGrain -= self.grain * 0.1
        self.grain -= (self.grain*0.1)

    def populationShift(self):
        """
        This method allows for population maintenance as households 'die', simulates movements of workers from failed to more successful households
        """
        startingPopulation = self.model.startingSettlements*self.model.startingHouseholds*self.model.startingHouseholdSize

        populateChance = random.uniform(0,1)

        if (self.model.totalPopulation <= (startingPopulation*(1 + pow(self.model.popGrowthRate/100,self.model.currentTime))) and (populateChance > 0.5)):
            self.workers += 1
            self.settlement.population += 1
            self.model.totalPopulation = self.model.totalPopulation + self.workers   ##### NEED TO CONFIRM THIS
        
        projectedHistoricalPopulation = pow(startingPopulation*(1.001),self.model.currentTime)

        

    def genChangeover(self):
        """
        This method is to simulate what may happen when a relative or child takes over the household and thus allows
        for the level competency and ambition of a household to change as would be expected when an new person is in control.
        """
        # Decreases the generational countdown 
        self.generationCountdown -= 1

        # Checks if the generation countdown has reached zero and thus will occur
        if self.generationCountdown <= 0:
            # Picks a new random value for the next generation to last (Min of 10 years, Max of 15 years)
            self.generationCountdown = random.randint(0, 5) + 10 

            # continues to recalculate the new ambition value until it is less than one and greater than the model's minimum ambition
            while(True):
                # Chooses an amount to change ambition by between 0 and the generational variance number
                ambitionChange = random.uniform(0, self.model.generationalVariation)
                # Chooses a random number between 0 and 1
                decreaseChance = random.uniform(0,1)

                # If decreaseChance is < 0.5 it causes an ambition decrease for the next generation
                if (decreaseChance < 0.5):
                    ambitionChange *= -1
            
                newAmbition = self.ambition + ambitionChange

                if((newAmbition > 1) or (newAmbition < self.model.minAmbition)):
                    break
            
            # sets the new ambition
            self.ambition = newAmbition

            # continues to recalculate the new competency value until it is less than one and greater than the model's minimum competency
            while(True): 
                # Chooses an amount to change competency by between 0 and the generational variance number
                competencyChange = random.uniform(0, self.model.generationalVariation)
                # Chooses a random number between 0 and 1
                decreaseChance = random.uniform(0,1)

                # If decreaseChance is < 0.5 it causes a competency decrease for the next generation
                if (decreaseChance < 0.5):
                    competencyChange *= -1
            
                newComp = self.competency + competencyChange

                if(newComp > 1 or newComp < self.model.minCompetency):
                    break
           
            # sets the new competency
            self.competency = newComp

    def fieldChangeover(self):
        """
        This method checks if an owned field has been harvested or not and tracks how many years it has been unharvested if not.
        Should the field not be harvested for longer than or equal to the fallowlimit then the Household loses ownership
        of the field and it is free for other households to claim.
        """

        # Array to store fields to delete
        toDel = []
        
        # For loop to loop through all owned fields
        for i in range(len(self.fields)):
            # If statement to check if a field has been harvested or not
            if (self.fields[i].harvested == True):
                self.fields[i].yearsFallow = 0
            else:
                self.fields[i].yearsFallow += 1
            
            # If statement to add fallowlimit exceeding fields to an array of fields to delete
            if (self.fields[i].yearsFallow >= self.model.fallowLimit): 
                self.fields[i].owned = False
                self.fields[i].field = False
                self.fieldsOwned -= 1
                toDel.append(i - len(toDel)) # Subtract to account for array shrinkage as deletion happens

        # For loop to remove all fallowlimit exceded fields from the Households ownership
        for i in toDel:
            del self.fields[i]


    def step(self):
        """
        The actions to take on a general step sequence
        """
        self.claimFields()
        self.farm()

    def stepFarm(self):
        """
        Calls the farming methods for the initial run of households in the scheduler
        """
        self.claimFields()
        self.farm()
    
    def stepRentConsumeChangeover(self):
        """
        Calls the renting, aging, changeover and methods
        """
        self.rent()
        self.consumeGrain()
        self.storageLoss()
        self.fieldChangeover()
        self.genChangeover()
        self.populationShift()

