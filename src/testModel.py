import unittest

from src.agents import Field, Settlement, River
from src.model import EgyptSim


class TestSetupMethods(unittest.TestCase):
    sim = EgyptSim(height=5, width=5, timeSpan=10, startingSettlements=2, startingHouseholds=2,
                   startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                   generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                   popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)

    def testConstructor(self):
        self.assertEqual(self.sim.height, 5)
        self.assertEqual(self.sim.width, 5)
        self.assertEqual(self.sim.timeSpan, 10)
        self.assertEqual(self.sim.startingSettlements, 2)
        self.assertEqual(self.sim.startingHouseholds, 2)
        self.assertEqual(self.sim.startingHouseholdSize, 2)
        self.assertEqual(self.sim.startingGrain, 5000)
        self.assertEqual(self.sim.minAmbition, 0.5)
        self.assertEqual(self.sim.minCompetency, 0.1)
        self.assertEqual(self.sim.generationalVariation, 0.7)
        self.assertEqual(self.sim.knowledgeRadius, 2)
        self.assertEqual(self.sim.distanceCost, 10)
        self.assertEqual(self.sim.fallowLimit, 1)
        self.assertEqual(self.sim.popGrowthRate, 0.2)
        self.assertEqual(self.sim.fission, False)
        self.assertEqual(self.sim.fissionChance, 0.5)
        self.assertEqual(self.sim.rental, False)
        self.assertEqual(self.sim.rentalRate, 0.1)

    def testGridSetup(self):
        """Test that the grid has been setup correctly """
        nRiver = 0
        nField = 0
        nSettlement = 0
        territory = True
        grid = self.sim.grid.get_neighbors((2, 2), True, True, 2)

        # Count instances of tile types and check territory
        for agent in grid:
            if isinstance(agent, River):
                nRiver += 1
            elif isinstance(agent, Field):
                nField += 1
            elif isinstance(agent, Settlement):
                nSettlement += 1
                local = self.sim.grid.get_neighbors(agent.pos, True, True, 1)
                # Check that territory is correct
                for a in local:
                    if not a.settlementTerritory:
                        territory = False

        self.assertEqual(nRiver, 5)  # 5 Tiles should be river
        self.assertEqual(nField, 20)  # 20 Tiles should be Field
        self.assertEqual(nSettlement, 2)  # There should be 2 Settlements
        self.assertTrue(territory)  # Territory is in correct regions

    def testSchedulerSetup(self):
        """Test that the scheduler was correctly generated"""
        dict = self.sim.schedule.agents_by_breed
        self.assertEqual(len(dict), 3)  # Should be 3 types of agent in scheduler

        f = False
        s = False
        h = False

        for agent_class in dict:
            if agent_class.__name__ == "Field":
                f = True
                self.assertEqual(len(list(dict[agent_class])), 20)  # Should be 20 Fields
            if agent_class.__name__ == "Settlement":
                s = True
                self.assertEqual(len(list(dict[agent_class])), 2)  # Should be 2 Settlements
            if agent_class.__name__ == "Household":
                h = True
                agent_keys = list(dict[agent_class].keys())
                for key in agent_keys:
                    pos = dict[agent_class][key].pos

                    print(pos)
                    lst = self.sim.grid.get_neighbors(pos = pos, moore = True, include_center = False, radius = self.sim.knowledgeRadius)
                    for n in lst:
                        print(n.pos, type(n).__name__)
                    print()
                self.assertEqual(len(list(dict[agent_class])), 4)  # Should be 4 Households

        self.assertTrue(f)  # Field is in the dictionary
        self.assertTrue(s)  # Settlement is in dictionary
        self.assertTrue(h)  # Household is in dictionary

    def testMetricsSetup(self):
        """Test that the metrics were correctly generated"""
        self.assertEqual(self.sim.totalGrain, self.sim.startingSettlements * self.sim.startingHouseholds * self.sim.startingGrain)  # Grain calculation was correctly done
        self.assertEqual(self.sim.totalPopulation, self.sim.startingSettlements * self.sim.startingHouseholds * self.sim.startingHouseholdSize) # Population was correctly setup

    def testClaimLogic(self):
        """Test that farm operates correctly"""
        

class TestAgentLogic(unittest.TestCase):
    sim = EgyptSim(height=5, width=5, timeSpan=10, startingSettlements=2, startingHouseholds=2,
                   startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                   generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                   popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)

    
    def testConsumeGrain(self):
        """Test that the grain is consumed (reduced) correctly """
        


def suite():
    """
    Gather all tests from this module into a test suite
    """
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestSetupMethods))

    return testSuite
