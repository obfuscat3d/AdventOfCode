DIRS = {'N': -1j, 'E': 1, 'W': -1, 'S': 1j}


def calc_distances(path):
    p, stack, dist = 0, [], {0: 0}
    for c in path:
        if c in DIRS:
            if DIRS[c] + p in dist:
                dist[DIRS[c] + p] = min(dist[p] + 1, dist[DIRS[c] + p])
            else:
                dist[DIRS[c] + p] = dist[p] + 1
            p = p + DIRS[c]
        elif c == '(':
            stack.append(p)
        elif c == ')':
            p = stack[-1]
            stack.pop()
        elif c == '|':
            p = stack[-1]
    return dist


path = open('input').read()[1:-1]
distances = calc_distances(path)
print(max(distances.values()))
print(len([1 for i in distances.values() if i >= 1000]))
