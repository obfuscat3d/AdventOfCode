def parse(filename):
    lines = open(filename).read().split('\n')
    state = {i: c for i, c in enumerate(lines[0][15:])}
    trans = {l[:5]: l[9] for l in lines[2:]}
    return state, trans


def iter(state, trans):
    min_x, max_x = int(min(state.keys())) - 2, int(max(state.keys())) + 2
    new_state = {}
    for x in range(min_x, max_x + 1):
        new_state[x] = trans[''.join(state.get(i, '.') for i in range(x - 2, x + 3))]
    return new_state


def part1(state, trans):
    for _ in range(20):
        state = iter(state, trans)
    print(sum(k for k, v in state.items() if v == '#'))


def part2(state, trans):
    scores = []
    while len(scores) < 3 or (scores[-1] - scores[-2] != scores[-2] - scores[-3]):
        state = iter(state, trans)
        scores.append(sum(k for k, v in state.items() if v == '#'))

    print((50000000000 - len(scores)) * (scores[-1] - scores[-2]) + scores[-1])


state, trans = parse("input")
part1(state, trans)
part2(state, trans)
