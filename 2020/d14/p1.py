with open('2020/d14/input') as input:
    instructions = input.read().splitlines()


def parsemask(m):
    mask1, mask0 = 0, 0
    bit = 35
    for i in m[7:]:
        if i == '1':
            mask1 |= 1 << bit
        if i == '0':
            mask0 |= 1 << bit
        bit -= 1
    return (mask0, mask1)


def run(masks, memory, ins):
    [addr, val] = ins.split('] = ')
    addr = int(addr[4:])
    val = int(val)
    memory[addr] = ~(~(val | masks[1]) | masks[0])


masks, memory = None, {}
for i in instructions:
    if i.startswith('mask'):
        masks = parsemask(i)
    else:
        run(masks, memory, i)

print(sum(memory.values()))
