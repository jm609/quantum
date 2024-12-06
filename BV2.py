import random
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
def main():
    qubit_count = 8
    circuit_sample_count = 3
    
    # 레지스터 생성
    qr_input = QuantumRegister(qubit_count, 'input')
    qr_output = QuantumRegister(1, 'output')
    cr = ClassicalRegister(qubit_count, 'result')
    
    secret_bias_bit = random.randint(0, 1)
    secret_factor_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    
    print('비밀 함수:\nf(x) = x*<{}>+ {} (mod2)'.format(
        ','.join(str(e) for e in secret_factor_bits), secret_bias_bit))
    
    circuit = make_bernstein_vazirani_circuit(qr_input, qr_output, cr, 
                                            secret_factor_bits, secret_bias_bit)
    print('\n회로:')
    print(circuit)
    
    # 시뮬레이션 실행
    simulator = Aer.get_backend('aer_simulator')
    job = simulator.run(circuit, shots=circuit_sample_count)
    result = job.result()
    counts = result.get_counts(circuit)
    print('\n표본 실행 결과:\n{}'.format(counts))
    
    # 가장 많이 나온 결과 확인
    most_common_bitstring = max(counts.items(), key=lambda x: x[1])[0]
    print('\n가장 많이 나온 비트열과 비밀 인자의 일치 여부:\n{}'.format(
        most_common_bitstring == bitstring(secret_factor_bits)))
    plot_histogram(counts)
    plt.show()
def make_bernstein_vazirani_circuit(qr_input, qr_output, cr, secret_factor_bits, secret_bias_bit):
    circuit = QuantumCircuit(qr_input, qr_output, cr)
    
    # 초기화
    circuit.x(qr_output)
    circuit.h(qr_output)
    for i in range(len(qr_input)):
        circuit.h(qr_input[i])
    
    # 오라클 구현
    if secret_bias_bit:
        circuit.x(qr_output)
    for i, bit in enumerate(secret_factor_bits):
        if bit:
            circuit.cx(qr_input[i], qr_output[0])
    
    # 측정 전 Hadamard 변환
    for i in range(len(qr_input)):
        circuit.h(qr_input[i])
    
    # 측정
    circuit.measure(qr_input, cr)
    
    return circuit

def bitstring(bits):
    return ''.join(str(int(b)) for b in reversed(bits))

if __name__ == '__main__':
    main()
