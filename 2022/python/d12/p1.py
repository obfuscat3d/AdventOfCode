from collections import deque


def is_valid_move(g, p1, p2):
    return p2 in g and ord(g[p1]) - ord(g[p2]) <= 1


grid = {x + y * 1j: e for y, l in enumerate(open("input").read().split('\n')) for x, e in enumerate(l)}
start = [k for k, v in grid.items() if v == 'S'][0]
end = [k for k, v in grid.items() if v == 'E'][0]
grid[start], grid[end] = 'a', 'z'
distance, queue = {end: 0}, deque([end])

while queue:
    p1 = queue.popleft()
    for p2 in [p1 - 1, p1 + 1, p1 - 1j, p1 + 1j]:
        if not p2 in distance and is_valid_move(grid, p1, p2):
            distance[p2] = distance[p1] + 1
            queue.append(p2)

print(distance[start])
print(sorted(distance[p] for p in distance if grid[p] in "Sa")[0])
