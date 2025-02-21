import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector
from qiskit_aer import Aer
# 복소 계수 정의
coefficients = [0.35+0.02j, -0.32, 0.37-0.02j, -0.35+0.04j,
                0.30-0.02j, -0.34j, 0.37-0.04j, -0.41] 

# 초기 상태 생성 (정규화)
norm = np.linalg.norm(coefficients)
normalized_coefficients = [c / norm for c in coefficients]
initial_state = Statevector(normalized_coefficients)

# 양자 회로 생성
qc = QuantumCircuit(3)
qc.initialize(initial_state.data, [0, 1, 2])

# QFT 구현 (3큐비트)
def qft_3qubits(circuit, n):
    for i in range(n):
        circuit.h(i)
        for j in range(i + 1, n):
            circuit.cp(np.pi / (2 ** (j - i)), j, i)
    # 큐비트 스왑
    for i in range(n // 2):
        circuit.swap(i, n - i - 1)

# QFT 적용
qft_3qubits(qc, 3)

# 결과 출력
print(qc)

# 시뮬레이션 실행
simulator = Aer.get_backend('statevector_simulator')
job = simulator.run(qc)
result = job.result()
output_state = result.get_statevector()

print("Output State:", output_state)

# 각 상태의 확률 계산
probabilities = np.abs(output_state) ** 2
for i, prob in enumerate(probabilities):
    print(f"State |{i:03b}>: Probability = {prob:.4f}")