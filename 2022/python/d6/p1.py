def first_consecutive_unique(text, n):
    for x in range(len(text)):
        if len(set(text[x:x+n])) == n:
            return x+n


text = open("input").read()
print(first_consecutive_unique(text, 4))
print(first_consecutive_unique(text, 14))
