from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

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


grid = CanvasGrid(portrayal, 30, 30, 600, 600)
chart = ChartModule([{"Label": "Total Grain", "Color": "Black"}], data_collector_name="datacollector")

server = ModularServer(EgyptSim, [grid, chart], "Egypt Sim", {"height": 30, "width": 30})

server.port = 8521
# server.launch()
