sign = lambda x: -1 if x < 0 else 0 if x == 0 else 1
moves = [(x.split(' ')[0], int(x.split(' ')[1])) for x in open("input").read().split('\n')]
dirs = {'R': 1, 'U': 1j, 'L': -1, 'D': -1j}
kts, k1, k9 = [0] * 10, set(), set()

for move in moves:
    for _ in range(move[1]):
        kts[0] += dirs[move[0]]
        for i in range(1, 10):
            d = kts[i - 1] - kts[i]
            if abs(d) >= 2:
                kts[i] += sign(d.real) + 1j * sign(d.imag)
        k1.add(kts[1])
        k9.add(kts[9])

print(len(k1))
print(len(k9))
