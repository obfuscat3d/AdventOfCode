import re, collections, itertools as it

Brick = collections.namedtuple('Brick', ['id', 'cells', 'minZ'])

def parse(filename):
    bricks = []
    for i,l in enumerate(open(filename).readlines()):
        x1,y1,z1,x2,y2,z2 = map(int, re.findall(r'\d+', l))
        cells, minZ = [], 1<<16
        for x in range(min(x1,x2), max(x1,x2)+1):
            for y in range(min(y1,y2), max(y1,y2)+1):
                for z in range(min(z1,z2), max(z1,z2)+1):
                    cells.append((x,y,z))
                    minZ = min(minZ, z)
        bricks.append(Brick(i, cells, minZ)) 
    return sorted(bricks, key=lambda b: b.minZ)

def lower_brick(b):
    return Brick(b.id, [(x,y,z-1) for x,y,z in b.cells], b.minZ-1)

def can_lower(occupied, b):
    return b.minZ > 1 and not occupied & set((x,y,z-1) for x,y,z in b.cells)

def apply_gravity(bricks):
    final_bricks = {}
    occupied = set()
    for b in bricks:
        while can_lower(occupied, b):
            b = lower_brick(b)
        occupied |= set(x for x in b.cells)
        final_bricks[b.id] = b
    return final_bricks

sorted_bricks = parse("input")
relaxed_bricks = apply_gravity(sorted_bricks)

can_be_destroyed, would_destroy = 0, 0
for less_one in it.combinations(relaxed_bricks.values(), len(relaxed_bricks)-1):
    temp = apply_gravity(less_one)
    can_be_destroyed += all(tp.minZ == relaxed_bricks[id].minZ for id,tp in temp.items())
    would_destroy += sum(tp.minZ != relaxed_bricks[id].minZ for id,tp in temp.items())

print(can_be_destroyed)
print(would_destroy)