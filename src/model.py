from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
import numpy as np
import random
import math

from src.agents import River, Field, Settlement, Household
from src.schedule import RandomActivationByBreed

class EgyptSim(Model):
    """
    Simulation Model for wealth distribution represented by grain in ancient Egypt
    """

    # Variable declarations for non python programmer sanity
    # Map variables
    height = 30
    width = 30

    # Simulation Variables
    timeSpan = 500
    currentTime = 0
    startingSettlements = 14
    startingHouseholds = 7
    startingHouseholdSize = 5
    startingGrain = 3000
    minAmbition = 0.1
    minCompetency = 0.5
    generationalVariation = 0.9
    knowledgeRadius = 20
    distanceCost = 10
    fallowLimit = 4
    popGrowthRate = 0.1
    fission = False
    fissionChance = 0.7
    rental = False
    rentalRate = 0.5
    totalGrain = 0
    totalPopulation = 0

    # Step variables
    mu = 0
    sigma = 0
    alpha = 0
    beta = 0

    # Debug
    verbose = False

    # Visualisation
    description = "A model simulating wealth growth and distribution in Ancient Egypt"

    def __init__(self, height: int = 30, width: int = 30, timeSpan: int = 500,
                startingSettlements: int = 14, startingHouseholds: int = 7,
                startingHouseholdSize: int = 5, startingGrain: int = 3000,
                minAmbition: float = 0.1, minCompetency: float = 0.5,
                generationalVariation: float = 0.9, knowledgeRadius: int = 20,
                distanceCost: int = 10, fallowLimit: int = 4, popGrowthRate: float = 0.1,
                fission: bool = False, fissionChance: float = 0.7, rental: bool = False,
                rentalRate: float = 0.5):
        """
        Create a new EgyptSim model
        Args:
            height: The height of the simulation grid
            width: The width of the simulation grid
            timeSpan: The number of years over which the model is to run
            startingSettlements: The starting number of Settlements 
            startingHouseholds: The starting number of Households per Settlement
            startingHouseholdSize: The starting number of workers in a Household
            startingGrain: The starting amount of grain for each Household
            minAmbition: The minimum ambition value for a Household
            minCompetency: The minimum competency value for a Household
            generationalVariation: The difference between generations of a Household
            knowledgeRadius: How far outside ther Settlement a Household can "see"
            distanceCost: The cost to move grain per cell away from a settlemnt
            fallowLimit: The number of years a field can lay fallow before it is harvested
            popGrowthRate: The rate at which the population grows
            fission: If Household fission (Moving between settlements) is allowed
            fissionChance: The chance fission occuring
            rental: If land rental is allowed
            rentalRate: The rate at which households will rent land
        """
        super().__init__()
        # Set Parameters
        # Map variables
        self.height = height
        self.width = width

        # Simulation Variables
        self.timeSpan = timeSpan
        self.currentTime = 0
        self.startingSettlements = startingSettlements
        self.startingHouseholds = startingHouseholds
        self.startingHouseholdSize = startingHouseholdSize
        self.startingGrain = startingGrain
        self.minAmbition = minAmbition
        self.minCompetency = minCompetency
        self.generationalVariation = generationalVariation
        self.knowledgeRadius = knowledgeRadius
        self.distanceCost = distanceCost
        self.fallowLimit = fallowLimit
        self.popGrowthRate = popGrowthRate
        self.fission = fission
        self.fissionChance = fissionChance
        self.rental = rental
        self.rentalRate = rentalRate
        self.totalGrain = startingGrain * startingHouseholds * startingSettlements
        self.totalPopulation = startingSettlements * startingHouseholds * startingHouseholdSize

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus = False)
        # TODO Setup full data collection
        # self.datacollector = DataCollector(
        #     {"Households": lambda m: m.schedule.get_breed_count(Household),
        #      "Settlements": lambda m: m.schedule.get_breed_count(Settlement),
        #     })

        self.datacollector = DataCollector(model_reporters = {"Total Grain" : lambda m: m.totalGrain})

        self.setup()
        self.running = True
        self.datacollector.collect(self)
    
    # def getTotalGrain(self):
    #     return self.totalGrain

    def setupMapBase(self):
        """
        Create the grid as field and river
        """
        for agent, x, y in self.grid.coord_iter():
            # If on left edge, make a river
            if x == 0:
                river = River(self.next_id(), self, (x, y))
                self.grid.place_agent(river, (x, y))
            # Otherwise make a field
            else:
                field = Field(self.next_id(), self, (x, y), 0.0)
                self.grid.place_agent(field, (x, y))
                self.schedule.add(field)

    def setupSettlementsHouseholds(self):
        """
        Add settlements and households to the simulation
        """
        for i in range(self.startingSettlements):
            # Loop untill a suitable location is found
            while True:
                x = self.random.randrange(1, self.width)
                y = self.random.randrange(self.height)

                flag = False
                cell = self.grid.get_cell_list_contents((x,y))
                # Check that tile is available
                for agent in cell:
                    if agent.settlementTerritory:
                        break
                    else:
                        flag = True
                        break

                if flag:
                    break

            # Add settlement to the grid
            population = self.startingHouseholds * self.startingHouseholdSize
            settlement = Settlement(self.next_id(), self, (x, y), population, self.startingHouseholds)
            self.grid.place_agent(settlement, (x, y))

            # Set the surrounding fields as territory
            local = self.grid.get_neighbors((x,y), moore = True, include_center = True, radius = 1)
            for a in local:
                a.settlementTerritory = True
                # print(type(a), a.pos, a.settlementTerritory, sep = "\t")
            self.schedule.add(settlement)

            # Add households for the settlement to the scheduler
            for j in range(self.startingHouseholds):
                ambition = self.minAmbition + np.random.uniform(0, 1 - self.minAmbition)
                competency = self.minCompetency + np.random.uniform(0, 1 - self.minCompetency)
                genCount = self.random.randrange(5)
                household = Household(self.next_id(), self, (x, y), self.startingGrain,
                                      self.startingHouseholdSize, ambition, competency,
                                      genCount)
                #! Dont add household to grid, that is redundant
                self.schedule.add(household)

    def setup(self):
        """
        Setup model parameters
        """
        self.setupMapBase()
        self.setupSettlementsHouseholds()  
        

    def step(self):
        self.currentTime += 1
        self.setupFlood()
        self.schedule.step()
        self.datacollector.collect(self)
    
    def setupFlood(self):
        """
        Variables used for flood methods for fields
        """
        self.mu = random.randint(0, 11) + 5
        self.sigma = random.randint(0, 6) + 5
        self.alpha = (2 * self.sigma ** 2)
        self.beta = 1/(self.sigma * math.sqrt( 2 * math.pi))