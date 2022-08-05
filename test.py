import tellurium as te
from load import load
import utils
mod = """
model test
    compartment C1;
    C1 = 1.0;
    species S1, S2;

    S1 = 10.0;
    S2 = 0.0;
    S1 in C1; S2 in C1;
    J1: S1 -> S2; k1*S1;

    k1 = 1.0;
end
"""
# model = load(mod)

# # print(model.list_parameters())

# a = model.list_parameters()


def test(*args):
    l = len(args)
    lis = []
    for i in range(0, l-2, 3):
        lis.append(args[i: i+3])
    return lis

print(test(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12))
print(test(range(3)))