import itertools
import math
import functools

def print_grid(g):
    for l in g:
        print(l)

def tuple_sub(a, b):
    return (a[0]-b[0], a[1]-b[1])

def tuple_add(a, b):
    return (a[0]+b[0], a[1]+b[1])

def check_valid(coord, grid):
    return 0 <= coord[0] < len(grid) and 0 <= coord[1] < len(grid[0])

@functools.lru_cache(maxsize=1000, typed=False)
def blink(arr):
    new_arr = []

    for a in arr:
        if a == 0:
            new_arr.append(1)
        elif len(s_a := str(a)) % 2 == 0:
            new_arr.append(int(s_a[:len(s_a)//2]))
            new_arr.append(int(s_a[len(s_a)//2:]))
        else:
            new_arr.append(a*2024)

    return new_arr

@functools.lru_cache(maxsize=10000, typed=False)
def solve(a, times):
    if times == 0:
        return 1

    if a == 0:
        return solve(1, times - 1)
    elif len(s_a := str(a)) % 2 == 0:
        return solve(int(s_a[:len(s_a)//2]), times - 1) + solve(int(s_a[len(s_a)//2:]), times - 1)
    else:
        return solve(a*2024, times - 1)
        

ori = [8069, 87014, 98, 809367, 525, 0, 9494914, 5]
tot = 0

for n in ori:
    tot += solve(n, 75)

# for a in ori:
#     n = [a]
#     for _ in range(75):
#         n = blink(n)

print(tot)