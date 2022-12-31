def _dec_coroutine(func):
    """
    decorator for coroutines
    """
    def new_func(*args, **kwargs):
        x = func(*args, **kwargs)
        x.send(None)
        return x
    return new_func
