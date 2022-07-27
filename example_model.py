import tellurium as te
import matplotlib.pyplot as plt

from utils.scan import doe_tool

"""
this code was used to generate the plots seen in the API documemntation
"""
mod1 = """
model feedback
    compartment C1;
    C1 = 1.0;
    species X
    const X0

    J1: X0 -> X; B + k1*X^4/(k2+X^4);
    J2: X -> ; k3*X;

    k1 = .9
    k2 = .3
    k3 = .7
    B = 0.1
    X = 1

end
"""

# --------------Plot for basic example----------------
model = te.loada(mod1)
data = model.simulate(0,100,100)

# print(model.getFloatingSpeciesIds() + model.getGlobalParameterIds())
# model['X'] = 5
# print(model.getFloatingSpeciesAmountsNamedArray())
dats = []
for i in range(0, 15, 1):
    model.reset()
    model['X'] = i*.1
    data = model.simulate(0,20,100)
    dats.append(data)

# print(dats)

fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for data in dats:
    ax.plot(data['time'], data['[X]'])
plt.savefig('example1.png')

# --------------Plot for something else----------------

