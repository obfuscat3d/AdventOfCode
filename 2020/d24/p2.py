def parse_tiles(input):
    tiles = {}
    for tile in input:
        c = {}
        for i in ['ne', 'nw', 'se', 'sw','w','e']:
            c[i] = tile.count(i)
            tile = tile.replace(i, '')

        # Note: we treat the tiles as a 2d grid of east and northeast. They can be negative.
        c['ne'] += c['nw'] - c['se'] - c['sw']
        c['e'] += c['se'] - c['nw'] - c['w']

        k = (c['e'], c['ne'])
        if k in tiles:
            tiles[k] = not tiles[k]
        else:
            tiles[k] = True

    # only keep the black tiles, everything else is white
    return {k:v for k,v in tiles.items() if v}

def neighbors(k):
    return [(k[0]+x, k[1]+y) for x,y in [(1,0),(0,1),(-1,0),(0,-1),(-1,1),(1,-1)]]

def step(tiles):
    count = {} # number of neighbors that are black
    ret = {}
    # for each black tile, increment all neighbor counts
    for k,v in tiles.items():
        for n in neighbors(k):
            if n in count:
                count[n] += 1
            else:
                count[n] = 1

    return {k:True for k,v in count.items() if v == 2 or (v == 1 and k in tiles)}


with open('2020/d24/input') as input:
    tiles = parse_tiles(input.read().splitlines())

for x in range(100):
    tiles = step(tiles)
    print(len(tiles))
