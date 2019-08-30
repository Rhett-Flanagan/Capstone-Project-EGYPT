from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from src.agents import River, Field, Settlement
from src.model import EgyptSim

max = 1.36  # Max Fertility Value = The man, the myth, the legendary Rhett worked this out using really slow and manual machine learning

def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Field:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        if agent.settlementTerritory:
            portrayal["Color"] = ["Purple"]

        # elif agent.owned:
            # portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]

        #    fertilityValue = agent.fertility
        #   # Inverse for the  RGB Scale
        #    inverseFertilityValue = max - fertilityValue
        #    rValue = round(inverseFertilityValue * (255/max))
        #    hexValue = rgb_to_hex((rValue, 255, 0))
        #    portrayal["Color"] = [hexValue]

        else:

            fertilityValue = agent.fertility
            # Inverse for the  RGB Scale (0 - 255)
            inverseFertilityValue = max - fertilityValue
            # More fertile = Lower Value for R, More Prominent Green
            # Should return value between 0 (if fertility == max) and 255 (if fertility == 0)
            rValue = round(inverseFertilityValue * (255/max))
            if fertilityValue <= max/4:
                # Minimum (0) - Lower Quartile
                # Least Fertile - Yellow
                hexValue = rgb_to_hex((rValue, 240, 0))
                portrayal["Color"] = [hexValue]
            elif fertilityValue <= max/2:
                # Lower Quartile - Median
                # Less Fertile - Lighter Green
                hexValue = rgb_to_hex((rValue, 220, 0))
                portrayal["Color"] = [hexValue]
            elif fertilityValue <= max*3/4:
                # Median - Upper Quartile
                # More Fertile - Darker Green
                hexValue = rgb_to_hex((rValue, 200, 0))
                portrayal["Color"] = [hexValue]
            else:
                # Upper Quartile - Maximum (1.36)
                # Most Fertile - Dark Green
                hexValue = rgb_to_hex((rValue, 180, 0))
                print(hexValue)
                portrayal["Color"] = [hexValue]

    elif type(agent) is River:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "Blue"
    elif type(agent) is Settlement:
        portrayal["Shape"] = "src/res/settlement.png"
        # portrayal["Color"] = "Black"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        # portrayal["scale"] = 1
    return portrayal

model_params = {"height": 30, 
                "width": 30,
                "timeSpan": UserSettableParameter('slider', 'Model Time Span', 500, 100, 500, 25),
                "startingSettlements": UserSettableParameter('slider', 'Starting Settlements', 14, 5, 20),
                "startingHouseholds": UserSettableParameter('slider', 'Starting Households', 7, 1, 10),
                "startingHouseholdSize": UserSettableParameter('slider', 'Starting Household Size', 5, 1, 10),
                "startingGrain": UserSettableParameter('slider', 'Starting Grain', 3000, 100, 8000, 100),
                "minAmbition": UserSettableParameter('slider', 'Minimum Ambition', 0.1, 0.0, 1.0, 0.1),
                "minCompetency": UserSettableParameter('slider', 'Minimum Competency', 0.7, 0.0, 1.0, 0.1),
                "generationalVariation": UserSettableParameter('slider', 'Generational Variation', 0.9, 0.0, 1.0, 0.1),
                "knowledgeRadius": UserSettableParameter('slider', 'Knowledge Radius', 20, 5, 40, 5),
                "distanceCost": UserSettableParameter('slider', 'Distance Cost (in kg)', 10, 1, 15),
                "fallowLimit": UserSettableParameter('slider', 'Population Growth Rate (in %)', 0.010, 0.00, 0.050, 0.001),
                "fission": UserSettableParameter('checkbox', 'Allow Household Fission?', value=False),
                "fissionChance": UserSettableParameter('slider', 'Minimum Fission Chance', 0.7, 0.5, 0.9, 0.1),
                "rental": UserSettableParameter('checkbox', 'Allow Land Rental?', value=False),
                "rentalRate": UserSettableParameter('slider', 'Land Rental Rate', 0.5, 0.3, 0.6, 0.05)}

grid = CanvasGrid(portrayal, 30, 30, 600, 600)
chart = ChartModule([{"Label": "Total Grain", "Color": "Black"}], data_collector_name="datacollector")

server = ModularServer(EgyptSim, [grid, chart], "Egypt Sim", model_params)

server.port = 8521
# server.launch()
