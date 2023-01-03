def parse(filename):
    return [l.split(' ') for l in open(filename).read().split('\n')]


def part1(data):
    print(len([1 for p in data if len(p) == len(set(p))]))


def part2(data):
    ans = 0
    for d in data:
        d = sorted(map(lambda x: ''.join(x), map(sorted, d)))
        ans += len(d) == len(set(d))
    print(ans)


data = parse("input")
part1(data)
part2(data)
