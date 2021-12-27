INPUT = [int(i) for i in '586439172']

def step(cups):
    removed_cups = [cups.pop(1), cups.pop(1), cups.pop(1)]

    destination = cups[0]-1
    while destination in removed_cups or destination == 0:
        destination -= 1
        if destination <= 0:
            destination = max(cups)

    destination_index = (cups.index(destination)+1) % len(cups)
    cups.insert(destination_index, removed_cups.pop())
    cups.insert(destination_index, removed_cups.pop())
    cups.insert(destination_index, removed_cups.pop())

    if destination_index:
        cups = cups[1:] + [cups[0]]
    else:
        cups = cups[4:] + cups[:4]

    return cups

cups = INPUT
for x in range(100):
    cups = step(cups)

print(''.join([str(cups[(cups.index(1) + x) % len(cups)])
      for x in range(1, len(cups))]))
