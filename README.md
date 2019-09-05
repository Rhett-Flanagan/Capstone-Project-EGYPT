# Capstone-Project-EGYPT

## Rhett Flanagan, James Kriel, Tumi Moeng

## FLNRHE001, KRLJAM001, MNGTUM007

## Summary

A model representing the change of wealth over time in Ancient Egypt, where wealth is represented by the amount of grain a household has.
The model active agent in the model is a Household, which has a number of workers and can farm fields to gain grain with those workers. Several households dwell in a settlement, which has a location on a grid of land that can be farmed.

## Installation

The model requires Python 3 to be installed and will not function on Python 2

To install the dependencies use pip and the requirements.txt in this directory. e.g.

``` cmd
    pip install -r requirements.txt
```

or on Linux with Python 3 installed:

``` terminal
    pip3 install -r requirements.txt
```

## Running the Model

To run the model run the run.py file in the root directory. e.g.

``` cmd
    python run.py
```

or on Linux with Python 3 installed:

``` terminal
    python3 run.py
```

This will open the model server in the web browser through which the model can be run. Clicking start or step will cause the model to start. Clicking reset will reset the model with any changes in parameters that have been entered.

## Running the Jupyter Notebook

To run the Jupyter notebook ensure that the requiremnts are installed and call:

``` cmd
    jupyter-notebook "Farmers to Pharaohs Notebook.ipynb"
```
