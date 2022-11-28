def _recursive_nWay_generator(input: list, output):
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
        yield dict(output.items())
    # recursive loop
    else:
        curr = input[0]
        par_name = curr[0]
        for par_value in curr[1]:
            output[par_name] = par_value
            # coroutines for the win!
            yield from _recursive_nWay_generator(input[1:], output=output)


testlist = [('a', (1, 2, 3)), ('b', (4, 5, 6)), ('c', (7, 8))]
a = {}
gen = _recursive_nWay_generator(testlist, a)
print(list(gen))
# for a in gen:
#     print(a)