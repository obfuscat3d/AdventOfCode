from collections import defaultdict


def parse(filename):
    text = open(filename).read().split("\n")
    constraints = defaultdict(list)
    tasks = set()
    for l in text:
        tasks.add(l[36])
        tasks.add(l[5])
        constraints[l[36]].append(l[5])
    return constraints, sorted(list(tasks))


def part1(constraints, tasks):
    complete, ans = set(), ""
    while len(complete) < len(tasks):
        for t in tasks:
            if t in complete:
                continue
            if all([c in complete for c in constraints[t]]):
                ans += t
                complete.add(t)
                break
    print(ans)


def part2(constraints, tasks):
    complete, in_progress = set(), set()
    EXTRA_TIME, WORKERS = 60, 4
    elves = [(0, None)] * WORKERS
    time = -1

    while len(complete) < len(tasks):
        time += 1
        for i, e in enumerate(elves):
            if e[0] == 0:
                if e[1]:
                    complete.add(e[1])
                elves[i] = (0, None)

        for i, e in enumerate(elves):
            if e[0] == 0:
                for t in tasks:
                    if t in complete:
                        continue
                    if t not in in_progress and all([c in complete for c in constraints[t]]):
                        elves[i] = [EXTRA_TIME + ord(t) - ord('A') + 1, t]
                        in_progress.add(t)
                        break

        for i, e in enumerate(elves):
            elves[i] = (max(0, e[0] - 1), e[1])

    print(time)


constraints, tasks = parse("input")
part1(constraints, tasks)
part2(constraints, tasks)
