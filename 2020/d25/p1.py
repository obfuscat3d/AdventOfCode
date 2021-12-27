card_pub = 6270530
door_pub = 14540258
modulus = 20201227

def calc_loop_size(n):
    v, i = 1, 0
    while v != n:
        v = (v*7) % modulus
        i += 1
    return i

card_loop_size = calc_loop_size(card_pub)
print(pow(door_pub, calc_loop_size(card_pub), modulus))
