import numpy as np

moves = [(x.split(' ')[0], int(x.split(' ')[1]))
         for x in open("input").read().strip().split('\n')]
dirs = {'R': 1, 'U': 1j, 'L': -1, 'D': -1j}
kts, k1, k9 = [0]*10, set(), set()

for move in moves:
    for _ in range(move[1]):
        kts[0] += dirs[move[0]]
        for i in range(1, 10):
            d = kts[i-1] - kts[i]
            if abs(d) >= 2:
                kts[i] += np.sign(d.real) + 1j * np.sign(d.imag)
        k1.add(kts[1])
        k9.add(kts[9])

print(len(k1), len(k9))
