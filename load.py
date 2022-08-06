import utils
import re
import model


PROG = re.compile("(\/+.*)+")


def load(mod, fromSave=False):
    """
    Used for loading in mondels/older simulations.
    Returns an instance of a mod object

    Attributes
    ----------
    mod : str
        A path to the supported file or
        an antimony mod

    fromSave = False : bool
        Used to specify whether or not loader should expect
        a COMBINE archive that was saved using this library

    Returns
    -------
    mod : class
        Primary class to interact witht the library
        inherits from:
        tellurium.roadrunner.extended_roadrunner.ExtendedRoadRunner
    """
    if type(mod) is not str:
        try:
            return model.Model(mod)
        except:
            err = """
            Something went wrong during loading,\n
            please make sure you are using an approapriate
            RoadRunner instance
            """
            print(err)
    # if is a string, then check against a reg ex
    if PROG.match(mod):  # if is a path to file
        return utils.file_load(mod)
    elif fromSave:
        return utils.save_load(mod)
    else:  # otherwise assumes antimony string
        return utils.antimony_load(mod)