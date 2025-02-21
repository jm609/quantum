import numpy as np
import cirq

def main():

    qft_circuit = generate_qft_circuit()
    print(qft_circuit)
    simulator = cirq.Simulator()
    result = simulator.simulate(qft_circuit)
    print(np.around(result.final_state, 3))

def cz_and_swap(q0, q1, rot):
    yield cirq.CZ(q0, q1)**rot
    yield cirq.SWAP(q0, q1)

def generate_qft_circuit():
    a, b, c, d = [cirq.GridQubit(0, i) for i in range(4)]
    circuit = cirq.Circuit()

    circuit.append(cirq.H(a))
    circuit.append(cz_and_swap(a, b, 0.5))
    circuit.append(cz_and_swap(a, c, 0.25))
    circuit.append(cz_and_swap(a, d, 0.125))
    circuit.append(cirq.H(b))
    circuit.append(cz_and_swap(b, c, 0.5))
    circuit.append(cz_and_swap(b, d, 0.25))
    circuit.append(cirq.H(c))
    circuit.append(cz_and_swap(c, d, 0.5))
    circuit.append(cirq.H(d))

    # Optional: Add SWAP gates at the end to rearrange qubits
    circuit.append(cirq.SWAP(a, d))
    circuit.append(cirq.SWAP(b, c))

    return circuit

if __name__ == "__main__":
    main()
