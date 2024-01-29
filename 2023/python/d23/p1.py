from collections import defaultdict

NDIRS = {'>':1, '^': -1j, '<': -1, 'v':1j}
n4 = lambda p: [p - 1j, p - 1, p + 1, p + 1j]

def parse(fn):
    grid = {x+1j*y:c for y,l in enumerate(open(fn).readlines()) for x,c in enumerate(l.strip())}
    start, end = 1, max(p.real for p in grid)- 1+ 1j*max(p.imag for p in grid)
    return grid, start, end

def find_adjacent(start, grid, terminals, ndirs):
    adj, q = [], [(start,0,{start})]
    while q:
        p, l, seen = q.pop(0)
        if p in terminals and p != start:
            adj.append((p,l))
            continue

        neighbors = [n for n in n4(p) if n in grid and n not in seen and grid[n] != '#']
        if len(neighbors) > 1 and p != start:
            adj.append((p, l))
            continue

        for n in neighbors:
            if ndirs and grid[n] in NDIRS and n + NDIRS[grid[n]] != p:
                q.append((n + NDIRS[grid[n]], l+2, seen | {n, n+NDIRS[grid[n]]}))
            elif grid[n] == '.' or not ndirs:
                q.append((n, l+1, seen | {n}))
    return adj

def build_graph(grid, start, end, ndirs):
    graph, seen, q = defaultdict(list), set(), [start]
    while q:
        p = q.pop()
        if p in seen: 
            continue
        seen.add(p)
        for n, l in find_adjacent(p, grid, [start, end], ndirs):
            graph[p].append((n, l))
            if n not in seen:
                q.append(n)
    return graph

def longest_path(graph, start, end):
    longest, q = 0, [(start, 0, {start})]
    while q:
        p, l, seen = q.pop()
        if p == end:
            longest = max(longest, l)
            continue
        for n,nl in graph[p]:
            if n not in seen:
                q.append((n, l+nl, seen | {n}))
    return longest

def part1(grid, start, end):
    graph = build_graph(grid, start, end, True)
    print(longest_path(graph, start, end))

def part2(grid, start, end):
    graph = build_graph(grid, start, end, False)
    print(longest_path(graph, start, end))

grid, start, end = parse("input")
part1(grid, start, end)
part2(grid, start, end)
