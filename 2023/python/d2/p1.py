import re, math, collections

COLOR_AMOUNTS = {"red": 12, "green": 13, "blue": 14}


def game_score_1(line):
    for color, amount in COLOR_AMOUNTS.items():
        if any(int(m.split()[0]) > amount for m in re.findall(f"\\d+ {color}", line)):
            return 0
    return int(line.split(" ")[1][:-1])


def game_score_2(line):
    min_colors = collections.defaultdict(int)
    for color in COLOR_AMOUNTS:
        for m in re.findall(f"\\d+ {color}", line):
            min_colors[color] = max(min_colors[color], int(m.split()[0]))
    return math.prod(min_colors.values())


text = open("input").read()
print(sum(game_score_1(line) for line in text.split("\n")))
print(sum(game_score_2(line) for line in text.split("\n")))
