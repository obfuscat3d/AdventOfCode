import re
from dataclasses import dataclass
from copy import deepcopy


@dataclass
class Group:
    team: str
    id: int
    units: int
    hp: int
    initiative: int
    damage: int
    attack: str
    weak: list
    immune: list


def make_group(s, team, id):
    units, hp, damage, initiative = map(int, re.findall("\d+", s))
    attack = s.split(' ')[-5]
    weak, immune = [], []
    # ugh, this is hella inelegant...
    if "weak" in s:
        i = s.find("weak")
        ws = s[i + 8:]
        cur = ""
        while ws[0] not in [';', ')']:
            if ws[0] == ',':
                weak.append(cur)
                cur = ""
                ws = ws[2:]
            else:
                cur += ws[0]
                ws = ws[1:]
        weak.append(cur)
    if "immune" in s:
        i = s.find("immune")
        ws = s[i + 10:]
        cur = ""
        while ws[0] not in [';', ')']:
            if ws[0] == ',':
                immune.append(cur)
                cur = ""
                ws = ws[2:]
            else:
                cur += ws[0]
                ws = ws[1:]
        immune.append(cur)
    return Group(team, id, units, hp, initiative, damage, attack, weak, immune)


def parse(filename):
    text = open(filename).read()
    immune_text, infection_text = text.split('\n\n')
    immune = [make_group(s, "Immune", i + 1) for i, s in enumerate(immune_text.split('\n')[1:])]
    infection = [make_group(s, "Infection", i + 1) for i, s in enumerate(infection_text.split('\n')[1:])]
    return immune, infection


def ep(g):
    return g.units * g.damage


def damage(attacker, defender):
    if attacker.attack in defender.immune:
        return 0
    return ep(attacker) * (2 if attacker.attack in defender.weak else 1)


def get_targets(attackers, defenders):
    attackers = sorted(attackers, key=lambda x: (1 << 32) * ep(x) + x.initiative, reverse=True)
    untargeted = defenders.copy()
    targets = []
    for a in attackers:
        potential_targets = [t for t in untargeted if damage(a, t)]
        if not potential_targets:
            targets.append((a, None))
            continue
        target = potential_targets[0]
        for t in potential_targets[1:]:
            if damage(a, t) > damage(a, target):
                target = t
            elif damage(a, t) == damage(a, target) and ep(t) > ep(target):
                target = t
            elif damage(a, t) == damage(a, target) and ep(t) == ep(target) and t.initiative > target.initiative:
                target = t
        targets.append((a, target))
        untargeted.remove(target)
    return targets


def battle(immune, infection):
    round, ROUND_LIMIT = 0, 10000
    while round < ROUND_LIMIT and immune and infection:
        round += 1
        immune_targets = get_targets(immune, infection)
        infection_targets = get_targets(infection, immune)
        attacks = sorted(immune_targets + infection_targets, key=lambda x: x[0].initiative, reverse=True)
        while attacks:
            a, t = attacks.pop(0)
            if not t:
                continue
            if a.units <= 0 or t.units <= 0:
                continue
            t.units -= damage(a, t) // t.hp
        immune = [i for i in immune if i.units > 0]
        infection = [i for i in infection if i.units > 0]
    return sum(i.units for i in immune), sum(i.units for i in infection)


def part1(immune, infection):
    a, b = battle(immune, infection)
    print(a + b)


def part2(immune, infection):
    boost, immune_survivors, infected_survivors = 0, 0, 0
    while immune_survivors == 0 or infected_survivors > 0:
        boost += 1
        temp_immune, temp_infection = deepcopy(immune), deepcopy(infection)
        for g in temp_immune:
            g.damage += boost
        immune_survivors, infected_survivors = battle(temp_immune, temp_infection)
    print(immune_survivors)


immune, infection = parse("input")
part1(deepcopy(immune), deepcopy(infection))
part2(deepcopy(immune), deepcopy(infection))
