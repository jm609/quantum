import cirq
q0, q1, q2 = cirq.LineQubit.range(3)
constant = ([], [cirq.X(q2)])
balanced = ([cirq.CNOT(q0, q2)],
            [cirq.CNOT(q1, q2)],
            [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2)],
            [cirq.CNOT(q0, q2), cirq.X(q2)],
            [cirq.CNOT(q1, q2), cirq.X(q2)],
            [cirq.CNOT(q0, q2), cirq.CNOT(q1, q2), cirq.X(q2)])


def your_circuit(oracle):
    yield cirq.X(q2), cirq.H(q2)
    yield cirq.H(q0), cirq.H(q1)
    yield oracle
    yield cirq.H(q0), cirq.H(q1), cirq.H(q2)
    yield cirq.X(q0), cirq.X(q1), cirq.CCX(q0, q1, q2)
    yield cirq.measure(q2)


simulator = cirq.Simulator()

print('상수 함수에 대한 결과')
for oracle in constant:
    result = simulator.run(cirq.Circuit(your_circuit(oracle)),
                           repetitions=10)
    print(result)

print('균형 함수에 대한 결과')
for oracle in balanced:
    result = simulator.run(cirq.Circuit(your_circuit(oracle)),
                           repetitions=10)
    print(result)
