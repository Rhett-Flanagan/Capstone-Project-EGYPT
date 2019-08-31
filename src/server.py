from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from src.agents import River, Field, Settlement
from src.model import EgyptSim

max = 1.36  # Max Fertility Value = The man, the myth, the legendary Rhett worked this out using really slow and manual machine learning


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb

def shade(percent):
    r = 255 - round(255 * percent) # Difference between yellow and dark green on red channel
    g = 255 - round(176 * percent) # Difference between yellow and dark green on green channel
    b = 102 - round(74 * percent) # Difference between yellow and dark green on blue channel
    return (r, g, b)


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
        fertilityValue = agent.fertility
        # Inverse for the  RGB Scale (0 - 255)
        #inverseFertilityValue = max - fertilityValue
        # if agent.owned:
        #     portrayal["Color"] = "Purple"
        # else:
        portrayal["Color"] = rgb_to_hex(shade(fertilityValue/max))
        # More fertile = Lower Value for R, More Prominent Green
        # Should return value between 0 (if fertility == max) and 255 (if fertility == 0)
        #rValue = round(inverseFertilityValue * (255 / max))
        # if fertilityValue <= max / 4:
        #     # Minimum (0) - Lower Quartile
        #     # Least Fertile - Yellow
        #     hexValue = rgb_to_hex((rValue, 240, 0))
        #     portrayal["Color"] = [hexValue]
        # elif fertilityValue <= max / 2:
        #     # Lower Quartile - Median
        #     # Less Fertile - Lighter Green
        #     hexValue = rgb_to_hex((rValue, 220, 0))
        #     portrayal["Color"] = [hexValue]
        # elif fertilityValue <= max * 3 / 4:
        #     # Median - Upper Quartile
        #     # More Fertile - Darker Green
        #     hexValue = rgb_to_hex((rValue, 200, 0))
        #     portrayal["Color"] = [hexValue]
        # else:
        #     # Upper Quartile - Maximum (1.36)
        #     # Most Fertile - Dark Green
        #     hexValue = rgb_to_hex((rValue, 180, 0))
        #     # print(hexValue)
        #     portrayal["Color"] = [hexValue]



    elif type(agent) is River:
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1
        portrayal["Color"] = "Blue"
    elif type(agent) is Settlement:
        portrayal["Shape"] = "circle"
        portrayal["Color"] = agent.color
        #portrayal["text"] = (agent.uid + str(agent.population)) # Cant make this transparent so it only appears on tooltip
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 1
        # Set size according to population
        if agent.population > 150:
            portrayal["r"] = 2
        elif agent.population > 100 and agent.population < 150:
            portrayal["r"] = 1.5
        elif agent.population > 50 and agent.population < 100:
            portrayal["r"] = 1
        else:
            portrayal["r"] = 0.5

    return portrayal


# List to display settlments in graph
SETDICT = {"s1": "#F08080",
           "s2": "#FF4500",
           "s3": "#FFFF00",
           "s4": "#FF8C00",
           "s5": "#7CFC00",
           "s6": "#006400",
           "s7": "#808000",
           "s8": "#00FFFF",
           "s9": "#008080",
           "s10": "#0000FF",
           "s11": "#FF00FF",
           "s12": "#FF69B4",
           "s13": "#000000",
           "s14": "#800000",
           "s15": "#BC8F8F",
           "s16": "#D2691E",
           "s17": "#8B4513",
           "s18": "#800080",
           "s19": "#4B0082",
           "s20": "#2E8B57"}

# Grid element for rendering
grid = CanvasGrid(portrayal, 30, 30, 600, 600)

# Chart elements for rendering
totalGrainChart = ChartModule([{"Label": "Total Grain", "Color": "Black"}])
totalPopulationChart = ChartModule([{"Label": "Total Population", "Color": "Black"},
                                    {"Label": "Projected Hisorical Poulation", "Color": "Red"}])
settlementsHouseholdsChart = ChartModule([{"Label": "Settlements", "Color": "Blue"},
                                          {"Label": "Households", "Color": "Red"}])
giniChart = ChartModule([{"Label": "Gini-Index", "Color": "Black"}])
minMaxMeanSetPopChart = ChartModule([{"Label": "Minimum Settlement Population", "Color": "Blue"}, 
                                     {"Label": "Maximum Settlement Population", "Color": "Red"}, 
                                     {"Label": "Mean Settlement Poulation", "Color": "Black"}])
minMaxMeanHPopChart = ChartModule([{"Label": "Minimum Household Population", "Color": "Blue"},
                                   {"Label": "Maximum Household Population", "Color": "Red"}, 
                                   {"Label": "Mean Household Poulation", "Color": "Black"}])
grainHoldingChart = ChartModule([{"Label": "< 33%", "Color": "Yellow"},
                                 {"Label": "33 - 66%", "Color": "Blue"},
                                 {"Label": "> 66%", "Color": "Purple"}])

elements = [grid, # Grid
            totalGrainChart, totalPopulationChart, settlementsHouseholdsChart, giniChart, minMaxMeanSetPopChart,
            minMaxMeanHPopChart, grainHoldingChart]

model_params = {"height": 30, 
                "width": 30,
                "infoText": UserSettableParameter('static_text', value = "After changing any of the starting settings for the simulation please click Reset in order for these changes to take effect."),
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

server = ModularServer(EgyptSim, elements, "Egypt Sim", model_params)

server.port = 8521