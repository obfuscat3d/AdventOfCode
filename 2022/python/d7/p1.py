import collections
import itertools


def parse(filename):
    pwd, filesystem = '', collections.defaultdict(int)

    for line in open(filename).read().split('\n')[1:]:
        if '..' in line:
            pwd = pwd[:pwd.rindex('/')]
        elif '$ cd' in line:
            pwd = pwd + '/' + line[5:]
        elif (size := line.split(' ')[0]).isnumeric():
            for p in itertools.accumulate(pwd.split('/')):
                filesystem[p] += int(size)
    return filesystem


def part1(filesystem):
    print(sum([v for v in filesystem.values() if v <= 100000]))


def part2(filesystem):
    minimum_to_free = filesystem[""] + 30000000 - 70000000
    print([x for x in sorted(filesystem.values()) if x - minimum_to_free > 0][0])


filesystem = parse("input")
part1(filesystem)
part2(filesystem)
