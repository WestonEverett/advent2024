from collections import Counter

with open(r"C:\Users\westo\advent2024\day_1\data.txt") as file:
    lines = [l for l in file]

l_1 = []
l_2 = []
for l in lines:
    a,b = l.split()
    l_1.append(int(a))
    l_2.append(int(b))

l_1.sort()
l_2.sort()

tot = 0
for a,b in zip(l_1, l_2):
    tot += abs(a-b)

c_s = Counter(l_2)

tot_2 = 0
for a in l_1:
    tot_2 += a * c_s.get(a,0)

print(tot_2)