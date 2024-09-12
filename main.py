import cirq

q0, q1, q2 = cirq.LineQubit.range(3)
circuit = cirq.Circuit()
circuit.append([cirq.X(q0), cirq.X(q1)])
circuit.append(cirq.TOFFOLI(q0, q1, q2))
circuit.append(cirq.measure(q0, q1, q2))
print(circuit)

simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=10)
print(result)