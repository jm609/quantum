import qiskit
qc = qiskit.QuantumCircuit(2)
qc.h(0)
qc.cx(0, 1)
print(qc)
qc.measure_all()

from qiskit_aer import AerSimulator
from qiskit import transpile, assemble
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt
simulator = AerSimulator()

compiled_circuit = transpile(qc, simulator)
result = simulator.run(compiled_circuit).result()
counts = result.get_counts(qc)
print(counts)

plot_histogram(counts)
plt.show()