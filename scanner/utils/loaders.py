import tellurium as te
from scanner.model import Model
"""
Set of functions that take in the model desctiption and return a model obnject
"""


def antimony_load(string):
    return Model(te.antimonyToSBML(string))


def file_load(string):
    try:
        return Model(string)
    except:
        return(te.antimonyToSBML(string))


def save_load(string):
    return None
