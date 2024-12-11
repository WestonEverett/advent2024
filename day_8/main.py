import itertools
import math

with open(r"day_8\data.txt") as file:
    lines = [list(l.strip()) for l in file] 

loc_map = []

def get_ant(grid):
    ants = {}

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (v := grid[i][j]) != ".":
                ants[v] = ants.get(v, []) + [(i,j)]
    
    return ants

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def check_valid(coord, grid):
    return 0 <= coord[0] < len(grid) and 0 <= coord[1] < len(grid[0])

def simple_tup(tup):
    gcd = abs(math.gcd(tup[0], tup[1]))
    return (tup[0]//gcd, tup[1]//gcd)

def get_diffs(coords,grid):
    diffs = set()
    for subset in itertools.combinations(coords, 2):
        diff = simple_tup(tuple_sub(subset[0], subset[1]))
        val = subset[0]
        while check_valid(val, grid):
            diffs.add(val)
            val = tuple_add(val, diff)

        diff = simple_tup(tuple_sub((0,0), diff))
        val = subset[1]
        while check_valid(val, grid):
            diffs.add(val)
            val = tuple_add(val, diff)
    
    return diffs

a = get_ant(lines)
a_n = {d for diff_d in a.values() for d in get_diffs(diff_d, lines) if check_valid(d, lines)}

with open(r"day_8\dt.txt") as file:
    t = [list(l.strip()) for l in file] 

for l in lines:
    print(l)

print()

for i, j in a_n:
    lines[i][j] = "#"

for l in lines:
    print(l)
print()
for l in t:
    print(l)


print(len(a_n))