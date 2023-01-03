PRIORITY = "_abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

sacks = open("input").read().split('\n')

extras = []
for sack in sacks:
    extras.append((set(sack[:len(sack)//2]) & set(sack[len(sack)//2:])).pop())

print(sum([PRIORITY.index(x) for x in extras]))

badges = []
for x in range(len(sacks)//3):
    badges.append((set(sacks[3*x]) & set(sacks[3*x+1])
                   & set(sacks[3*x+2])).pop())

print(sum([PRIORITY.index(x) for x in badges]))
