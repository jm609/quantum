import random
import cirq

def main():
    qubit_count = 8
    circuit_sample_count = 10

    input_qubits = [cirq.GridQubit(i, 0) for i in range(qubit_count)]
    output_qubit = cirq.GridQubit(qubit_count, 0)

    secret_bias_bit = random.randint(0, 1)
    secret_factor_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    oracle = make_oracle(input_qubits, output_qubit, secret_factor_bits, secret_bias_bit)
    print('비밀 함수:\nf(x) = x*<{}>+ {} (mod2)'.format(','.join(str(e) for e in secret_factor_bits), secret_bias_bit))
    circuit = make_bernstein_vazirani_circuit(input_qubits, output_qubit, oracle)
    print('\n회로:')
    print(circuit)

    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=circuit_sample_count)
    frequencies = result.histogram(key='result', fold_func=bitstring)
    print('\n표본 실행 결과:\n{}'.format(frequencies))

    most_common_bitstring = frequencies.most_common(1)[0][0]
    print('\n가장 많이 나온 비트열과 비밀 인자의 일치 여부:\n{}'.format(most_common_bitstring == bitstring(secret_factor_bits)))

def make_oracle(input_qubits, output_qubit, secret_factor_bits, secret_bias_bit):
    if secret_bias_bit:
        yield cirq.X(output_qubit)
    for qubit, bit in zip(input_qubits, secret_factor_bits):
        if bit:
            yield cirq.CNOT(qubit, output_qubit)

def make_bernstein_vazirani_circuit(input_qubits, output_qubit, oracle):
    c = cirq.Circuit()
    c.append([cirq.X(output_qubit), cirq.H(output_qubit), cirq.H.on_each(*input_qubits)])
    c.append(oracle)
    c.append([cirq.H.on_each(*input_qubits), cirq.measure(*input_qubits, key='result')])
    return c

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

if __name__ == '__main__':
    main()
