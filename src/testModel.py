import unittest

from src.model import EgyptSim

class TestSetupMethods(unittest.TestCase):
    sim = EgyptSim(height = 3, width = 3, startingSettlements = 1, startingHouseholds = 1)
    # sim.setupMapBase()
    # for agent
    local = sim.grid.get_neighbors((1,1), moore = True, include_center = True, radius = 1)
    print()
    for a in local:
        print(type(a), a.pos, a.settlementTeritory, sep = "\t")

def suite():
    """
    Gather all tests from this module into a test suite
    """
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestSetupMethods))

    return testSuite