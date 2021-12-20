from os import X_OK
import re

with open('2020/d14/input') as input:
    instructions = input.read().splitlines()


def addresses(mask, addr):
    addr |= int(mask.replace('X', '0'), 2)
    xs = [_.start() for _ in re.finditer('X', mask)]
    if not xs:  # No X's, return the addr as-is
        return [addr]

    # Replace the first X with a 1 and a 0 in in recursive calls
    new_mask = mask[:xs[0]] + '0' + mask[xs[0]+1:]
    bitmask = 1 << (35-xs[0])
    return addresses(new_mask, ~(bitmask | ~addr)) + addresses(new_mask, bitmask | addr)


def run(mask, memory, ins):
    [addr, val] = ins.split('] = ')
    addr = int(addr[4:])
    val = int(val)
    for a in addresses(mask, addr):
        memory[a] = val


mask, memory = None, {}
for i in instructions:
    if i.startswith('mask'):
        mask = i[7:]
    else:
        run(mask, memory, i)

print(sum(memory.values()))
