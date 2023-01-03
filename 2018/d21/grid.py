R = [1, 21, False, 65536, 11469373, 0]

R[1] = R[1] + R[2]
print(R)
R[1] += 1
print(R)
R[5] += 1
print(R)
R[1] = 17
print(R)
R[1] = R[5] + 2
print(R)
R[2] *= 256
print(R)
