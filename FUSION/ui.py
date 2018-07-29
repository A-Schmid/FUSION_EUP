import ipywidgets as widgets
from IPython.display import display

def createSlider():
    w = widgets.IntSlider()
    display(w)

def createText():
    t = widgets.Text()
    display(t)

"""
from __future__ import print_function
from ipywidgets import interact, interactive, fixed, interact_manual
import ipywidgets as widgets

def createSlider(minimum = -10.0, maximum = 10.0):
    def f(slider_range):
        return (slider_range)
    interact(f, slider_range=(minimum, maximum))
"""
