# these functions are used for creating coroutines that compare
# the output of postprocessing to a some desired value/property

from utils import _dec_coroutine


@_dec_coroutine
def boundary_cond(*range):
    """
    Check if a given input value is within a specified range.

    Parameters:
    - *range:
        A tuple of one or two elements specifying the lower and
        upper bounds of the range. If only one element is given,it is
        interpreted as the lower bound and the upper bound is set to None.
        If no elements are given, the range is set to (None, None).

    Yields:
    - bool:
        A boolean value indicating whether the input value is within
        the specified range.

    Raises:
    - ValueError: If the number of elements in the range tuple is not 1 or 2.
    - ValueError: If both lower and upper bounds are set to None.
    - TypeError: If the input value is not valid (int or float or None).

    """
    # print(range)
    if len(range) == 1:
        lower_bound, upper_bound = range[0], None
    elif len(range) == 2:
        lower_bound, upper_bound = range
    else:
        raise ValueError('Invalid range')
    if lower_bound is None and upper_bound is None:
        raise ValueError('Invalid range')
    output = None
    while True:
        input = (yield output)
        try:
            if lower_bound is None:
                output = input <= upper_bound
            elif upper_bound is None:
                output = input >= lower_bound
            else:
                output = lower_bound <= input <= upper_bound
        except TypeError:
            # doing this because of the decorator behaviour
            # when using 'yield from' to reference this generator func
            if input is None:
                pass
            else:
                print(f'range is: {range}')
                print(f'lbound: {lower_bound}, ubound:{upper_bound}')
                print(f'the input is: {input}')
                raise TypeError(
                    'conditionals.boundary_cond had unexpected type')


@_dec_coroutine
def range_cond(value, error):
    '''
    Check if a given input value is within
    a specified range around a given value.

    Parameters:
    - value (int or float):
        The center value of the range.
    - error (int or float):
        The maximum deviation from the center value allowed in the range.

    Yields:
    - bool:
        A boolean value indicating whether the input value
        is within the specified range.
    '''
    lower_bound = value - error
    upper_bound = value + error
    while True:
        yield from boundary_cond(lower_bound, upper_bound)


if __name__ == '__main__':
    test = boundary_cond(0, 5)
    print(test.send(6))
    print(test.send(-1))
    test1 = boundary_cond(5)
    print(test1.send(6))
    print(test1.send(4))
    print('_______')
    test2 = range_cond(5, 1)
    print(test2.send(7))
    print(test2.send(5.5))
