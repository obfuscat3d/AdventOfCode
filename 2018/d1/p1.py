def part1(filename):
    print(sum(map(int, open(filename).read().split('\n'))))


def part2(filename):
    data = list(map(int, open(filename).read().split('\n')))
    i, running_total, seen = 0, 0, set()
    while not running_total in seen:
        seen.add(running_total)
        running_total += data[i % len(data)]
        i += 1
    print(running_total)


part1("input")
part2("input")
