from utils import _dec_coroutine
import conditionals


class doe_tool():
    # TODO: scanning algo
    # TODO: reset functionality
    # TODO: visualization tools
    # TODO: handle models that are classes?

    def __init__(self, model, par_names, initial_vals):
        self.model = self.load_model(model)
        self.par_names = par_names
        self.initial_vals = initial_vals
        self.post_processor = lambda x: x  # hacky way of 'optionality'
        self.conditional = None
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
        # TODO: sbml model handling
        if callable(model):
            return self._func_wrapper(model)

    def simulate(self, simspec):
        return self.model.send(simspec)

    # TODO: postprocessing only makes sense with sbml models,
    # consider an ACTUAL optional skip
    def load_post_processor(self, func):
        self.post_processor = self._func_wrapper(func)
        return None

    def send_post_processor(self, data):
        try:
            return self.post_processor.send(data)
        # part of the hacky optional skip
        except AttributeError:
            return self.post_processor(data)

    @_dec_coroutine
    def _conditional(self, type, *args, **kwargs):
        # TODO: write out the docstring explaining what
        # variables to pass down in what case
        # TODO: consider custom function handling
        if type == 'boundary':
            yield from conditionals.boundary_cond(*args, **kwargs)
        elif type == 'error_range':
            yield from conditionals.range_cond(*args, **kwargs)
        else:
            raise ValueError('Invalid value for type')

    def set_conditional(self, type, *args, **kwargs):
        self.conditional = self._conditional(type, *args, **kwargs)
        return None

    def send_conditional(self, value):
        return self.conditional.send(value)

    def scan_demo(self, scan_parameters):
        """
        This func is used in the demo for demonstration purposes
        """
        simspecs = self.simspec_generator_grid(scan_parameters)
        for simspec in simspecs:
            a = self.send_post_processor(self.simulate(simspec))
            if self.send_conditional(a):
                self.simspec = simspec
                return simspec
            else:
                continue
        return 'none found'

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
    scanner.set_conditional('boundary', 0, 5)
    print(scanner.send_conditional(6))
    scanner.set_conditional('error_range', value=10, error=1)
    print(scanner.send_conditional(10))
    scan_parameters = (('x', [0, 1, 2, 3, 4]), ('y', range(5)))
    print(scanner.scan_demo(scan_parameters))
