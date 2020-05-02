from brian2 import *
import matplotlib.pyplot as plt

tau = 10*ms
u_rest = 0.1*mV
u_reset = 0.1*mV
t_refrac = 5*ms

eqs = '''
    du/dt = ( -(u-u_rest) + i_syn / nS ) / tau : volt
    i_syn = g * nS * u                         : amp
    dg/dt = -g / (1.0*ms)                      : 1
'''

rst = '''
    u = u_reset
'''

P = PoissonGroup(1, 500*Hz)
G = NeuronGroup(1, eqs, threshold='u>20*mV', reset=rst, refractory=t_refrac)
M1 = SpikeMonitor(P)
M = StateMonitor(G, ['u', 'i_syn', 'g'], record=True)
S = Synapses(P, G, on_pre='g += 10')
S.connect(j='i')
G[0].u = u_rest

run(100*ms)

fig, plot1 = plt.subplots()
plot1.plot(M.t/ms, M.u[0]/mV, 'ro', label='U')
plot1.set_xlabel('Time (ms)')
plot2 = plot1.twinx()
plot2.plot(M.t/ms, M.i_syn[0]/mA, 'b', label='I')
plt3 = plot1.twinx()
plt3.plot(M.t/ms, M.g[0], 'g', label='g')
fig.tight_layout()
plt.plot(M1.t/ms, M1.i, '.')
plt.show()
