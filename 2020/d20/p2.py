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


def pixel_from_final_grid(final_grid, x, y):
    minX = min([pos[0] for pos in final_grid.keys()])
    minY = min([pos[1] for pos in final_grid.keys()])
    gridX = minX + math.floor(x/8)
    gridY = minY + math.floor(y/8)
    tileX = x % 8 + 1
    tileY = y % 8 + 1
    return final_grid[(gridX, gridY)]['tile'][tileX][tileY]


def image_frim_grid(final_grid):
    minX = min([pos[0] for pos in final_grid.keys()])
    maxX = max([pos[0] for pos in final_grid.keys()])
    minY = min([pos[1] for pos in final_grid.keys()])
    maxY = max([pos[1] for pos in final_grid.keys()])
    full_image = []
    for x in range(8*(maxX-minX+1)):
        temp = []
        for y in range(8*(maxY-minY+1)):
            temp.append(pixel_from_final_grid(final_grid, x, y))
        full_image.append(temp)
    return full_image


def print_image(image):
    for row in image:
        for pixel in row:
            print(pixel, end='')
        print()
    print()


SEA_MONSTER = """                  #
#    ##    ##    ###
 #  #  #  #  #  #  """.split('\n')


def check_sea_monster(image, x, y):
    for i in range(len(SEA_MONSTER)):
        for j in range(len(SEA_MONSTER[0])):
            if SEA_MONSTER[i][j] == '#' and image[x+i][y+j] != '#':
                return False
    return True


def count_sea_monsters_without_transform(image):
    count = 0
    for x in range(len(image)-len(SEA_MONSTER)):
        for y in range(len(image[0])-len(SEA_MONSTER[0])):
            if check_sea_monster(image, x, y):
                count += 1
    return count


def count_most_sea_monsters(image):
    return max([count_sea_monsters_without_transform(t(image)) for t in TRANSFORMATIONS])


with open('2020/d20/input') as input:
    images = [parse_image(i) for i in input.read().split('\n\n')]

final_grid = place_images_in_grid(images)
full_image = image_frim_grid(final_grid)

monsters = count_most_sea_monsters(full_image)
hashes = [a for b in full_image for a in b].count('#')
print(hashes - 15*monsters)
