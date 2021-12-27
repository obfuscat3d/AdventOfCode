from collections import Counter

with open('2020/d24/input') as input:
    to_flip = input.read().splitlines()

tiles = {}
for tile in to_flip:
    c = {}
    for i in ['ne', 'nw', 'se', 'sw', 'w', 'e']:
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

print(len({k:v for k,v in tiles.items() if v}))
