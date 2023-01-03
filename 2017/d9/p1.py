text = open("input").read()

depth, score, trash_count, is_trash = 1, 0, 0, False
while text:
    if not is_trash and text[0] == '{':
        depth, score = depth + 1, score + depth
    elif not is_trash and text[0] == '<':
        is_trash = True
    elif is_trash and text[0] == '>':
        is_trash = False
    elif is_trash and text[0] == '!':
        text = text[1:]
    elif not is_trash and text[0] == '}':
        depth -= 1
    elif is_trash:
        trash_count += 1
    text = text[1:]

print(score)
print(trash_count)
