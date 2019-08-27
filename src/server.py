from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule

from src.agents import River, Field, Settlement
from src.model import EgyptSim

max = 1.36  # The man, the myth, the legendary Rhett worked this out using really slow and manual machine learning


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
            # Inverse for the  RGB Scale
            inverseFertilityValue = max - fertilityValue
            # More fertile = Lower Value for R, More Green
            rValue = round(inverseFertilityValue * (255/max))
            hexValue = rgb_to_hex((rValue, 230, 0))
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
