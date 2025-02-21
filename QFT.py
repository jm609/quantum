from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
from qiskit.visualization import plot_histogram
from qiskit.circuit.library import QFT
import numpy as np
import matplotlib.pyplot as plt
initial_state = np.array([0.35+0.02j, -0.32, 0.37-0.02j, -0.35+0.04j, 0.30-0.02j, -0.34, 0.37-0.04j, -0.41])
initial_state = initial_state / np.linalg.norm(initial_state)  # 정규화

# 회로 생성
qc = QuantumCircuit(3)

# 초기 상태 적용 (Statevector 방식 사용)
from qiskit.quantum_info import Statevector
qc = QuantumCircuit(3)
qc.initialize(initial_state, [0, 1, 2])
qc.barrier()

# QFT 적용
qc.append(QFT(3), [0, 1, 2])
qc.barrier()

# 측정 추가
qc.measure_all()

# 회로 시뮬레이션
simulator = Aer.get_backend('aer_simulator')
compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()

# 결과 출력
counts = result.get_counts()
print(counts)
plot_histogram(counts)
plt.show()

