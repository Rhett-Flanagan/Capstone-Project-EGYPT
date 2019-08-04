import random


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
        for i in range(Map.__maxGrid):
            row = []
            for j in range(Map.__maxGrid):
                row.append(0)
            Map.__grid.append(row)

    # Print the grid upon which the simulation will occur (for testing purposes)
    def print(self):
        for i in range(Map.__maxGrid):
            for j in range(Map.__maxGrid):
                if j == Map.__maxGrid-1:
                    print(Map.__grid[i][j], end="\n")
                else:
                    print(Map.__grid[i][j], end=",")

    # Setup procedure including generation of maps, placement of river, placement of Settlements etc.
    def setup(self):
        Map.__setupRiver(self)
        Map.__setupSettlements(self)
        Map.__setupHouseholds(self)

    # Create the Nile river using river width variable for the size of the Nile
    def __setupRiver(self):
        for i in range(Map.__maxGrid):
            for j in range(Map.__maxGrid):
                if j <= Map.__riverWidth - 1:
                    Map.__grid[i][j] = 1

    # Create and place all the settlements on the grid, and enter them into an array of all settlements
    def __setupSettlements(self):
        count = 0
        while count < Map.__numberOfSettlements:
            xCord = random.randint(0, Map.__maxGrid-1)
            yCord = random.randint(0, Map.__maxGrid-1)
            if (Map.__grid[yCord][xCord] != 1) & (Map.__grid[yCord][xCord] != 2):
                Map.__grid[yCord][xCord] = 2
                count += 1
