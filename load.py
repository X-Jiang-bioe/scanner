import utils
import re


PROG = re.compile("(\/+.*)+")


def load(string, fromSave=False):
    """
    Used for loading in mondels/older simulations.
    Returns an instance of a model object

    Attributes
    ----------
    string : str
        A path to the supported file or
        an antimony string

    fromSave = False : bool
        Used to specify whether or not loader should expect
        a COMBINE archive that was saved using this library

    Returns
    -------
    Model : class
        Primary class to interact witht the library
        inherits from:
        tellurium.roadrunner.extended_roadrunner.ExtendedRoadRunner
    """

    if PROG.match(string):  # if is a path to file
        return utils.file_load(string)
    elif fromSave:
        return utils.save_load(string)
    else:  # otherwise assumes antimony string
        return utils.antimony_load(string)