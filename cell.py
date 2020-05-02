from brian2 import *
import matplotlib.pyplot as plt

tau = 10*ms
u_rest = 0.1*mV
u_reset = 0.1*mV
t_refrac = 5*ms

taupre = taupost = 20*ms
wmax = 14
Apre = 10
Apost = -Apre*taupre/taupost*1.05

eqs = '''
    du/dt = ( -(u-u_rest) + i_syn / nS ) / tau : volt
    i_syn = g * nS * u                         : amp
    dg/dt = -g / (1.0*ms)                      : 1
'''

rst = '''
    u = u_reset
'''

#P = SpikeGeneratorGroup(5, array([0,1,2,3,4,5,6,7,8,9,10,11,12,13]), array([1,2,3,4,5, 5.5,6,6.5,7,7.5,8,8.5,9,9.5])*ms, period=10*ms)
P = SpikeGeneratorGroup(1, array([0]), array([1])*ms, period=6*ms)
SM = SpikeMonitor(P)
# MP = StateMonitor(P, 'v', record=True)
G = NeuronGroup(1, eqs, threshold='u>20*mV', reset=rst, refractory=t_refrac)
M = StateMonitor(G, ['u', 'i_syn', 'g'], record=True)
S = Synapses(P, G, 
'''
    w : 1
    dapre/dt = -apre/taupre : 1 (event-driven)
    dapost/dt = -apost/taupost : 1 (event-driven)
''',
on_pre='''
    g_post += w
    apre += Apre
    w = clip(w+apost, 0, wmax)
    ''',
on_post='''
    apost += Apost
    w = clip(w+apre, 0, wmax)
''')
S.connect()
S.w = 10

MS = StateMonitor(S, ['w'], record=True)

G[0].u = u_rest

run(100*ms)

fig, plot1 = plt.subplots()
plot1.plot(M.t/ms, M.u[0]/mV, 'ro', label='U')
plot1.set_xlabel('Time (ms)')
plot2 = plot1.twinx()
plot2.plot(M.t/ms, M.i_syn[0]/mA, 'b', label='I')
plt3 = plot1.twinx()
plt3.plot(M.t/ms, M.g[0], 'g', label='g')
plt4 = plot1.twinx()
plt4.plot(MS.t/ms, MS.w[0], 'y')
spikes = SM.spike_trains()[0]
for s in spikes:
    axvline(s/ms, ls='--', c='k')
fig.tight_layout()
plt.show()
