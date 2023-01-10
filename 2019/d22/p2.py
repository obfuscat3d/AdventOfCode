"""
Definitely borrowed some ideas from the solutions mega thread :(
"""

L = 119315717514047
N = 101741582076661

a, b = 1, 0
for ins in open('input').read().split('\n')[::-1]:
    if "stack" in ins:
        a, b = -1 * a, -b - 1
    elif "increment" in ins:
        n = int(ins.split()[-1])
        p = pow(n, L - 2, L)
        a, b = a * p, b * p
    elif "cut" in ins:
        n = int(ins.split()[-1])
        b += n
    a, b = a % L, b % L

q1 = pow(a, N, L) * 2020
q2 = b * (pow(a, N, L) + L - 1) * pow(a - 1, L - 2, L)
print((q1 + q2) % L)
