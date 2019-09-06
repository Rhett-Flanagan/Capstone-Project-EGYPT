import math
import random
import numpy as np

from mesa import Model
from mesa.datacollection import DataCollector
from mesa.space import MultiGrid

from src.agents import River, Field, Settlement, Household
from src.schedule import EgyptSchedule

# Data collctor methods
def gini(model):
    """Calculates the Gini-Index of the model"""
    # Sorting functor
    def wealth(agent):
        return agent.grain

    agents = model.schedule.get_breed(Household)
    # print(agent_wealths)
    agents.sort(key = wealth)
    x = []
    for agent in agents:
        x.append(agent.grain)
    N = model.schedule.get_breed_count(Household)
    # Avoid divide by 0 errors
    if N != 0:
        B = sum(xi * (N - i) for i, xi in enumerate(x)) / (N * sum(x))
        return round((1 + (1 / N) - 2 * B), 2)
    else:
        return 0

def minSetPop(model):
    """Finds the minimum settlement population in the model"""
    settlements = model.schedule.get_breed(Settlement)
    minPop = float("inf") # Workaround of removal of sys.maxint
    for settlement in settlements:
        if(minPop > settlement.population):
            minPop = settlement.population
    return minPop

def maxSetPop(model):
    """Finds the maximum settlement population in the model"""
    settlements = model.schedule.get_breed(Settlement)
    maxPop = 0
    for settlement in settlements:
        if(maxPop < settlement.population):
            maxPop = settlement.population
    return maxPop

def meanSetPop(model):
    """Finds the mean settlement population in the model"""
    settlements = model.schedule.get_breed(Settlement)
    meanPop = 0
    for settlement in settlements:
        meanPop += settlement.population
    if model.schedule.get_breed_count(Settlement) != 0:
        return round(meanPop/model.schedule.get_breed_count(Settlement), 2)
    else:
        return 0

def minHWealth(model):
    """Finds the minimum household wealth in the model"""
    households = model.schedule.get_breed(Household)
    minWealth = float("inf") # Workaround of removal of sys.maxint
    for household in households:
        if(minWealth > household.grain):
            minWealth = household.grain
    return minWealth

def maxHWealth(model):
    """Finds the maximum household wealth in the model"""
    households = model.schedule.get_breed(Household)
    maxWealth = 0
    for household in households:
        if(maxWealth < household.grain):
            maxWealth = household.grain
    return maxWealth

def meanHWealth(model):
    """Finds the mean household wealth in the model"""
    households = model.schedule.get_breed(Household)
    meanWealth = 0
    for household in households:
        meanWealth += household.grain
    if model.schedule.get_breed_count(Household) != 0:
        return round(meanWealth/model.schedule.get_breed_count(Household), 2)
    else:
        return 0


def lowerThirdGrainHoldings(model):
    """ Determines the number of households that hold below 33% of the highest grain total"""
    households = model.schedule.get_breed(Household)
    count = 0
    for household in households:
        if household.grain <= (model.maxHouseholdGrain / 3):
            count += 1
    return count

def middleThirdGrainHoldings(model):
    """ Determines the number of households that hold between 33% and 66% of the highest grain total"""
    households = model.schedule.get_breed(Household)
    count = 0
    for household in households:
        if ((household.grain > (model.maxHouseholdGrain / 3)) and (household.grain <= ( 2 * model.maxHouseholdGrain / 3))):
            count += 1
    return count

