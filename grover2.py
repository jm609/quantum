from qiskit import QuantumCircuit
from qiskit_aer import Aer
from qiskit.circuit.library import MCXGate
import random

def set_io_qubits(qubit_count):
    input_qubits = list(range(qubit_count))
    output_qubit = qubit_count
    return input_qubits, output_qubit

def make_oracle(circuit, input_qubits, output_qubit, x_bits):
    for qubit, bit in zip(input_qubits, x_bits):
        if not bit:
            circuit.x(qubit)
    circuit.mcx(input_qubits, output_qubit)
    for qubit, bit in zip(input_qubits, x_bits):
        if not bit:
            circuit.x(qubit)

def make_grover_circuit(input_qubits, output_qubit, oracle, x_bits):
    qubit_count = len(input_qubits)
    circuit = QuantumCircuit(qubit_count + 1, qubit_count)

    # Initial state preparation
    circuit.x(output_qubit)
    circuit.h(output_qubit)
    circuit.h(input_qubits)

    # Oracle
    oracle(circuit, input_qubits, output_qubit, x_bits)

    # Grover diffusion operator
    circuit.h(input_qubits)
    circuit.x(input_qubits)
    circuit.h(input_qubits[-1])
    circuit.mcx(input_qubits[:-1], input_qubits[-1])
    circuit.h(input_qubits[-1])
    circuit.x(input_qubits)
    circuit.h(input_qubits)

    # Measurement
    circuit.measure(input_qubits, range(qubit_count))
    return circuit

def bitstring(bits):
    return ''.join(str(bit) for bit in bits)

def main():
    qubit_count = 2
    circuit_sample_count = 100

    input_qubits, output_qubit = set_io_qubits(qubit_count)
    x_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    print('Secret bitstring:', bitstring(x_bits))

    circuit = make_grover_circuit(input_qubits, output_qubit, make_oracle, x_bits)
    print('회로:')
    print(circuit.draw())

    simulator = Aer.get_backend('qasm_simulator')
    # Execute the circuit
    result = simulator.run(circuit, shots=circuit_sample_count).result()
    counts = result.get_counts()

    print('표본 실행 결과:\n', counts)

    # Reverse the bit order for comparison
    most_common_bitstring = max(counts, key=counts.get)[::-1]
    print('최대 빈도 비트 문자열:', most_common_bitstring)
    print('비밀 비트 문자열과 일치:', most_common_bitstring == bitstring(x_bits))

if __name__ == '__main__':
    main()