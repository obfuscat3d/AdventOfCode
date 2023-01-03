from collections import deque
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Unit:
    uid: int
    team: str
    p: complex
    hp: int = 200
    fp: int = 3


@dataclass
class State:
    grid: dict
    units: list
    move_list: list
    round: int

    def unit_from_pos(self, p):
        return next((u for u in self.units if u.p == p), None)

    def unit_from_uid(self, id):
        return next((u for u in self.units if u.uid == id), None)


def neighbors(p):
    return [p - 1j, p - 1, p + 1, p + 1j]  # in reading order


def ordered_uid_list(s):
    units = sorted(s.units, key=lambda x: 1000 * x.p.imag + x.p.real)
    return [u.uid for u in units]


def parse(filename):
    grid, units = {}, []
    for y, line in enumerate(open(filename).read().split('\n')):
        for x, c in enumerate(line):
            grid[x + 1j * y] = c
            if c in ['G', 'E']:
                units.append(Unit(len(units), c, x + 1j * y, 200, 3))
    return State(grid, units, [], 0)


def find_move(s, unit):
    queue = deque([[p] for p in neighbors(unit.p) if s.grid[p] == '.'])
    seen, targets, min_distance_to_target = set(), [], None
    while queue:
        cur = queue.popleft()
        if len(cur) == min_distance_to_target:
            continue
        for n in neighbors(cur[-1]):
            if n in seen:
                continue
            seen.add(n)
            if s.grid[n] in ['G', 'E'] and s.grid[n] != unit.team:
                targets.append(cur + [n])
                min_distance_to_target = len(cur) + 1
            elif s.grid[n] == '.':
                queue.append(cur + [n])

    targets = sorted(targets, key=lambda x: 1000 * x[-1].imag + x[-1].real)
    return targets[0][0] if targets else None


def move(s, uid):
    unit = s.unit_from_uid(uid)
    dest = find_move(s, unit)
    if dest:
        s.grid[unit.p] = '.'
        s.grid[dest] = unit.team
        unit.p = dest


def attack(s, uid):
    unit, targets = s.unit_from_uid(uid), []
    for p in neighbors(unit.p):
        if s.grid[p] in ['E', 'G'] and s.grid[p] != unit.team:
            targets.append(s.unit_from_pos(p))

    if not targets:
        return False

    targets = sorted(targets, key=lambda x: 10000000 * x.hp + 1000 * x.p.imag + x.p.real)
    targets[0].hp -= unit.fp
    if targets[0].hp <= 0:
        s.grid[targets[0].p] = '.'
        s.units = [u for u in s.units if u.uid != targets[0].uid]
    return True


def step(s):
    if not s.move_list:
        s.move_list = ordered_uid_list(s)
    uid = s.move_list.pop(0)
    if s.unit_from_uid(uid) and not attack(s, uid):
        move(s, uid)
        attack(s, uid)
    if not s.move_list:
        s.round += 1


def part1(s):
    while 'E' in s.grid.values() and 'G' in s.grid.values():
        step(s)
    print(s.round * sum(u.hp for u in s.units))


def mod_elf_power(s, new_power):
    for u in s.units:
        if u.team == 'E':
            u.fp = new_power
    elf_count = len([1 for v in s.grid.values() if v == 'E'])
    while 'E' in s.grid.values() and 'G' in s.grid.values():
        step(s)
    return len([1 for v in s.grid.values() if v == 'E']) == elf_count


def part2(s):
    new_power, s_temp = 4, deepcopy(s)
    while not mod_elf_power(s_temp, new_power):
        new_power, s_temp = new_power + 1, deepcopy(s)
    print(s_temp.round * sum(u.hp for u in s_temp.units))


state = parse("input")
part1(deepcopy(state))
part2(deepcopy(state))
