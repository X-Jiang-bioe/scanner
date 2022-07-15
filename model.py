import string
import tellurium as te
# import utils


DEFAULT_SCAN_RANGE = [i for i in range(11)]
DEFAULT_SIM_PARAMETERS = (0, 10, 100)
SCAN_TYPES = ['linear', 'logarithmic', 'exponential',
              'multiplicative', 'custom']


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
        Function used to defnine what is examined during the parameter scan.
        Takes in the output of .ExtendedRoadRunner.simulate() and returns
        the target.
        Initialized using self.set_target

    results : list
        list of outputs of self.scan_target function

    tracker : list
        list of parameters that were passed to the model for simulation

    scan_range()-> list : function
        Function used to define the range of a parameter scan.
        Takes in the self.results
        Initialized using self.set_range

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

    set_range(scanRange, isUniform = True)
        selects the range/ranges for the parameters during the scan,
        accepts a list of values to pass to the scanner or a function that
        returns uses the output of target function to return the next step for
        a given parameter
        for isUniform = False, list of lists order must correspond to the order
        of self.scan_parameterIds

    scan(save = False)
        runs the parameter scan, executes a dry run(no saving) by default

    _display_state()
        internal function; handles the terminal display updates during a
        parameter scan
    -------
    """
    def __init__(self, rr_model):  # only takes in sbml format

        # setup BEFORE the scan
        super().__init__(rr_model)
        # self.parameterIds = self.getFloatingSpeciesIds()
        # self._parameterConcentrationIds = \
        #     self.getFloatingSpeciesConcentrationIds()
        self.scan_target = default_target
        self.scan_range = DEFAULT_SCAN_RANGE
        self.scan_parameterIds = None
        self.sim_parameters = DEFAULT_SIM_PARAMETERS

        # parameters filled DURING scan
        self.tracker = []  # what values were passed to model
        self.results = []  # what was the return of the target function

        return None

    def list_parameters(self):
        return (super().getFloatingSpeciesIds())

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
            #  return the simulation results of a given target species
        else:
            self.target = target

    def set_scan_range(self, *range_args, type="linear", dependent=False):
        # if type(range) is list:
        #     self.scan_range = (lambda x: range[len(self.results)])
        #     #  return the value based on # of completed loops
        # else:
        #     self.scan_range = range
        return None

    # def linear_step():
    #     step = 0
    #     return step
    def save(self, path):
        return

    # def _runExperiment(self, params):
    #     return

    # def
