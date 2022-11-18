class doe_tool():
    """
    Collection of functions that facilitate doe study of a model.
    Levels are treated as percent deviations from the initial value

    Input
    -----
    model: function
        must be a function that takes in a list of factors that affect
        the model and returns data of chosen form based on those factors
    factor_names: list of str
        names of factors that will be studied
    initial_values: list of float
        initial values of factors, should be the same as in factor_names
    """
    def __init__(self, model, factor_names, initial_values):

        self.model, self.factor_names, self.initial_values = \
            model, factor_names, initial_values

        self.tracker = []  # what values were passed to model
        self.results = []  # what was the return of the model

    def getTracker(self):
        return self.tracker

    def getResults(self):
        return self.results

    def getDeviations(self):
        dev = []
        temp = []
        for tracked in self.tracker:
            for i, parameter in enumerate(tracked):
                temp.append(round(
                    (parameter/self.initial_values[i]-1)*100, ndigits=1))
            dev.append(temp)
            temp = []
        return dev
    # def getFactorlevels(self, tracker = None):
    #   return

    def reset(self):
        self.tracker = []
        self.results = []

    def simulate(self, factors):
        return self.model(factors)

    def runExperiment(self, deviation, initial_values):
        """
        get the result of a percent deviation of one factor

        Params
        ------
        deviation: list of tuples
            ('factor to vary', percent deviation)
        """
        new_vals = initial_values.copy()
        which = self.factor_names.index(deviation[0])
        new_vals[which] = new_vals[which]*(1+.01*deviation[1])
        self.tracker.append(new_vals)
        self.results.append(self.simulate(new_vals))

    def runOneFactor(self, name, levels, initial_values):
        for level in levels:
            self.runExperiment((name, level), initial_values)

    def runOneFactorStudy(self, deviations, initial_values=None):
        """

        Params
        ------
        deviations = dict
        {'factor to vary': [percent deviations]}


        """
        if initial_values is None:
            initial_values = self.initial_values
        if len(deviations) == 0:
            raise Exception('the deviations dictionary is empty')
        if type(deviations) != dict:
            raise Exception('deviations must be a dictionary')
        keys = list(deviations.keys())
        for key in keys:
            self.runOneFactor(key, deviations[key], initial_values)

    def runOneWDWithLevels(self, levels):
        dic = {}
        for key in self.factor_names:
            dic[key] = levels
        self.runOneFactorStudy(dic)

    def runNWDStudy(self, deviations):
        if len(deviations) == 0:
            raise Exception('the deviations dictionary is empty')
        if len(deviations) == 1:
            self.runOneFactorStudy(deviations)
        else:
            self._runNWDStudy(self.initial_values, deviations)

    def _runNWDStudy(self, current_parameter_values, deviations):
        keys = list(deviations.keys())
        if len(deviations) > 1:  # starts recursive loop for each factor
            current_levels = deviations.pop(keys[0])
            which = self.factor_names.index(keys[0])
            for level in current_levels:
                new_vals = current_parameter_values.copy()
                new_vals[which] = new_vals[which]*(1+.01*level)
                self._runNWDStudy(new_vals, deviations)

        else:  # exit condition
            self.runOneFactorStudy(
                deviations, initial_values=current_parameter_values)
            return


def _linear_range(start, end, points):
    """
    Returns a list of equally spaced values of length
    'points' between 'start' and end' in a x=y linear fashion

    Parameters
    ----------
    start: float
        The first value of the range

    end: float
        Last value of the range

    points: int
        The total number of points (at least 2)

    Returns
    -------
    range_values: list of float
        The values to be passed to the scanner
    """
    return None


def _exp_range(start, end, points):
    """
    Returns a list of equally spaced values of length
    'points' between 'start' and end' in a x=e^y exponential fashion

    Parameters
    ----------
    start: float
        The first value of the range

    end: float
        Last value of the range

    points: int
        The total number of points (at least 2)

    Returns
    -------
    range_values: list of float
        The values to be passed to the scanner
    """
    return None


def _log_range(start, end, points):
    """
    Returns a list of equally spaced values of length
    'points' between 'start' and end' in a x=log(y) logarithmic fashion

    Parameters
    ----------
    start: float
        The first value of the range

    end: float
        Last value of the range

    points: int
        The total number of points (at least 2)

    Returns
    -------
    range_values: list of float
        The values to be passed to the scanner
    """
    return None
