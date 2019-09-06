import json
from mesa.visualization.modules import ChartModule

class TableChartModule(ChartModule):
    """Chart that obtains data from a table rather than a model var in the datacollector"""
    tableName = ""

    def __init__(self, series, tableName, 
                 canvas_height=200, canvas_width=500, data_collector_name="datacollector"):
        """
        Args:
            tableName: Name of the table to read from
            series: A list of dictionaries containing series names and
                    HTML colors to chart them in, e.g.
                    [{"Label": "happy", "Color": "Black"},]
            canvas_height, canvas_width: Size in pixels of the chart to draw.
            data_collector_name: Name of the DataCollector to use.
            """
        self.tableName = tableName

        super().__init__(series, #title, xlab, ylab, 
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