with open(r"day_4\data.txt") as file:
    lines = [l.strip() for l in file]

def is_valid(i,j,grid):
    if not (0 <= i < len(grid)):
        return False
    if not (0 <= j < len(grid[0])):
        return False
    return True

def check(i,j, dir_i, dir_j, grid, s_word):
    end_i = i + (dir_i * (len(s_word) - 1))
    end_j = j + (dir_j * (len(s_word) - 1))

    if not is_valid(i,j,grid) or not is_valid(end_i, end_j, grid):
        return False
        
    for d in range(len(s_word)):
        if grid[i+(d*dir_i)][j+(d*dir_j)] != s_word[d]:
            return False
    return True

def project(i,j, grid):
    if grid[i][j] != "A":
        return 0
    
    base = "MMSS"
    locs = [(-1,-1),(1,-1),(1,1),(-1,1)]

    tot = 0
    for x in range(len(base)):    
        ind_count = 0
        for loc, val in zip(locs, base[x:] + base[:x]):
            if is_valid(i+loc[0], j+loc[1], grid) and grid[i+loc[0]][j+loc[1]] == val:
                ind_count += 1
        if ind_count == 4:
            tot += 1

    
    return tot


# tot = 0
# for r in range(len(lines)):
#     for c in range(len(lines[0])):
#         for dir_i, dir_j in [(0,1), (1,1), (1,0), (1,-1), (0,-1), (-1,-1), (-1,0), (-1,1)]:
#             if check(r,c,dir_i,dir_j,lines,"XMAS"):
#                 tot+=1

# lines = [
#     "MDM",
#     "CAC",
#     "SAS"
# ]

tot = 0
for r in range(len(lines)):
    for c in range(len(lines[0])):
        tot += project(r,c,lines)
print(tot)
