import cirq

def bitstring(bits):
    return ''.join('1' if e else '0' for e in bits)

qreg = [cirq.LineQubit(x) for x in range(2)]
circ = cirq.Circuit()

# 각 메세지별 연산 딕셔너리
message = {"00": [], 
"01": [cirq.X(qreg[0])],
"10": [cirq.Z(qreg[0])],
"11": [cirq.X(qreg[0]), cirq.Z(qreg[0])]}

# 엘리스가 벨 쌍 생성
circ.append(cirq.H(qreg[0]))
circ.append(cirq.CNOT(qreg[0], qreg[1]))

# 엘리스가 보낼 메세지 선택 및 인코딩
m  = "01"
print(m)
circ.append(message[m])

# 밥이 벨 기저로 측정
circ.append(cirq.CNOT(qreg[0], qreg[1]))
circ.append(cirq.H(qreg[0]))
circ.append([cirq.measure(qreg[0]), cirq.measure(qreg[1])])

# 양자회로 출력
print(circ)

# 양자회로 시물레이션
sim = cirq.Simulator()
res =sim.run(circ, repetitions=1)
received_bits = res.measurements['q(0)'][0][0], res.measurements['q(1)'][0][0]

print(bitstring(received_bits))