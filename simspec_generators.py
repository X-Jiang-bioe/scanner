# These functions are used to generate the simulation specifications
# for the scanner to use during the search

def grid_search(input: list, output={}):
    '''
    Used to generate parameter-value pairs
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
            yield from grid_search(
                input[1:], output=output)


def random_search(paramters):
    None


generator_list = {
    'grid': grid_search,
    'random': random_search
}