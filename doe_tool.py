class doe_tool():
    # TODO: visualization tools
    # TODO: handle models that are classes
    # TODO: turn scan into a generator function

    def __init__(self, model, par_names, initial_vals):
        self.model = model
        self.par_names = par_names
        self.initial_vals = initial_vals
        self.simspec = {}  # what is passed to model for simulation
        self._setup()
        return None

    def _setup(self):
        # TODO: make initial_vals optional
        for name, val in zip(self.par_names, self.initial_vals):
            self.simspec[name] = val
        # lists to fill after initialization, first element
        # is the initial conditions run
        # TODO: Need a better way to store scan results
        #   perhaps do a n-dim DF with pandas
        self.outputs = [self.model(self.simspec)]  # raw outputs of model
        # specifications for each model simulation
        self.simspecs = [self.simspec]
        return

    def get_outputs(self):
        return self.outputs

    def get_simspecs(self):
        # specs = list(self._nWay_generator(self.scan_parameters))
        # self.simspecs.append(specs)
        return self.simspecs

    def reset(self):
        # if self.reset_sim is not None:
        #     self.reset_sim()
        self.outputs = []
        self.simspecs = []
        self._setup()
        return

    def simulate(self):
        return self.model(self.simspec)

    def scan(self, scan_parameters):
        simspecs = self._nWay_generator(scan_parameters)
        for simspec in simspecs:
            # print(simspec)
            self.simspec = simspec
            self.simspecs.append(simspec)
            self.outputs.append(self.simulate())
        return None

    def _nWay_generator(self, input: list, output={}):
        '''
        Helper function; used to generate parameter-value pairs
        to submit to the model for the simulation.

        Parameters
        ----------
        input : list of tuple
            every tuple of the list must be of the form:
            ``('name_of_parameter', iterable_of_values)``

        output : list, optional
            parameter used for recursion; allows for iterable building
            across subgenerators

        Returns
        -------
        Generator :
            Specifications used for simulation setup of the form:
            ``[('par1', val1), ('par2', val2), ...]``
        '''
        # exit condition
        if len(input) == 0:
            yield dict(output.items())
        # recursive loop
        else:
            curr = input[0]
            par_name = curr[0]
            for par_value in curr[1]:
                output[par_name] = par_value
                # coroutines for the win!
                yield from self._nWay_generator(
                    input[1:], output=output)


if __name__ == "__main__":

    def testfun(dic):
        return dic['x'] ** dic['y']

    scanner = doe_tool(testfun, ('x', 'y'), (5, 5))
    print(scanner.get_outputs())

    scanner.scan((('x', [0, 1, 2, 3, 4]), ('y', range(2))))
    print('----------')
    print(scanner.get_outputs())
    print('----------')
    print(scanner.get_simspecs())
