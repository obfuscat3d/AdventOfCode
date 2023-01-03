import string


def reduce(polymer):
    i = 0
    while i < len(polymer) - 1:
        if ord(polymer[i]) - ord(polymer[i + 1]) in [ord('A') - ord('a'), ord('a') - ord('A')]:
            polymer = polymer[:i] + polymer[i + 2:]
            i = max(0, i - 1)
        else:
            i += 1
    return polymer


def part1(filename):
    print(len(reduce(open(filename).read())))


def part2(filename):
    polymer, best = list(open(filename).read()), 1 << 32
    for a, A in zip(string.ascii_lowercase, string.ascii_uppercase):
        np = [p for p in polymer if p not in [a, A]]
        best = min(best, len(reduce(np)))
    print(best)


part1("input")
part2("input")
