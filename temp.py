from mesa.batchrunner import BatchRunner
import pandas
import numpy as np
from src.model import EgyptSim
from src.agents import Household

# Parameters
# params = dict(height = [30], width = [30], timeSpan = [100],
#               startingSettlements = [14], startingHouseholds = [7],
#               # Vary Household size from 1 to 10
#               startingHouseholdSize = np.linspace(1, 10, 1)[1:],
#               startingGrain = [3000], minAmbition = [0.1], minCompetency = [0.5],
#               generationalVariation = [0.9], knowledgeRadius = [20],
#               distanceCost = [10], fallowLimit = [4], popGrowthRate = [0.1],
#               fission = [False], fissionChance = [0.7], rental = [True],
#               rentalRate = [0.5])

params = dict(timeSpan = [100],
    startingHouseholdSize = np.linspace(1, 10, 1)[1:]
)


# Reporter, Note that this is in the same format as the model DataCollector
m_reporters = {
    "Households": lambda m: m.schedule.get_breed_count(Household),
    "Total Population": lambda m: m.totalPopulation
}

# Create the batch runner
batch = BatchRunner(EgyptSim, params, model_reporters = m_reporters)

batch.run_all()

print(batch.model_vars)