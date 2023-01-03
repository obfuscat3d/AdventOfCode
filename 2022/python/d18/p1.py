C = {tuple(map(int, l.split(','))) for l in open("input").read().split('\n')}
A = [(0, 0, 1), (0, 0, -1), (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0)]

reachable, seen, new_steam = 0, set(), [(0, 0, 0)]
while steam := new_steam:
    new_steam = []
    for s, a in [(s, a) for s in steam for a in A]:
        q = tuple(map(sum, zip(s, a)))
        if not q in seen and all(-1 <= x <= 21 for x in q):
            if q in C:
                reachable += 1
            else:
                seen.add(q)
                new_steam.append(q)

print(sum([1 for c in C for a in A if tuple(map(sum, zip(c, a))) not in C]))
print(reachable)
