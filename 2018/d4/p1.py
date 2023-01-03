from collections import defaultdict
from datetime import datetime

START, SLEEP, WAKE = 0, 1, 2


def parse(filename):
    entries = []
    for l in open("input").read().split('\n'):
        t = datetime.fromisoformat(l[1:17])
        if 'sleep' in l:
            entries.append((SLEEP, t))
        elif 'wakes' in l:
            entries.append((WAKE, t))
        else:
            entries.append((START, t, int(l.split()[3][1:])))
    return sorted(entries, key=lambda x: x[1])


def calc_guard_sleep(entries):
    log, guard, start = defaultdict(int), defaultdict(int), 0
    for e in entries:
        if e[0] == START:
            guard = e[2]
        elif e[0] == SLEEP:
            start = e[1]
        elif e[0] == WAKE:
            for m in range(start.minute, e[1].minute):
                log[guard, m] += 1
    return log


def part1(log):
    guards = defaultdict(int)
    for k, v in log.items():
        guards[k[0]] += v
    guard = max(guards, key=lambda x: guards[x])
    guard_day = {k[1]: v for k, v in log.items() if k[0] == guard}
    print(guard * max(guard_day, key=lambda x: guard_day[x]))


def part2(log):
    sleepiest = max(log, key=lambda x: log[x])
    print(sleepiest[0] * sleepiest[1])


log = calc_guard_sleep(parse('input'))
part1(log)
part2(log)
