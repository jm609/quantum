# 벨 부등식 테스트
# a(X) XOR b(y) == xy

import cirq
import numpy as np

def make_bell_test_circuit():
    alice = cirq.GridQubit(0, 0) 
    bob = cirq.GridQubit(1, 0)
    alice_referee =cirq.GridQubit(0, 1)
    bob_referee =cirq.GridQubit(1, 1)
    circuit = cirq.Circuit()

    # 앨리스와 밥이 공유하는 얽힌 상태 준비
    circuit.append([
        cirq.H(alice),
        cirq.CNOT(alice, bob),
        cirq.X(alice)**-0.25
    ])    

    # 심판이 동전 던지기 수행
    circuit.append([
        cirq.H(alice_referee),
        cirq.H(bob_referee),
    ])

    # 참여자들은 심판이 동전을 던져 나온 결과에 따라 sqrt(X) 수행
    circuit.append([
        cirq.CNOT(alice_referee, alice)**0.5,
        cirq.CNOT(bob_referee, bob)**0.5,
    ])

    circuit.append([
        cirq.measure(alice, key='a'),
        cirq.measure(bob, key='b'),
        cirq.measure(alice_referee, key='x'),
        cirq.measure(bob_referee, key='y'),
    ])

    return circuit


def bitstring(bits):
    return ''.join('1' if e else '_' for e in bits)

def main():
    circuit = make_bell_test_circuit()
    print(circuit)
    repetitions = 1000
    result = cirq.Simulator().run(program=circuit, repetitions=repetitions)

    # 결과 수집
    a = np.array(result.measurements['a'][:, 0])
    b = np.array(result.measurements['b'][:, 0])
    x = np.array(result.measurements['x'][:, 0])
    y = np.array(result.measurements['y'][:, 0])

    # 승률 계산
    outcomes = a ^ b == x & y
    win_percent = len([e for e in outcomes if e]) * 100 / repetitions

    # 데이터 출력
    print('a: ', bitstring(a))
    print('b: ', bitstring(b))
    print('x: ', bitstring(x))
    print('y: ', bitstring(y))
    print('(a XOR b) == (XY):\n', bitstring(outcomes))
    print('승률: {}%'.format(win_percent))

if __name__ == '__main__':
    main()