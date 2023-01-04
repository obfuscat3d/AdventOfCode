from collections import defaultdict


def parse(filename):
    text = open(filename).read()
    lines = text.split('\n')
    bridges = defaultdict(list)
    for l in lines:
        a, b = map(int, l.split('/'))
        bridges[a].append(b)
        bridges[b].append(a)
    return bridges


def dfs(bridges, start, cmp, used=set()):
    best = [0, 0]
    for b in bridges[start]:
        if (start, b) not in used and (b, start) not in used:
            result = dfs(bridges, b, cmp, used | {(b, start)})
            result[1] += start + b
            if cmp(best, result):
                best = result
    return [best[0] + 1, best[1]]


def part1(bridges):
    print(dfs(bridges, 0, cmp=lambda a, b: a[1] < b[1])[1])


def part2(bridges):
    print(dfs(bridges, 0, cmp=lambda a, b: a[0] < b[0] or (a[0] == b[0] and a[1] < b[1]))[1])


bridges = parse("input")
part1(bridges)
part2(bridges)
