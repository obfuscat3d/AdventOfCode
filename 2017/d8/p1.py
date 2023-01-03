from collections import defaultdict

max_val = 0
R = defaultdict(int)
for l in open("input").read().split('\n'):
    r1, op1, v1, _, r2, op2, v2 = l.split()
    r1, r2 = "qwer" + r1, "qwer" + r2
    if eval(r2 + op2 + v2, {}, R):
        R[r1] += (1 if op1 == "inc" else -1) * int(v1)
    max_val = max(max(R.values()), max_val)

print(max(R.values()))
print(max_val)
