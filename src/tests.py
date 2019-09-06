import unittest
import math

from src.agents import Field, Settlement, River, Household
from src.model import EgyptSim, gini, minSetPop, maxSetPop, meanSetPop, minHWealth, maxHWealth, meanHWealth, lowerThirdGrainHoldings, middleThirdGrainHoldings, upperThirdGrainHoldings


class TestSetupMethods(unittest.TestCase):

    def testConstructor(self):
        """ Test that the constructor creates values as expected """
        sim = EgyptSim()  # Test default
        self.assertEqual(sim.height, 30)
        self.assertEqual(sim.width, 30)
        self.assertEqual(sim.timeSpan, 500)
        self.assertEqual(sim.startingSettlements, 14)
        self.assertEqual(sim.startingHouseholds, 7)
        self.assertEqual(sim.startingHouseholdSize, 5)
        self.assertEqual(sim.startingGrain, 3000)
        self.assertEqual(sim.minAmbition, 0.1)
        self.assertEqual(sim.minCompetency, 0.5)
        self.assertEqual(sim.generationalVariation, 0.9)
        self.assertEqual(sim.knowledgeRadius, 20)
        self.assertEqual(sim.distanceCost, 10)
        self.assertEqual(sim.fallowLimit, 4)
        self.assertEqual(sim.popGrowthRate, 0.1)
        self.assertEqual(sim.fission, False)
        self.assertEqual(sim.fissionChance, 0.7)
        self.assertEqual(sim.rental, True)
        self.assertEqual(sim.rentalRate, 0.5)

        sim = EgyptSim(6, 5, 10, 2, 1, 10, 5000, 0.3, 0.7, 0.1, 2, 5, 1, 0.2, True, 0.1, False, 0.1)  # Test parameters
        self.assertEqual(sim.height, 6)
        self.assertEqual(sim.width, 5)
        self.assertEqual(sim.timeSpan, 10)
        self.assertEqual(sim.startingSettlements, 2)
        self.assertEqual(sim.startingHouseholds, 1)
        self.assertEqual(sim.startingHouseholdSize, 10)
        self.assertEqual(sim.startingGrain, 5000)
        self.assertEqual(sim.minAmbition, 0.3)
        self.assertEqual(sim.minCompetency, 0.7)
        self.assertEqual(sim.generationalVariation, 0.1)
        self.assertEqual(sim.knowledgeRadius, 2)
        self.assertEqual(sim.distanceCost, 5)
        self.assertEqual(sim.fallowLimit, 1)
        self.assertEqual(sim.popGrowthRate, 0.2)
        self.assertEqual(sim.fission, True)
        self.assertEqual(sim.fissionChance, 0.1)
        self.assertEqual(sim.rental, False)
        self.assertEqual(sim.rentalRate, 0.1)

        sim = EgyptSim(startingSettlements=200, startingHouseholds=5)  # Too many settlements
        self.assertEqual(sim.height, 30)
        self.assertEqual(sim.width, 30)
        self.assertEqual(sim.timeSpan, 500)
        self.assertEqual(sim.startingSettlements, 20)
        self.assertEqual(sim.startingHouseholds, 5)
        self.assertEqual(sim.startingHouseholdSize, 5)
        self.assertEqual(sim.startingGrain, 3000)
        self.assertEqual(sim.minAmbition, 0.1)
        self.assertEqual(sim.minCompetency, 0.5)
        self.assertEqual(sim.generationalVariation, 0.9)
        self.assertEqual(sim.knowledgeRadius, 20)
        self.assertEqual(sim.distanceCost, 10)
        self.assertEqual(sim.fallowLimit, 4)
        self.assertEqual(sim.popGrowthRate, 0.1)
        self.assertEqual(sim.fission, False)
        self.assertEqual(sim.fissionChance, 0.7)
        self.assertEqual(sim.rental, True)
        self.assertEqual(sim.rentalRate, 0.5)

    def testGridSetup(self):
        """Test that the grid has been setup correctly """
        sim = EgyptSim(height=11, width=11, timeSpan=10, startingSettlements=2, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        nRiver = 0
        nField = 0
        nSettlement = 0
        territory = True
        grid = sim.grid.get_neighbors((5, 5), True, True, 5)

        # Count instances of tile types and check territory
        for agent in grid:
            if isinstance(agent, River):
                nRiver += 1
            elif isinstance(agent, Field):
                nField += 1
            elif isinstance(agent, Settlement):
                nSettlement += 1
                local = sim.grid.get_neighbors(agent.pos, True, True, 1)
                # Check that territory is correct
                for a in local:
                    if not a.settlementTerritory:
                        territory = False

        self.assertEqual(nRiver, 11)  # 10 Tiles should be river
        self.assertEqual(nField, 110)  # 90 Tiles should be Field
        self.assertEqual(nSettlement, 2)  # There should be 2 Settlements
        self.assertTrue(territory)  # Territory is in correct regions

    def testSchedulerSetup(self):
        """Test that the scheduler was correctly generated"""
        sim = EgyptSim(height=6, width=5, timeSpan=10, startingSettlements=2, startingHouseholds=1,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        dict = sim.schedule.agents_by_breed
        self.assertEqual(len(dict), 3)  # Should be 3 types of agent in scheduler

        f = False
        s = False
        h = False

        for agent_class in dict:
            if agent_class.__name__ == "Field":
                f = True
                self.assertEqual(len(list(dict[agent_class])), 24)  # Should be 24 Fields
            if agent_class.__name__ == "Settlement":
                s = True
                self.assertEqual(len(list(dict[agent_class])), 2)  # Should be 2 Settlements
            if agent_class.__name__ == "Household":
                h = True
                self.assertEqual(len(list(dict[agent_class])), 2)  # Should be 2 Households

        self.assertTrue(f)  # Field is in the dictionary
        self.assertTrue(s)  # Settlement is in dictionary
        self.assertTrue(h)  # Household is in dictionary

    def testMetricsSetup(self):
        """Test that the metrics were correctly generated"""
        sim = EgyptSim(height=10, width=10, timeSpan=10, startingSettlements=2, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertEqual(sim.totalGrain, 2 * 2 * 5000)  # Grain calculation was correctly done
        self.assertEqual(sim.totalPopulation, 2 * 2 * 2)  # Population was correctly setup

    def testFloodSetup(self):
        """Test that floodSetup generates correct values"""
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=2, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        sim.setupFlood()
        alpha = (2 * sim.sigma ** 2)
        beta = 1 / (sim.sigma * math.sqrt(2 * math.pi))
        # Use almostEqual because float calulations can be dodgy
        self.assertAlmostEqual(alpha, sim.alpha)
        self.assertAlmostEqual(beta, sim.beta)


class TestDataCollectorMethods(unittest.TestCase):

    def testGini(self):
        """ Tests that the Gini index is calculated correctly and that divide by zero errors are handled"""

        # Start with perfect equality
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=2, startingHouseholds=50,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)

        # Almost Equal for float comparison, should be zero at start for perfect equality at start
        self.assertAlmostEqual(gini(sim), 0)

        # Modify for perfect inequality
        wealth = True
        for h in sim.schedule.get_breed(Household):
            # Make one household have all wealth
            if wealth:
                h.grain = 5000
                wealth = False
            else:
                h.grain = 0
        # Almost Equal for float comparison, will be close to 1 for large numbers of households, 0.99 for the smaller number here
        self.assertAlmostEqual(gini(sim), 0.99)

        # Modify for predeterimed values at some other point in gini index
        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        self.assertAlmostEqual(gini(sim), 0.33)  # Almost Equal for float comparison

        # Force 0 Households, divide by 0 error
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=0, startingHouseholds=0,
                       startingHouseholdSize=0, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)

        self.assertAlmostEqual(gini(sim), 0)

    def testMinSetPop(self):
        """ Test that the correct minimum settlement population is obtained"""
        # Equal populations
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=4, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertEqual(minSetPop(sim), 4)

        # Different Populations
        i = 10
        for s in sim.schedule.get_breed(Settlement):
            s.population = i
            i += 10

        self.assertEqual(minSetPop(sim), 10)

    def testMaxSetPop(self):
        """ Test that the correct maxmimum settlement population is obtained"""
        # Equal populations
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=4, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertEqual(maxSetPop(sim), 4)

        # Different Populations
        i = 10
        for s in sim.schedule.get_breed(Settlement):
            s.population = i
            i += 10

        self.assertEqual(maxSetPop(sim), 40)

    def testMeanSetPop(self):
        """ Test that the correct mean settlement population is obtained"""
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=4, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertAlmostEqual(meanSetPop(sim), 4)

        # Different Populations
        i = 10
        for s in sim.schedule.get_breed(Settlement):
            s.population = i
            i += 10

        self.assertAlmostEqual(meanSetPop(sim), 25)

    def testMinHWealth(self):
        """ Test that the correct minimum household wealth is obtained """
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=4, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertEqual(minHWealth(sim), 5000)

        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        self.assertEqual(minHWealth(sim), 1000)

    def testMaxHWealth(self):
        """ Test that the correct maximum household wealth is obtained """
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=4, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertEqual(maxHWealth(sim), 5000)

        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        self.assertEqual(maxHWealth(sim), 8000)

    def testMeanHWealth(self):
        """ Test that the correct mean household wealth is obtained """
        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=4, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        self.assertAlmostEqual(meanHWealth(sim), 5000)

        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        self.assertAlmostEqual(meanHWealth(sim), 4500)

    def testLowerThirdGrainHoldings(self):
        """ Tests that the correct number of households are below the 1/3 grain threshold"""

        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=3, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        sim.maxHouseholdGrain = 9000

        self.assertAlmostEqual(lowerThirdGrainHoldings(sim), 3)

    def testMiddleThirdGrainHoldings(self):
        """ Tests that the correct number of households are between the 1/3 -2/3 grain thresholds """

        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=3, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        sim.maxHouseholdGrain = 9000

        self.assertAlmostEqual(lowerThirdGrainHoldings(sim), 3)

    def testUpperThirdGrainHoldings(self):
        """ Tests that the correct number of households are above the 2/3 grain threshold"""

        sim = EgyptSim(height=30, width=30, timeSpan=10, startingSettlements=3, startingHouseholds=2,
                       startingHouseholdSize=2, startingGrain=5000, minAmbition=0.5, minCompetency=0.1,
                       generationalVariation=0.7, knowledgeRadius=2, distanceCost=10, fallowLimit=1,
                       popGrowthRate=0.2, fission=False, fissionChance=0.5, rental=False, rentalRate=0.1)
        i = 1000
        for h in sim.schedule.get_breed(Household):
            h.grain = i
            i += 1000

        sim.maxHouseholdGrain = 9000

        self.assertAlmostEqual(lowerThirdGrainHoldings(sim), 3)


def suite():
    """
    Gather all tests from this module into a test suite
    """
    testSuite = unittest.TestSuite()
    testSuite.addTest(unittest.makeSuite(TestSetupMethods))
    testSuite.addTest(unittest.makeSuite(TestDataCollectorMethods))

    return testSuite
