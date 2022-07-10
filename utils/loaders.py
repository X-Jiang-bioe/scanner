import tellurium as te
import model
"""
Set of functions that take in the model desctiption and return a model obnject
"""


def antimony_load(string):
    return model.Model(te.antimonyToSBML(string))


def file_load(string):
    try:
        return model.Model(string)
    except:
        return(te.antimonyToSBML(string))


def save_load(string):
    return None
