import string
import tellurium as te
import utils


DEFAULT_SCAN_RANGE = [i for i in range(10)]
DEFAULT_SIM_PARAMETERS = (0, 10, 100)


def default_target(data):
    return data


class Model(te.roadrunner.extended_roadrunner.ExtendedRoadRunner):
    """
    A class used to represent a model to run analysis on.
    Inherits from extened roadrunner:
    tellurium.roadrunner.extended_roadrunner.ExtendedRoadRunner


    Attributes
    ----------
    scan_target(NamedArray)-> any : function
        Function used to defnine what is examined during the parameter scan
        takes in the output of .ExtendedRoadRunner.simulate() and returns
        the target

    sim_parameters : tuple
        arguments to pass down to .ExtendedRoadRunner.simulate

    scan_parameterIds : list of string
        list of parameter Ids used in the parameter scan.
        strings must mirror Ids from self.list_parameters()


    Methods
    -------
    simulate(start, stop, points)
        inherited function
        runs time series simulation with (start, stop, #of points) as
        required parameters

    set_parameters(params)
        selects up parameters for scanning

    set_target(target)
        selects the scan target, accepts a function
        that manipulates NamedArray output of ExtendedRoadRunner.simulate()

    set_range(discrete = False, *args, **kwargs)
        sets up the range across witch to run simulations with a given
        set of parameters accepts lists or a function to return a timepoint

    scan(save = False)
        runs the parameter scan, executes a dry run(no saving) by default

    _display_state()
        internal function that prints out information about the object after
        an action
    -------
    """
    def __init__(self, rr_model):  # only takes in sbml format

        # setup BEFORE the scan
        super().__init__(self, rr_model)
        # self.parameterIds = self.getFloatingSpeciesIds()
        # self._parameterConcentrationIds = \
        #     self.getFloatingSpeciesConcentrationIds()
        self.scan_target = default_target
        self.scan_step = default_step
        self.scan_parameterIds = None
        self.sim_parameters = DEFAULT_SIM_PARAMETERS

        # parameters filled DURING scan
        self.tracker = []  # what values were passed to model
        self.results = []  # what was the return of the target function

        return None

    def list_parameters(self):
        return (print(self.getFloatingSpeciesIds()))

    def scan(self, *simulate_parameters):
        return

    def reset_scanner(self):
        self.resetAll()
        self.scan_parameterIds = None
        self.sim_parameters = DEFAULT_SIM_PARAMETERS
        self.target = default_target
        self.tracker = []
        self.results = []
        return

    def set_parameters(self, parameters):
        self.scan_parameterIds = parameters

    def set_target(self, target):
        if type(target) is string:
            self.target = (lambda data:  data[target])
        else:
            self.target = target

    # def linear_step():
    #     step = 0
    #     return step
    def save(self, path):
        return

    def _runExperiment(self, params):
        return

    def