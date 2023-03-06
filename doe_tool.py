from utils import _dec_coroutine, invalid_generator, rr_coroutine
import conditionals
import simspec_generators
import tellurium as te


class doe_tool():
    # TODO: reset functionality
    # TODO: visualization tools

    def __init__(self, model, sim_time=(0, 50, 100)):
        self.model = model
        self.sim_time = sim_time
        self.coroutine_model = self.load_model(model)
        self.post_processor = lambda x: x  # hacky way of 'optionality'
        self.conditional = None
        self.simspecs = []
        self.sims = []
        self.results = []
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
        # TODO: better way of changing time of simulations
        # TODO: graphing capabilities
        if callable(model):
            return self._func_wrapper(model)
        else:
            # assume any given string is antimony or sbml file
            try:
                r = te.loadSBMLModel(model)
            except:
                r = te.loada(model)
            # !!! The simulation range specification is here
            # Bad spot, can't think of a better one
            return rr_coroutine(r, *self.sim_time)

    def change_model(self, model=None, sim_time=None):
        if sim_time is not None:
            self.sim_time = sim_time
        if model is not None:
            self.model = model
        self.coroutine_model = self.load_model(model)
        return None

    def simulate(self, simspec):
        return self.coroutine_model.send(simspec)

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
            raise ValueError('Invalid conditional type')

    def set_conditional(self, type, *args, **kwargs):
        self.conditional = self._conditional(type, *args, **kwargs)
        return None

    def send_conditional(self, value):
        return self.conditional.send(value)

    def optimize_demo(self, scan_type, scan_parameters):
        """
        Version of optimize that probably only works with
        grid simspec generator
        used in the demo

        Returns the set of parameters for a simulation that
        satisfy specified condition
        """
        generator = simspec_generators.generator_list.get(
            scan_type, invalid_generator)
        simspecs = generator(scan_parameters)
        cond = None
        state = False
        while not state:
            try:
                simspec = simspecs.send(cond)
                state, cond = self.send_conditional(
                    self.send_post_processor(
                        self.simulate(simspec)
                    )
                )
            except StopIteration:
                print('No specification that satisfies condition found')
                return None
        return simspec

    def scan(self, scan_type, scan_parameters):
        generator = simspec_generators.generator_list.get(
            scan_type, invalid_generator)
        simspecs = generator(scan_parameters)
        cond = None
        while True:
            try:
                self.simspecs.append(simspecs.send(cond))
                self.sims.append(self.simulate(self.simspecs[-1]))
                self.results.append(self.send_post_processor(self.sims[-1]))
                state, cond = self.send_conditional(self.results[-1])
                # TODO: anything except grid needs some stopping point
                # future extention to handle more complex generators put here
                # if state:
                #     raise(StopIteration)
                continue
            except StopIteration:
                break

        return None

    def get_scan(self):
        return self.simspecs, self.sims, self.results


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
    scanner.scan('grid', scan_parameters)
    specs, sims, res = scanner.get_scan()

    for i in (specs, sims, res):
        print(f'{i}')
        print('_________')
