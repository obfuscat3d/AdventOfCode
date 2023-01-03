PRIORITY = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def part1(sacks):
    extras = [(set(s[:len(s) // 2]) & set(s[len(s) // 2:])).pop() for s in sacks]
    print(sum([PRIORITY.index(x) for x in extras]))


def part2(sacks):
    badges = []
    for x in range(len(sacks) // 3):
        badges.append((set(sacks[3 * x]) & set(sacks[3 * x + 1])
                       & set(sacks[3 * x + 2])).pop())

    print(sum([PRIORITY.index(x) for x in badges]))


sacks = open("input").read().split('\n')
part1(sacks)
part2(sacks)
