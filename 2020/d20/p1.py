import math


def clockwise(tile): return list(zip(*tile[::-1]))
def flip(tile): return [t[::-1] for t in tile]
def left(tile): return [tile[x][0] for x in range(len(tile))]
def right(tile): return [tile[x][len(tile[0])-1] for x in range(len(tile))]
def top(tile): return [tile[0][y] for y in range(len(tile[0]))]
def bottom(tile): return [tile[len(tile)-1][y] for y in range(len(tile[0]))]


# position relative to fixed image, edge selector for each position
RELATIVE_POSITION_CHECKS = [
    (0, -1, lambda x: left(x), lambda x: right(x)),
    (0, 1, lambda x: right(x), lambda x: left(x)),
    (-1, 0, lambda x: top(x), lambda x: bottom(x)),
    (1, 0, lambda x: bottom(x), lambda x: top(x))
]

TRANSFORMATIONS = [
    lambda x: x,
    lambda x: clockwise(x),
    lambda x: clockwise(clockwise(x)),
    lambda x: clockwise(clockwise(clockwise(x))),
    lambda x: flip(x),
    lambda x: clockwise(flip(x)),
    lambda x: clockwise(clockwise(flip(x))),
    lambda x: clockwise(clockwise(clockwise(flip(x))))
]


def match(final_grid, i0, i1):
    for dx, dy, e0, e1 in RELATIVE_POSITION_CHECKS:
        if not (i0['pos'][0]+dx, i0['pos'][1] + dy) in final_grid:
            for t in TRANSFORMATIONS:
                if e0(i0['tile']) == e1(t(i1['tile'])):
                    i1['tile'] = t(i1['tile'])
                    i1['pos'] = (i0['pos'][0]+dx, i0['pos'][1] + dy)
                    final_grid[i1['pos']] = i1
                    return True
    return False


def parse_image(image_text):
    [id_text, image_text] = image_text.split('\n', 1)
    image = [[p for p in line] for line in image_text.split('\n')]
    return {'id': int(id_text[5:9]),
            'pos': None,
            'tile': image}


def place_images_in_grid(images):
    final_grid = {(0, 0): images[0]}
    images[0]['pos'] = (0, 0)
    to_be_placed = images[1:]
    while to_be_placed:
        to_remove = []
        for image1 in to_be_placed:
            for image0 in final_grid.values():
                if (match(final_grid, image0, image1)):
                    to_remove.append(image1)
                    break
        to_be_placed = [i for i in to_be_placed if not i in to_remove]
    return final_grid


def multiply_edges(final_grid):
    minX = min([pos[0] for pos in final_grid.keys()])
    maxX = max([pos[0] for pos in final_grid.keys()])
    minY = min([pos[1] for pos in final_grid.keys()])
    maxY = max([pos[1] for pos in final_grid.keys()])
    return math.prod([final_grid[(minX, minY)]['id'],
                      final_grid[(minX, maxY)]['id'],
                      final_grid[(maxX, minY)]['id'],
                      final_grid[(maxX, maxY)]['id']])


with open('2020/d20/input') as input:
    images = [parse_image(i) for i in input.read().split('\n\n')]

print(multiply_edges(place_images_in_grid(images)))