def upperThirdGrainHoldings(model):
    """ Determines the number of households that hold above 66% of the highest grain total"""
    households = model.schedule.get_breed(Household)
    count = 0
    for household in households:
        if household.grain > ( 2 * model.maxHouseholdGrain / 3):
            count += 1
    return count

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
    rental = True
    rentalRate = 0.5
    totalPopulation = startingSettlements * startingHouseholds * startingHouseholdSize
    totalGrain = startingGrain * startingHouseholds
    startingPopulation = totalPopulation
    projectedHistoricalPopulation = totalPopulation
    maxHouseholdGrain = startingGrain

    # Step variables
    mu = 0
    sigma = 0
    alpha = 0
    beta = 0

    # Visualisation
    description = "A model simulating wealth growth and distribution in Ancient Egypt.\n\nThe model allows one to see how variables such as the flooding of the Nile, human character traits and random chance effect the acquisition and distribution of wealth."

    # List of identifiers and colors for settlements
    SETDICT = {"s1": "#FF0000",
               "s2": "#FF4500",
               "s3": "#BC8F8F",
               "s4": "#00FF00",
               "s5": "#00FFFF",
               "s6": "#0000FF",
               "s7": "#FF00FF",
               "s8": "#FF1493",
               "s9": "#708090",
               "s10": "#DC143C",
               "s11": "#FF8C00",
               "s12": "#FF69B4",
               "s13": "#800000",
               "s14": "#7CFC00",
               "s15": "#008B8B",
               "s16": "#483D8B",
               "s17": "#4B0082",
               "s18": "#FF69B4",
               "s19": "#000000",
               "s20": "#8B4513"}

    def __init__(self, height: int = 30, width: int = 30, timeSpan: int = 500,
                 startingSettlements: int = 14, startingHouseholds: int = 7,
                 startingHouseholdSize: int = 5, startingGrain: int = 3000,
                 minAmbition: float = 0.1, minCompetency: float = 0.5,
                 generationalVariation: float = 0.9, knowledgeRadius: int = 20,
                 distanceCost: int = 10, fallowLimit: int = 4, popGrowthRate: float = 0.1,
                 fission: bool = False, fissionChance: float = 0.7, rental: bool = True,
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
        # Map size
        self.height = height
        self.width = width

        # If the number of starting settlements is greater than the maximum reasonable number of households considering territory and farming area
        # Considers that each household needs at least two field to survive at a minimum number of members, a Settlment needs 9 (territory) + 2 * households
        # Tiles to survive
        if startingSettlements > ((width - 1) * height) // (9 + (startingHouseholds * 2)):
            if startingSettlements > 20:
                self.startingSettlements = 20
            else:
                self.startingSettlements = ((height - 1) * width) // (9 + (startingHouseholds * 2))
            print("Too many starting settlements to support the settlements and household, truncating to: ", self.startingSettlements)
        else:
            self.startingSettlements = startingSettlements
        # Simulation Variables
        self.timeSpan = timeSpan
        self.currentTime = 0
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
        self.startingPopulation = self.totalPopulation
        self.projectedHistoricalPopulation = self.startingPopulation
        self.maxHouseholdGrain = startingGrain

        # Scheduler and Grid
        self.schedule = EgyptSchedule(self)
        self.grid = MultiGrid(height = self.height, width = self.width, torus=False)

        # Define specific tables for data collection purposes
        setlist = []
        for i in range(self.startingSettlements):
            setlist.append("s" + str(i + 1) + "_Population")
        tables = {"Settlement Population": setlist}

        # Data collection
        self.datacollector = DataCollector(model_reporters = 
            {"Households": lambda m: m.schedule.get_breed_count(Household),
             "Settlements": lambda m: m.schedule.get_breed_count(Settlement),
             "Total Grain": lambda m: m.totalGrain,
             "Total Population": lambda m: m.totalPopulation,
             "Projected Hisorical Poulation (0.1% Growth)": lambda m: m.projectedHistoricalPopulation,
             "Gini-Index": gini,
             "Maximum Settlement Population": maxSetPop,
             "Minimum Settlement Population": minSetPop,
             "Mean Settlement Poulation" : meanSetPop,
             "Maximum Household Wealth": maxHWealth,
             "Minimum Household Wealth": minHWealth,
             "Mean Household Wealth" : meanHWealth,
             "Number of households with < 33% of wealthiest grain holding": lowerThirdGrainHoldings,
             "Number of households with 33 - 66%  of wealthiest grain holding": middleThirdGrainHoldings,
             "Number of households with > 66% of wealthiest grain holding": upperThirdGrainHoldings 
            },
            tables = tables)

        self.setup()
        self.running = True
        self.collectTableData()
        self.datacollector.collect(self)

    def collectTableData(self):
        setPops = {}
        for s in self.schedule.get_breed(Settlement):
            setPops[s.unique_id + "_Population"] = s.population
        self.datacollector.add_table_row("Settlement Population", setPops, True)

    def setupMapBase(self):
        """
        Create the grid as field and river
        """
        for agent, x, y in self.grid.coord_iter():
            # If on left edge, make a river
            if x == 0:
                uid = "r" + str(x) + "|" + str(y)
                river = River(uid, self, (x, y))
                self.grid.place_agent(river, (x, y))
            # Otherwise make a field
            else:
                uid = "f" + str(x) + "|" + str(y)
                field = Field(uid, self, (x, y), 0.0)
                self.grid.place_agent(field, (x, y))
                self.schedule.add(field)

    def setupSettlementsHouseholds(self):
        """
        Add settlements and households to the simulation
        """
        h = 1
        for i in range(self.startingSettlements):
            # Loop untill a suitable location is found
            while True:
                x = self.random.randrange(1, self.width)
                y = self.random.randrange(self.height)

                flag = False
                cell = self.grid.get_cell_list_contents((x, y))
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
            uid = "s" + str(i + 1) # Use a custom id for the datacollector
            settlement = Settlement(uid, self, (x, y), population, self.startingHouseholds, uid, self.SETDICT[uid])
            self.grid.place_agent(settlement, (x, y))

            # Set the surrounding fields as territory
            local = self.grid.get_neighbors((x, y), moore=True, include_center=True, radius=1)
            for a in local:
                a.settlementTerritory = True

            # Add households for the settlement to the scheduler
            for j in range(self.startingHouseholds):
                huid = "h" + str(h) # Use a custom id for the datacollector
                ambition =  np.random.uniform(self.minAmbition, 1)
                competency = np.random.uniform(self.minCompetency, 1)
                genCount = self.random.randrange(5) + 10
                household = Household(huid, self, settlement, (x, y), self.startingGrain,
                                      self.startingHouseholdSize, ambition, competency, genCount)
                # ! Dont add household to grid, is redundant
                self.schedule.add(household)
                h += 1
            # Add settlement to the scheduler
            self.schedule.add(settlement)

    def setup(self):
        """
        Setup model parameters
        """
        self.setupMapBase()
        self.setupSettlementsHouseholds()

    def step(self):
        self.currentTime += 1
        self.maxHouseholdGrain = 0
        self.setupFlood()
        self.schedule.step()
        self.projectedHistoricalPopulation = round(self.startingPopulation * ((1.001) ** self.currentTime))
        self.datacollector.collect(self)
        # Add settlement data to table 
        self.collectTableData()
        # Cease running once time limit is reached or everyone is dead
        if self.currentTime >= self.timeSpan or self.totalPopulation == 0: 
            self.running = False
 
    def setupFlood(self):
        """
        Sets up common variables used for the flood method in Fields
        """
        self.mu = random.randint(0, 10) + 5
        self.sigma = random.randint(0, 5) + 5
        self.alpha = (2 * self.sigma ** 2)
        self.beta = 1 / (self.sigma * math.sqrt(2 * math.pi))