import random
import Tile

class Map:
    """Terrain Class"""
    """
    1 - Represents the Nile River
    2 - Settlements
    """

    __grid = []
    # All these values could be changed by user input through GUI
    __maxGrid = 30
    __numberOfHouseholds = 5
    __numberOfSettlements = 15
    __riverWidth = 1
    __settlements = []

    # Variables as set by Analysis Diagram
    __aveAmbition = 0.0
    __aveCompetency = 0.0
    __floodLevel = 0.0
    __giniIndex = 0.0
    __lorenzPoints = 0.0
    __projectedPopulation = 0
    __totalGrain = 0
    __totalPopulation = 0

    # Create the grid upon which the simulation occurs (30 by 30)
    def __init__(self):
        for i in range(self.__maxGrid):
            row = []
            for j in range(self.__maxGrid):
                row.append(Tile.Field(i, j, 0))
            self.__grid.append(row)

    # Print the grid upon which the simulation will occur (for testing purposes)
    def print(self):
        for i in range(self.__maxGrid):
            for j in range(self.__maxGrid):
                if j == self.__maxGrid-1:
                    print(self.__grid[i][j].out(), end="\n")
                else:
                    print(self.__grid[i][j].out(), end=",")

    # Setup procedure including generation of maps, placement of river, placement of Settlements etc.
    def setup(self):
        self.__setupRiver()
        self.__setupSettlements()
        # Map.__setupHouseholds(self)

    # Create the Nile river using river width variable for the size of the Nile
    def __setupRiver(self):
        for i in range(self.__maxGrid):
            for j in range(self.__maxGrid):
                if j <= self.__riverWidth - 1:
                    self.__grid[i][j] = Tile.River(i, j)

    # Create and place all the settlements on the grid, and enter them into an array of all settlements
    def __setupSettlements(self):
        count = 0
        while count < self.__numberOfSettlements:
            xCord = random.randint(0, self.__maxGrid-1)
            yCord = random.randint(0, self.__maxGrid-1)
            if (type(self.__grid[yCord][xCord]).__name__ != "River") & (type(self.__grid[yCord][xCord]).__name__ != "Settlement"):
                self.__grid[yCord][xCord] = Tile.Settlement(xCord, yCord, 0, 0)
                count += 1
