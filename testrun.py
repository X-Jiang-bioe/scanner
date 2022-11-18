import tellurium as te
import scanner

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
sbml = te.antimonyToSBML(mod)
a = te.loada(mod)

b = a.getGlobalParameterIds()
print(b)

c = scanner.load(mod)
d = c.listParameters()
print(d)