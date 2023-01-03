""" Got 38/84 on the leaderboard! """

from collections import defaultdict


def get_grid():
    T = open("input").read().split('\n')
    return {x + 1j * y for y, l in enumerate(T) for x, c in enumerate(l) if c == '#'}


neighbors = lambda p: [p - 1, p + 1, p - 1j, p + 1j, p + 1 + 1j, p + 1 - 1j, p - 1 + 1j, p - 1 - 1j]


def elf_move(grid, p, round_no):
    if all(not p1 in grid for p1 in neighbors(p)):
        return p
    moves_ops = [([p - 1j, p + 1 - 1j, p - 1 - 1j], p - 1j),
                 ([p + 1j, p + 1 + 1j, p - 1 + 1j], p + 1j),
                 ([p - 1 + 1j, p - 1 - 1j, p - 1], p - 1),
                 ([p + 1 + 1j, p + 1 - 1j, p + 1], p + 1)]
    for i in range(round_no, round_no + 4):
        if all(p1 not in grid for p1 in moves_ops[i % len(moves_ops)][0]):
            return moves_ops[i % len(moves_ops)][1]
    return p


def do_round(grid, round_no):
    did_move, moves, new_grid = False, defaultdict(list), set()
    for elf in grid:
        new_p = elf_move(grid, elf, round_no)
        if new_p != elf:
            did_move = True
        moves[new_p].append(elf)
    for k, v in moves.items():
        if len(v) == 1:
            new_grid.add(k)
        else:
            new_grid.update(v)
    return new_grid, did_move


def part1():
    grid = get_grid()
    for round_no in range(10):
        grid, _ = do_round(grid, round_no)
    ys = sorted([i.imag for i in grid])
    xs = sorted([i.real for i in grid])
    print((xs[-1] - xs[0] + 1) * (1 + ys[-1] - ys[0]) - len(grid))


def part2():
    did_move, grid, round_no = True, get_grid(), 0
    while did_move:
        grid, did_move = do_round(grid, round_no)
        round_no += 1
    print(round_no)


part1()
part2()
