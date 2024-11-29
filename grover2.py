from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit_aer import Aer
from qiskit.circuit.library import MCMT
from qiskit.visualization import circuit_drawer
import random
import numpy as np
from qiskit import transpile

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
    # 개선된 확산 연산자
    circuit.h(input_qubits)
    circuit.x(input_qubits)
    
    # 위상 킥백 감소를 위한 제어-Z 구현
    circuit.h(input_qubits[-1])
    circuit.mcx(input_qubits[:-1], input_qubits[-1], 
               mode='noancilla')  # 보조 큐비트 없이 구현
    circuit.h(input_qubits[-1])
    
    circuit.x(input_qubits)
    circuit.h(input_qubits)
    circuit.barrier()  # 회로 최적화 제어

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
    
    # 최적의 반복 횟수 계산 개선
    N = 2**qubit_count
    iterations = int(round(3.14159265359 * np.sqrt(N)/4.0))
    
    # 진폭 증폭을 위한 위상 반전 추가
    for _ in range(iterations):
        create_oracle(circuit, qr, ancilla, x_bits)
        # 위상 보정
        circuit.phase(np.pi, qr)
        create_diffusion(circuit, qr)
    
    # 측정 전 추가 게이트
    circuit.barrier()  # 최적화 방지를 위한 장벽 추가
    circuit.measure(qr, cr)
    
    return circuit

def bitstring(bits):
    return ''.join(str(int(b)) for b in bits)

def main():
    # 파라미터 설정
    qubit_count = 2  # 2개의 큐비트로 시작
    shots = 1000    # 측정 횟수 증가
    
    # 무작위 타겟 비트열 생성
    x_bits = [random.randint(0, 1) for _ in range(qubit_count)]
    print('비밀 비트열:', bitstring(x_bits))
    
    # Grover 회로 생성
    circuit = create_grover_circuit(qubit_count, x_bits)
    print('회로:')
    print(circuit)
    
    # 실행 파라미터 조정
    backend = Aer.get_backend('qasm_simulator')
    backend_options = {
        "optimization_level": 3,
        "initial_statevector": True,
        "zero_threshold": 1e-10
    }
    
    # 회로 실행
    job = backend.run(circuit, 
                     shots=shots,
                     optimization_level=3,
                     backend_options=backend_options)
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
