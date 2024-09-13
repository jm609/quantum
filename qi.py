import qiskit

qreg = qiskit.QuantumRegister(1, name='qreg')
creg = qiskit.ClassicalRegister(1, name='creg')
circ = qiskit.QuantumCircuit(qreg, creg)
circ.x(qreg[0])
circ.measure(qreg, creg)
print(circ.draw())
