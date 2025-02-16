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
    settlementTerritory = False
    owned = False

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
    Field agent, can be farmed by households and have changing fertility values and owners
    """

    # Variable declarations for non python programmer sanity
    fertility = 0.0
    avf = 0.0
    yearsFallow = 0
    harvested = False
    owner = None

    def __init__(self, unique_id, model, pos: tuple = (0, 0), fertility: float = 0.0):
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
        self.harvested = False
        self.owner = None

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
    color = "#000000"

    def __init__(self, unique_id, model, pos: tuple, population: int, noHouseholds: int, uid, color: str):
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
        self.color = color


    def step(self):
        """ Actions to take on a step"""
        # Check if settlement is dead
        if self.population == 0:
            local = self.model.grid.get_neighbors(self.pos, moore=True, include_center=True, radius=1)
            # Mark the land as available for farming. River included for an extension that includes fishing.
            # Can be extended by having a timer where the area is not able to be cultivated.
            for a in local:
                if type(a) is Field or type(a) is River:
                    a.settlementTerritory = False
            # Remove from consideration
            self.model.schedule.remove(self)
            self.model.grid.remove_agent(self)


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
    fields = []
    farms = {} # Dict of farms for visualisation purposes

    def __init__(self, unique_id, model, settlement: Settlement, pos: tuple, grain: int,
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
        self.fields = []
        # For visualisation
        self.farms = {}

    def claimFields(self):
        """
        This method allows households to *decide* whether or not to claim fields that fall within their knowledge-radii.
        The decision to claim is a function the productivity of the field compared to existing fields and ambition.
        """
        chance = np.random.uniform(0, 1)
        if (chance > self.ambition and self.workers > len(self.fields)) or (len(self.fields) <= 1):
            bestFertility = 0
            bestField = None

            # Iterate through fields on the grid
            neighbours = self.model.grid.get_neighbors(pos = self.pos, moore = False, include_center =  False, radius = self.model.knowledgeRadius)
            for a in neighbours:
                if (type(a) is Field and a.fertility > bestFertility 
                        and a.owned == False and a.settlementTerritory == False):
                    bestFertility = a.fertility
                    bestField = a

            # Make claim
            if bestField != None:
                # Redundancy checks
                if (type(bestField) is Field and bestField.owned == False
                        and bestField.settlementTerritory == False):
                    # Redundancy Removal of farms
                    if (len(self.model.grid.get_cell_list_contents(bestField.pos)) != 1):
                        for a in self.model.grid.get_cell_list_contents(bestField.pos):
                            if type(a) is Farm:
                                self.model.grid.remove_agent(a)

                    bestField.owned = True
                    bestField.owner = self
                    bestField.harvested = False
                    bestField.yearsFallow = 0
                    self.fields.append(bestField)

                    # Make farm for visualisation
                    farm = Farm(self.model.next_id(), self.model, bestField.pos, self.settlement.color, False)
                    self.model.grid.place_agent(farm, bestField.pos)
                    self.farms[bestField.pos] = farm

    def farm(self, fields, rental):
        """ Farms fields that the Household owns ifthe chance is met"""
        totalHarvest = 0
        maxYield = 2475
        loops = ((self.workers - self.workersWorked)// 2) # Protection against loop breaking with changes
        
        # Sorting functor, sorts on fertility unless field is harvested
        def fert(field):
            if not field.harvested:
                return field.fertility
            else:
                return -1

        fields.sort(key = fert, reverse = True) # Sort fields on fertility so save loop iterations

        for i in range(loops):
            # Optimised looping through fields from NetLogo, saves several loop cycles and calculations 
            for f in fields:
                # If the field is not harvested, setup for harvesting
                if not f.harvested:
                    harvest = (int(f.fertility * maxYield * self.competency) - 
                              (((abs(self.pos[0]) - f.pos[0]) + 
                                 abs(self.pos[1] - f.pos[1])) * 
                                 self.model.distanceCost))
                    # If the chance is met, harvest the field
                    chance = np.random.uniform(0, 1)
                    if (((self.grain > (self.workers * 160)) or (chance < self.ambition * self.competency)) 
                        and (f is not None)):
                        f.harvested = True
                        if rental and f.owner is not None:
                            totalHarvest += round((harvest * (1 - (self.model.rentalRate)))) - 300 #Renter farms and re-seeds
                            f.owner.grain += round(harvest * (self.model.rentalRate)) # Renter pays rental fee
                            self.model.totalGrain += round(harvest * (self.model.rentalRate)) # Add to total grain
                        else:
                            totalHarvest += harvest - 300  # -300 for planting
                        self.workersWorked += 2
                    break # Stop looping through fields after choosing the best and taking the farm chance
        # Complete farming by updating grain totals
        self.grain += totalHarvest
        self.model.totalGrain += totalHarvest

    def rent(self, fields):
        """
        This method allows more ambition and competent households to farm the unharvested fields owned by other households.
        """
        # Functor to get the ambition of an agent for sorting

        # Checks to see if rental is allowed
        if(self.model.rental == True):
            # Gets a list of the households and sorts by ambition level
            self.farm(fields, True)   
    
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
            self.model.totalGrain -= self.grain # Add back negative grain to prevent negatve grain in model and incorrect grain representation
            self.grain = 0
            self.workers -= 1
            self.settlement.population -= 1
            self.model.totalPopulation -= 1

            # Check if there are still workers in the Household
            if self.workers <= 0:
                # Removes ownership of all fields
                for f in self.fields:
                    f.owned = False
                # Decrements the amount of households and removes this household from the simulation
                self.settlement.noHouseholds -= 1
                self.model.schedule.remove(self)

    def storageLoss(self):
        """
        This method removes grain from the households total to account for typical annual storage loss of agricultural product
        """
        self.model.totalGrain -= round(self.grain * 0.1) # Prevent grain going to a float because unrestricted types
        self.grain -= round(self.grain*0.1)

    def populationShift(self):
        """
        This method allows for population maintenance as households 'die', simulates movements of workers from failed to more successful households
        """
        startingPopulation = self.model.startingSettlements*self.model.startingHouseholds*self.model.startingHouseholdSize

        populateChance = random.uniform(0,1)

        # If the household can grow, inrease population.
        if (self.model.totalPopulation <= (startingPopulation * ((1 + (self.model.popGrowthRate/100)) ** self.model.currentTime)) 
            and (populateChance > 0.5)):
            self.workers += 1
            self.settlement.population += 1
            self.model.totalPopulation += 1

    def genChangeover(self):
        """
        This method is to simulate what may happen when a relative or child takes over the household and thus allows
        for the level of competency and ambition of a household to change as would be expected when an new person is in control.
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

                # sets the new ambition and breaks the loop
                if((newAmbition > 1) or (newAmbition < self.model.minAmbition)):
                    self.ambition = newAmbition
                    break

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

                # sets the new competency and breaks the loop
                if(newComp > 1 or newComp < self.model.minCompetency):
                    self.competency = newComp
                    break
           
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
            # If statement to check if a field has been harvested or not, and set render values for the farms
            if (self.fields[i].harvested == True):
                self.fields[i].yearsFallow = 0
                if self.fields[i].pos in self.farms:
                    self.farms[self.fields[i].pos].farmed = True
            else:
                self.fields[i].yearsFallow += 1
                if self.fields[i].pos in self.farms:
                    self.farms[self.fields[i].pos].farmed = False
            
            # If statement to add fallowlimit exceeding fields to an array of fields to delete
            if (self.fields[i].yearsFallow >= self.model.fallowLimit):
                self.model.grid.remove_agent(self.farms[self.fields[i].pos])# Remove the farm from the map
                del self.farms[self.fields[i].pos] # Remove the farm from list 
                # Reset ownership
                self.fields[i].owned = False
                self.fields[i].owner = None
                toDel.append(i - len(toDel)) # Subtract to account for array shrinkage as deletion happens

        # Remove all fallowlimit exceded fields from the Households ownership, does not remove agent
        for i in toDel:
            del self.fields[i] # Delete the field

    def fission(self):
        """ Performs household fission if enabled"""
        # If allowed
        if self.model.fission:
            # If chance is met
            if self.model.fissionChance < np.random.uniform(0,1):
                # If requirements are met, create a splinter household
                if self.workers >= 15 and self.grain > (3 * self.workers * (164)):
                    uid = "h" + str(self.model.schedule.get_breed_count(Household) + 1)
                    ambition =  np.random.uniform(self.model.minAmbition, 1)
                    competency = np.random.uniform(self.model.minCompetency, 1)
                    genCount = random.randrange(5) + 10
                    household = Household(uid, self.model, self.settlement, self.pos, 1100, # Grain for 5 workers and 1 field
                                        5, ambition, competency, genCount)
                    self.model.schedule.add(household) # Add to scheduler
                    self.workers -= 5
                    self.grain -= 5

    def step(self):
        """
        The actions to take on a general step sequence
        """
        self.workersWorked = 0
        self.claimFields()
        self.farm(self.fields, False)
        self.consumeGrain()
        self.storageLoss()
        self.fieldChangeover()
        self.genChangeover()
        self.populationShift()

    def stepFarm(self):
        """
        Calls the farming methods for the initial run of households in the scheduler
        """
        # Reset parameters
        self.workersWorked = 0
        # Farm
        self.claimFields()
        self.farm(self.fields, False)
    
    def stepRentConsumeChangeover(self, fields):
        """
        Calls the renting, aging, changeover and methods
        """
        self.rent(fields)
        self.consumeGrain()
        self.storageLoss()
        self.fieldChangeover()
        self.genChangeover()
        self.populationShift()
        self.fission()
        # Update grain max for datacollector
        if self.grain > self.model.maxHouseholdGrain:
            self.model.maxHouseholdGrain = self.grain


class Farm(Tile):
    """Farm stub object for visualsiation purposes"""

    color = ""
    farmed = False

    def __init__(self, unique_id: int, model, pos: tuple, color: str = "#FFFFFF", farmed: bool = False):
        super().__init__(unique_id, model, pos)
        self.color = color
        self.farmed = farmed
