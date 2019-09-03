import json
from mesa.visualization.ModularVisualization import VisualizationElement
from mesa.visualization.modules import ChartModule

class TitledChartModule(VisualizationElement):

    package_includes = ["Chart.min.js"]
    local_includes = ["TitledChartModule.js"]

    title = ""
    xlab = ""
    ylab = ""

    def __init__(self, series, title = "Title", xlab = "x-axis", ylab = "y-axis", 
                 canvas_height=200, canvas_width=500, data_collector_name="datacollector"):
        """
        Create a new line chart visualization.

        Args:
            title: The title of the chart
            xlab: The label for the x-axis
            ylab: The label for the y-axis
            series: A list of dictionaries containing series names and
                    HTML colors to chart them in, e.g.
                    [{"Label": "happy", "Color": "Black"},]
            canvas_height, canvas_width: Size in pixels of the chart to draw.
            data_collector_name: Name of the DataCollector to use.
        """
        
        self.series = series
        self.canvas_height = canvas_height
        self.canvas_width = canvas_width
        self.data_collector_name = data_collector_name

        series_json = json.dumps(self.series)
        new_element = "new TitledChartModule({}, {}, {}, {}, {},  {})"
        new_element = new_element.format(title, xlab, ylab, series_json,
                                         canvas_width, canvas_height)
        self.js_code = "elements.push(" + new_element + ");"

    def render(self, model):
        current_values = []
        data_collector = getattr(model, self.data_collector_name)

        for s in self.series:
            name = s["Label"]
            try:
                val = data_collector.model_vars[name][-1]  # Latest value
            except (IndexError, KeyError):
                val = 0
            current_values.append(val)
        return current_values

class TableChartModule(TitledChartModule):
    """Chart that obtains data from a table rather than a model var in the datacollector"""
    tableName = ""

    def __init__(self, series, tableName, title = "Title", xlab = "x-axis", ylab = "y-axis", 
                 canvas_height=200, canvas_width=500, data_collector_name="datacollector"):
        """
        Args:
            tableName: Name of the table to read from
            title: The title of the chart
            xlab: The label for the x-axis
            ylab: The label for the y-axis
            series: A list of dictionaries containing series names and
                    HTML colors to chart them in, e.g.
                    [{"Label": "happy", "Color": "Black"},]
            canvas_height, canvas_width: Size in pixels of the chart to draw.
            data_collector_name: Name of the DataCollector to use.
            """
        self.tableName = tableName

        super().__init__(series, title, xlab, ylab, 
                         canvas_height, canvas_width,
                         data_collector_name)

    def render(self, model):
            current_values = []
            data_collector = getattr(model, self.data_collector_name)

            for s in self.series:
                col = s["Label"]
                try:
                    val = data_collector.tables[self.tableName][col][-1]  # Latest value
                except (IndexError, KeyError):
                    val = 0
                current_values.append(val)
            return current_values