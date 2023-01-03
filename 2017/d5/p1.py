def parse(filename):
    return list(map(int, open(filename).read().split('\n')))


def part1(data):
    ip, c = 0, 0
    while 0 <= ip < len(data):
        data[ip], ip, c = data[ip] + 1, ip + data[ip], c + 1
    print(c)


def part2(data):
    ip, c = 0, 0
    while 0 <= ip < len(data):
        data[ip], ip, c = data[ip] + (1 if data[ip] < 3 else -1), ip + data[ip], c + 1
    print(c)


data = parse("input")
part1(data.copy())
part2(data.copy())
