def parse(filename):
    return open(filename).read()


def part1(text):
    total = int(text[0]) if text[0] == text[-1] else 0
    for i, c in enumerate(text[:-1]):
        if c == text[i + 1]:
            total += int(c)
    print(total)


def part2(text):
    total = 0
    for i, x in enumerate(text):
        if x == text[(i + len(text) // 2) % len(text)]:
            total += int(x)
    print(total)


data = parse("input")
part1(data)
part2(data)
