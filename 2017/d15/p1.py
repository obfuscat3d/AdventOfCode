def gen(x, factor, mod_val):
    while True:
        x = (x * factor) % 2147483647
        if x % mod_val == 0:
            yield x


gA, gB = gen(512, 16807, 1), gen(191, 48271, 1)
print(sum(1 for _ in range(40_000_000) if 0xFFFF & next(gA) == 0xFFFF & next(gB)))

gA, gB = gen(512, 16807, 4), gen(191, 48271, 8)
print(sum(1 for _ in range(5_000_000) if 0xFFFF & next(gA) == 0xFFFF & next(gB)))
