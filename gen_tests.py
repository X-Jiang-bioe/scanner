def generator(input: list, output):
    # exit condition
    if len(input) == 0:
        yield dict(output.items())
    # recursive loop
    else:
        curr = input[0]
        par_name = curr[0]
        for par_value in curr[1]:
            output[par_name] = par_value
            yield from generator(input[1:], output=output)

def dec_coroutine(func):
    def new_func(item):
        x = func(item)
        x.send(None)
        return x
    return new_func

@dec_coroutine
def post_proc(func):
    '''
    postprocessing function coroutine wrapper
    '''
    output = None
    while input := (yield output):
        output = func(input)

def test_func(x):
    return x[0]**x[1]

testlist = [('a', (1, 2, 3)), ('b', (4, 5, 6)), ('c', (7, 8))]
a = {}
# gen = generator(testlist, a)
# print(list(gen))
# for a in gen:
#     print(a)