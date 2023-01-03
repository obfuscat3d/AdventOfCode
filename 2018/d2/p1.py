def part1(filename):
    text = open(filename).read().split('\n')
    twos, threes = 0, 0
    for l in text:
        twoc, threec = False, False
        for c in l:
            if not twoc and l.count(c) == 2:
                twos += 1
                twoc = True
            if not threec and l.count(c) == 3:
                threes += 1
                threec = True
    print('part1: ', (twos * threes))


def part2(filename):
    text = open(filename).read().split('\n')
    words = [set(enumerate(word)) for word in text]
    for a in words:
        for b in words:
            if a != b and len(a - b) == 1:
                print(''.join(c[1] for c in sorted(list(a & b))))
                return


part1("input")
part2("input")
