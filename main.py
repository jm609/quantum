import cirq

qreg = [cirq.LineQubit(x) for x in range(2)]
circ = cirq.Circuit()
circ.append([cirq.H(qreg[0]), cirq.CNOT(qreg[0], qreg[1])])
print(circ)
circ.append(cirq.measure(*qreg, key='z'))
sim = cirq.Simulator()
res = sim.run(circ, repetitions=100)
print(res.histogram(key='z'))