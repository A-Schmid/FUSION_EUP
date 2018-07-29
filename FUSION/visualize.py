from bokeh.io import output_notebook, show, push_notebook
from bokeh.models import ColumnDataSource
from bokeh.plotting import Figure, show, curdoc
import time
import numpy as np

class Plot:
    
    def __init__(self, width = 800, height = 300, lines = 1, resolution = 100, update_rate = 1, title = ""):
        self.__line_colors = ["red", "blue", "green", "orange", "purple"]

        self.__num_lines = 0
        self.__max_lines = lines
        self.__line_counter = 0
        
        self.__counter = 0
        self.data = []

        self.update_rate = update_rate
        self.resolution = resolution

        output_notebook()
        self.__doc = curdoc()

        column_data_structure = dict(x = [])
        self.__source = ColumnDataSource(column_data_structure)

        self.__figure = Figure(plot_width = width, plot_height = height)
        self.__figure.title.text = title

        for i in range(0, self.__max_lines):
            self.__add_line()
        
        self.__handle = show(self.__figure, notebook_handle = True)

        

    def __add_line(self):
        self.__source.add([], "t00%d" % (self.__num_lines))
        temp = self.__figure.line(source = self.__source, x = 'x', y = 't00%d' % (self.__num_lines), alpha = 0.85, color = self.__line_colors[self.__num_lines % len(self.__line_colors)])
        self.data.append(0)
        self.__num_lines += 1

    def show(self, data):
        if(self.__line_counter >= self.__num_lines):
            raise Exception("tried to add too many lines!")
            return

        self.data[self.__line_counter] = data
        self.__line_counter += 1

    def update(self):
        new_data = dict(x = [self.__counter])
        for i in range(0, self.__num_lines):
            new_data["t00%d" % (i)] = np.array([self.data[i]])
        self.__source.stream(new_data, self.resolution)
        push_notebook(handle = self.__handle)
        self.__counter += 1
        self.__line_counter = 0
