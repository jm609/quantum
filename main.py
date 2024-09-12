import cirq

qubit = cirq.GridQubit(0, 0)
circuit = cirq.Circuit(
    cirq.X(qubit),
    cirq.measure(qubit, key='m')
)

print(circuit)

simulator = cirq.Simulator()
result = simulator.run(circuit, repetitions=10)
print(result)