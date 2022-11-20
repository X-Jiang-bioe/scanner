import string
import tellurium as te
# import utils


DEFAULT_SCAN_RANGE = (0.5, 2, 3)
DEFAULT_SIM_PARAMETERS = (0, 10, 100)
SCAN_TYPES = ['linear', 'logarithmic', 'exponential',
              'multiplicative', 'custom']


def default_target(data):
    '''
    Accepts the roadrunner.simulate output

    Retunrns the same thing
    '''
    return data


class Model(te.roadrunner.extended_roadrunner.ExtendedRoadRunner):
    """
    A class used to represent a model to run analysis on.
    Inherits from extened roadrunner:
    tellurium.roadrunner.extended_roadrunner.ExtendedRoadRunner


    Attributes
    ----------
    scanTarget(NamedArray)-> any : function
        Function used to defnine what is examined during the parameter scan.
        Takes in the output of .ExtendedRoadRunner.simulate() and returns
        the target.
        Initialized using self.setTarget

    output : list
        list of outputs of self.scan() function

    results : list
        list of raw simulation outputs

    scanRange : list
        List/lists used to define the range of a parameter scan.
        Initialized using self.setRange

    simParameters : tuple
        arguments to pass down to .ExtendedRoadRunner.simulate

    scanParameterIds : list of string
        list of parameter Ids used in the parameter scan.
        strings must mirror Ids from self.listParameters()


    Methods
    -------
    simulate(start, stop, points)
        inherited function
        runs time series simulation with (start, stop, #of points) as
        required parameters

    listParameters()
        returns possible parameters to input to setParameters

    getData()
        returns the information from Model.output in an array

    setParameters(params)
        selects up parameters for scanning

    setTarget(target)
        selects the scan target, accepts a function
        that manipulates NamedArray output of ExtendedRoadRunner.simulate()

    setRange(*rangeArgs, type = linear, uniform = True)
        creates the range/ranges for the parameters during the scan,
        accepts values to pass to the scanner or a list of values to pass
        directly to the scan

    scan(save = False)
        runs the parameter scan, executes a dry run(no saving) by default

    plotSimple('Parameter name')
        creates a simple plot of a given parameter time series
        assumes that target was a time series

    plotOver('Parameter name')
        creates a series of plots w.r.t. a given parameter
        assumes 2D scan and that target was a time series

    plotHeatMap('parameter1', 'parameter2')
        creates the elasticity heatmap
        assumes 2D and a single value target output
    """
    def __init__(self, rr_model):  # only takes in sbml format

        # setup BEFORE the scan
        super().__init__(rr_model)

        self.target = default_target
        self.scanRange = None
        self.scanParameterIds = None
        self.simParameters = DEFAULT_SIM_PARAMETERS
        self.uniform = True

        # parameters filled DURING scan
        self.output = []  # what was the return of the target function
        self.results = []  # output/initial simulation

        return None

    def listParameters(self):
        species = super().getFloatingSpeciesIds()
        constants = super().getGlobalParameterIds()
        return (species + constants)

    def listParametersConcentrations(self):
        return (super().getFloatingSpeciesConcentrationIds())

    def resetScanner(self):
        super().resetAll()
        self.scanParameterIds = None
        self.simParameters = DEFAULT_SIM_PARAMETERS
        self.target = default_target
        self.tracker = []
        self.output = []
        self.results = {}
        return

    def getData(self):
        return

    def setParameters(self, parameters):
        self.scanParameterIds = parameters

    def setTarget(self, target):
        if type(target) is string:
            self.target = (lambda data: data[target])
            #  returns the simulation result of a given target species
        else:
            self.target = target

    def setScanRange(self, *rangeArgs, type="linear", uniform=True):
        self.uniform = uniform
        if uniform:
            if type == "custom":
                # unpacks the list, probably unnecessary here
                # some sort of unpacking will be needed in
                # the non-uniform case
                self.scanRange = [item for item in rangeArgs[0]]
            else:
                self.scanRange = []
                # call to the functions from utils to get the lists for
                # multiplication
        else:
            # Non-uniform case handled here
            # might be useful to use i as a tracker for rangeArgs
            i = 0
            for typ in type:
                None

        return None

    def scan(self):
        # at least scan parameters must be predefined
        # if scan range was not, call set_scan_range with default
        # parameters after the scan parameter check
        self._recursive_nWay_generator()
        return None

    def _recursive_nWay_generator(self, input: list, output=[]):
        '''
        Helper function; used to generate parameter-value pairs
        to submit to the model for the simulation. Bases the values on
        the calculated ranges.

        Parameters
        ----------
        input : list of tuple
            every tuple of the list must be of the form:
            ``('name_of_parameter', iterable_of_values)``

        output : list, optional
            parameter used for recursion; allows for list building
            across subgenerators

        Returns
        -------
        Generator :
            Specifications used for simulation setup of the form:
            ``[('par1', val1), ('par2', val2), ...]``
        '''
        # exit condition
        if len(input) == 0:
            yield output
        # recursive loop
        else:
            curr = input[0]
            par_name = curr[0]
            for par_value in curr[1]:
                output_new = output + [(par_name, par_value)]
                # coroutines for the win!
                yield from self._recursive_nWay_generator(
                    input[1:], output=output_new)



    def plotSimple(self, targetID):
        return None
