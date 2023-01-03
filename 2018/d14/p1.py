INPUT = "074501"

recipes, e1, e2 = "37", 0, 1
while INPUT not in recipes[-7:]:
    recipes += str(int(recipes[e1]) + int(recipes[e2]))
    e1 = (e1 + int(recipes[e1]) + 1) % len(recipes)
    e2 = (e2 + int(recipes[e2]) + 1) % len(recipes)
print(recipes[int(INPUT):int(INPUT) + 10])
print(recipes.index(INPUT))
