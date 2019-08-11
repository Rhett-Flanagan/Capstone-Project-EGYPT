# Polymorphic classes for use in the Map class
# Imports
from abc import ABC, abstractmethod
import math

class Tile:
    """Basic Tile Class"""
    # Variables
    __x = 0
    __y = 0

    # Methods
    def __init__(self, x: int, y: int):
        """
        Constructor Stub
        x: x coordinate
        y: y coordinate
        """
        self.__x = x
        self.__y = y
        pass

    def flood(self):
        """Flood Stub"""
        pass

    def out(self) -> str:
        """print stub for demo"""
        pass

class River(Tile):
    """
    River Child Class
    Rivers don't do anything in the NetLogo implementation so currently a stub for the map to use
    """

    def out(self) -> str:
        """Print for demo"""
        return 'R'


class Settlement(Tile):
    """
    Settlement Child Class
    Implementation of settlements to act as a population hub on a Tile map
    """

    # Variables
    __noHouseholds = 0
    __pop = 0

    # Methods
    def __init__(self, x: int, y: int, nH: int, p: int):# Constructor
        """
        Constructor
        x:  x coordinate
        y:  y coordinate
        nh: Number of Households in the Settlement
        p:  Population of Settlement
        """
        Tile.__init__(self, x, y)
        self.__noHouseholds = nH
        self.__pop = p

    def flood(self):
        """Does nothing for now"""
        pass

    def out(self) -> str:
        """Print for demo"""
        return 'S'

class Field(Tile):
    """
    Field Child Class
    Implementation of fields to be claimed and farmed by houeseholds
    """

    # Variables
    __claimed = False
    __harvested = False
    __yearsHarvested = 0
    __yearsFallow = 0
    __fertility = 0
    __avf = 0

    # Methods
    def __init__(self, x: int, y: int, f: float):
        """
        Constructor
        x:   x coordinate
        y:   y coordinate
        f:   Fertility value
        """
        Tile.__init__(self, x, y)
        self.__fertility = f
        self.__avf = f
        

    def plant(self):
        """TODO"""
    
    def harvest(self):
        """
        Sets harvested totrue, used in conjunction with the farm() method in household
        """
        self.__harvested = True

    # def claimStatus(self, ):
    #     self.__claimed = True

    def flood(self, mu: float, sigma: float, alpha: float, beta: float, ticks: int):
        """
        Abstract representation of the annual Nile flood, asssigning a fertility value based on distance from water
        mu:    mean
        sigma: standard deviation
        alpha: alpha for normal distribution
        beta:  beta for normal distribution
        ticks: number of ticks that the simulation has run for
        """
        self.__fertility = 17 * ( beta * (math.exp(0 - (self.__x - mu) ** 2 /  alpha)))
        self.__avf = ((ticks * self.__avf) + self.__fertility)/(ticks + 1)
        self.__harvested = False

    def out(self) -> str:
        """Print for demo"""
        if(self.__harvested == False):
            return 'F'
        else:
            return 'H'