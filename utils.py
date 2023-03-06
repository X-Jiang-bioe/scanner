def _dec_coroutine(func):
    """
    decorator for coroutines, sends the required None
    as an initializer
    """
    def new_func(*args, **kwargs):
        x = func(*args, **kwargs)
        x.send(None)
        return x
    return new_func


def invalid_generator(x):
    raise Exception("Invalid generator name")


@_dec_coroutine
def rr_coroutine(model, start, end, numpts):
    """
    Takes in the standard roadrunner model and adds
    the parameter replacement functionality
    """
    output = None

    while True:
        input = (yield output)
        model.resetAll()
        for key in input:
            model[key] = input[key]
        output = model.simulate(start, end, numpts)


class StopCoroutine(Exception):
    pass
