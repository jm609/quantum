import random
import cirq

def make_quantum_teleportation_circuit(ranX, ranY):
    circuit = cirq.Circuit()
    msg, alice, bob= cirq.LineQubit.range(3)
    # 엘리스와 밥 사이의 공유할 벨 상태 생성
    circuit.append([cirq.H(alice), cirq.CNOT(alice, bob)])
    # 메세지에 해당하는 임의의 상태 생성
    circuit.append([cirq.X(msg)**ranX, cirq.Y(msg)**ranY])
    # 메세지와 엘리스의 얽힌 큐비트에 대해 벨 측정
    circuit.append([cirq.CNOT(msg, alice), cirq.H(msg)])
    circuit.append(cirq.measure(msg, alice))
    # 두 개의 고전 비트를 사용해 벨 측정 결과로부터 밥의 얽힌 큐비트에 원래 양자 메세지 복원
    circuit.append([cirq.CNOT(alice, bob), cirq.CZ(msg, bob)])
    return msg, circuit

def main():
    # 양자 순간 이동할 임의의 상태를 인코딩
    ranX = random.random()
    ranY = random.random()
    msg, circuit = make_quantum_teleportation_circuit(ranX, ranY)
    sim = cirq.Simulator()
    message = sim.simulate(cirq.Circuit([cirq.X(msg)**ranX, cirq.Y(msg)**ranY]))
    # 엘리스의 큐비트에 해당하는 블로흐 구 출력
    b0X, b0Y, b0Z = cirq.bloch_vector_from_state_vector(
        message.final_state_vector, 0)
    print("x: ", round(b0X, 4),
          "y: ", round(b0Y, 4),
          "z: ", round(b0Z, 4))
    print(circuit)
    # 시뮬레이션의 최종 상태 기록
    final_results = sim.simulate(circuit)  
    # 밥의 큐비트에 해당하는 블로흐 구 출력
    b2X, b2Y, b2Z = cirq.bloch_vector_from_state_vector(final_results.final_state_vector, 2)
    print("x: ", round(b2X, 4),
          "y: ", round(b2Y, 4),
          "z: ", round(b2Z, 4))
          
if __name__ == '__main__':
    main()