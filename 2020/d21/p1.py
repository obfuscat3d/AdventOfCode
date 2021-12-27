from collections import Counter

with open('2020/d21/input') as input:
    menu_items = [(line.split(' (contains ')[0].split(' '),
                  line.split(' (contains ')[1][:-1].split(', '))
                  for line in input.read().splitlines()]

# Create a set of all incredients and which ingredients may be which allergen
ingredient_counts = Counter()
possible_allergens = {}
for ingredients, allergens in menu_items:
    ingredient_counts.update(ingredients)
    for allergen in allergens:
        if allergen in possible_allergens:
            possible_allergens[allergen] = \
                possible_allergens[allergen] & set(ingredients)
        else:
            possible_allergens[allergen] = set(ingredients)

# Process possible allergens until each allergen has exactly one food
again = True
while again:
    again = False
    for allergen, foods in possible_allergens.items():
        if len(foods) == 1:
            for a, f in possible_allergens.items():
                if a != allergen and list(foods)[0] in f:
                    again = True
                    f.remove(list(foods)[0])

all_allergens = []
for allergen, foods in possible_allergens.items():
    all_allergens.append((list(foods)[0], allergen))

# Part 1
print(len([i for i in ingredient_counts.elements() if i not in all_allergens]))

# Part 2
all_allergens.sort(key=lambda x: x[1])
print(','.join([i[0] for i in all_allergens]))