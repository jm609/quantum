from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.circuit.library import MCMT
from qiskit.visualization import circuit_drawer
import random

def create_oracle(circuit, input_qubits, ancilla_qubit, x_bits):
    # 타겟 상태에 대한 오라클 구현
    for qubit, bit in zip(input_qubits, x_bits):
        if not bit:
            circuit.x(qubit)
    
    # 다중 제어 Toffoli 게이트
    circuit.mcx(input_qubits, ancilla_qubit)
    
    # 입력 큐비트 복원
    for qubit, bit in zip(input_qubits, x_bits):
        if not bit:
            circuit.x(qubit)

def create_diffusion(circuit, input_qubits):
    # Diffusion 연산자 구현
    circuit.h(input_qubits)
    circuit.x(input_qubits)
    
    # 다중 제어 Z-게이트 구현
    circuit.h(input_qubits[-1])
    circuit.mcx(input_qubits[:-1], input_qubits[-1])
    circuit.h(input_qubits[-1])
    
    circuit.x(input_qubits)
    circuit.h(input_qubits)

def create_grover_circuit(qubit_count, x_bits):
    # 레지스터 생성
    qr = QuantumRegister(qubit_count, 'q')
    ancilla = QuantumRegister(1, 'ancilla')
    cr = ClassicalRegister(qubit_count, 'c')
    
    # 양자 회로 생성
    circuit = QuantumCircuit(qr, ancilla, cr)
    
    # 초기 중첩 상태 준비
    circuit.h(qr)
    circuit.x(ancilla)
    circuit.h(ancilla)
    
    # Grover 반복 횟수 계산 (π/4 * √N에 가장 가까운 정수)
    iterations = int(round(3.14159 / 4.0 * 2**(qubit_count/2)))
    
    # Grover 반복
    for _ in range(iterations):
        # 오라클 적용
        create_oracle(circuit, qr, ancilla, x_bits)
        # 확산 연산자 적용
        create_diffusion(circuit, qr)
    
    # 측정
    circuit.measure(qr, cr)
    
    return circuit

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

def main():
    # 파라미터 설정
    qubit_count = 2  # 2개의 큐비트로 시작
    shots = 100    # 측정 횟수
    
    # 무작위 타겟 비트열 생성
    x_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    print('비밀 비트열:', bitstring(x_bits))
    
    # Grover 회로 생성
    circuit = create_grover_circuit(qubit_count, x_bits)
    print('회로:')
    print(circuit)
    
    # 시뮬레이션 실행
    backend = Aer.get_backend('qasm_simulator')
    job = backend.run(circuit, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    print('\n측정 결과:', counts)
    
    # 가장 많이 측정된 상태 찾기
    most_common_state = max(counts.items(), key=lambda x: x[1])[0]
    print('가장 많이 측정된 상태:', most_common_state)
    print('비밀 비트열과 일치:', most_common_state == bitstring(x_bits))
    
    # 회로 시각화
    circuit_drawer(circuit, output='mpl')

if __name__ == '__main__':
    main()
