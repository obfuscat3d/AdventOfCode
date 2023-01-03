import numpy as np

moves = [(x.split(' ')[0], int(x.split(' ')[1]))
         for x in open("input").read().split('\n')]
dirs = {'R': (1, 0), 'U': (0, 1), 'L': (-1, 0), 'D': (0, -1)}
kts = [[0, 0] for _ in range(10)]
k1, k9 = set(), set()

for move in moves:
    for _ in range(move[1]):
        kts[0] = [kts[0][0]+dirs[move[0]][0], kts[0][1]+dirs[move[0]][1]]
        for i in range(1, 10):
            if (abs(kts[i][0] - kts[i-1][0]) == 2 or
                    abs(kts[i][1] - kts[i-1][1]) == 2):
                kts[i][0] += np.sign(kts[i-1][0] - kts[i][0])
                kts[i][1] += np.sign(kts[i-1][1] - kts[i][1])
        k1.add(tuple(kts[1]))
        k9.add(tuple(kts[9]))

print(len(k1), len(k9))
