import tellurium as te

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
# for element in r.keys():
#     print(element)

r = te.loada(mod)
# r = \
# te.roadrunner.extended_roadrunner.ExtendedRoadRunner(te.antimonyToSBML(mod))
# data = r.simulate(0,1,100)
# print(r.getFloatingSpeciesIds())
# print("_____")
# r.setGlobalParameterByName()
# print(r.getFloatingSpeciesConcentrationIds())

# print(r.simulate(0,1,100)["[S1]"])
r.setValues(['S1', 'S2'], [5., 5.])
print(r.getFloatingSpeciesAmountsNamedArray()[0])