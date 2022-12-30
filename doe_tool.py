def _dec_coroutine(func):
    """
    decorator for coroutines
    """
    def new_func(self, item):
        x = func(self, item)
        x.send(None)
        return x
    return new_func


class doe_tool():
    # TODO: visualization tools
    # TODO: handle models that are classes
    # TODO: turn scan into a generator function

    def __init__(self, model, par_names, initial_vals):
        self.model = self.load_model(model)
        self.par_names = par_names
        self.initial_vals = initial_vals
        # self._setup()
        return None

    @_dec_coroutine
    def _func_wrapper(self, func):
        '''
        function coroutine wrapper
        '''
        output = None
        while True:
            input = (yield output)
            output = func(input)

    def load_model(self, model):
        # TODO sbml model handling
        if callable(model):
            return self._func_wrapper(model)

    def simulate(self, simspec):
        return self.model.send(simspec)

    # TODO: postprocessing only makes sense with sbml models,
    # consider optional skip
    def load_post_processor(self, func):
        self.post_processor = self._func_wrapper(func)
        return

    def send_post_processor(self, data):
        return self.post_processor.send(data)

    # def scan(self, scan_parameters):
    #     simspecs = self._grid(scan_parameters)
    #     for simspec in simspecs:
    #         # print(simspec)
    #         self.simspec = simspec
    #         self.simspecs.append(simspec)
    #         self.outputs.append(self.simulate())
    #     return None

    def simspec_generator_grid(self, input: list, output={}):
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
                yield from self.simspec_generator_grid(
                    input[1:], output=output)

    # @_dec_coroutine
    # def simspec_generator_random(self, ranges):
    #     while True:
    #         input = (yield)


if __name__ == "__main__":

    def testfun(dic):
        return dic['x'] ** dic['y']

    scanner = doe_tool(testfun, ('x', 'y'), (5, 5))

    # a = scanner.model.send(('x', [0, 1, 2, 3, 4]), ('y', range(2)))
    a = scanner.simulate({'x': 2, 'y': 2})
    print(a)
    # print(scanner.get_outputs())

    # scanner.scan((('x', [0, 1, 2, 3, 4]), ('y', range(2))))
    # print('----------')
    # print(scanner.get_outputs())
    # print('----------')
    # print(scanner.get_simspecs())
