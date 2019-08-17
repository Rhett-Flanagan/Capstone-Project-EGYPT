import unittest

from src.model import EgyptSim
from src.agents import Field, Settlement, River, Household

class TestSetupMethods(unittest.TestCase):
    sim = EgyptSim(height = 5, width = 5, startingSettlements = 2, startingHouseholds = 2)
    
    def testGridSetup(self):
        """Test that the grid has been setup correctly """
        nRiver = 0
        nField = 0
        nSettlement = 0
        territory = True
        grid = self.sim.grid.get_neighbors((2,2), True, True, 2)
        for agent in grid:
            if type(agent) == River:
                nRiver += 1
            elif type(agent) ==  Field:
                nField +=1
            elif type(agent) ==  Settlement:
                nSettlement +=1
                local = self.sim.grid.get_neighbors(agent.pos, True, True, 1)
                for a in local:
                    if not a.settlementTerritory:
                        territory = False
        
        self.assertEqual(nRiver, 5) # 5 Tiles should be river
        self.assertEqual(nField, 20) # 20 Tiles should be Field
        self.assertEqual(nSettlement, 2) # There should be 2 Settlements
        self.assertTrue(territory) # The territory should be correctly set up

    def testSchedulerSetup(self):
        """Test that the scheduler was correctly generated"""
        dict = self.sim.schedule.agents_by_breed
        self.assertEqual(len(dict), 3) # Should be 3 types of agent in scheduler

        f = False
        s = False
        h = False

        for agent_class in dict:
            if agent_class.__name__ == "Field":
                f = True
                self.assertEqual(len(list(dict[agent_class])), 20) # Should be 20 Fields
            if agent_class.__name__ == "Settlement":
                s = True
                self.assertEqual(len(list(dict[agent_class])), 2) # Should be 2 Settlements
            if agent_class.__name__ == "Household":
                h = True
                self.assertEqual(len(list(dict[agent_class])), 4) # Should be 4 Households
        
        self.assertTrue(f) # Field is in the dictionary
        self.assertTrue(s) # Settlement is in dictionary
        self.assertTrue(h) # Household is in dictionary

    def testMetricsSetup(self):
        """Test that the metrics were correctly generated"""
        self.assertEqual(self.sim.totalGrain, 2 * 2 * 3000) # Grain calculation was correctly done
        self.assertEqual(self.sim.totalPopulation, 2 * 2 * 5)
        


def suite():
    """
    Gather all tests from this module into a test suite
    """
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestSetupMethods))

    return testSuite