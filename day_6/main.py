import copy


with open(r"day_6\data.txt") as file:
    lines = [list(l.strip()) for l in file]

turn_map = {
    (-1,0) : (0,1),
    (0,1): (1,0),
    (1,0): (0,-1),
    (0,-1): (-1,0)
}

dir_map = {
    "<" : (0,-1),
    "v": (1,0),
    ">": (0,1),
    "^": (-1,0)
}

char_map = {
    (0,-1):"<",
    (1,0):"v" ,
    (0,1):">",
    (-1,0):"^" 
}

def next_step(c,d,grid):
    pot = (c[0] + d[0], c[1] + d[1])

    if not (0 <= pot[0] < len(grid) and 0 <= pot[1] < len(grid)):
        return (-1,-1), d
    
    if grid[pot[0]][pot[1]] == "#":
        return c, turn_map[d]
    else:
        return pot, d

def find_cur(grid):
    for i in range(len(grid)):
        for j in range(len(grid)):
            if grid[i][j] in "><v^":
                return ((i,j), dir_map[grid[i][j]])
            
def explore(old_grid):
    grid = copy.deepcopy(old_grid)
    c_loc = find_cur(grid)
    while True:
        n_loc = next_step(c_loc[0], c_loc[1], grid)     

        if n_loc[0] == (-1,-1):
            return grid, False
            
        if grid[n_loc[0][0]][n_loc[0][1]] != ".":
            if char_map[n_loc[1]] in grid[n_loc[0][0]][n_loc[0][1]]:
                return grid, True
            else:
                grid[n_loc[0][0]][n_loc[0][1]] += char_map[n_loc[1]]
        else: 
            grid[n_loc[0][0]][n_loc[0][1]] = char_map[n_loc[1]]

        #  grid[n_loc[0][0]][n_loc[0][1]] = char_map[n_loc[1]]

        # for line in grid:
        #     print(line)
        c_loc = n_loc

def nice_print(lines):
    for l in lines:
        print(l)

tot = 0
base_grid = explore(lines)[0]
start = find_cur(lines)[0]

for i in range(len(lines)):
    for j in range(len(lines[0])):
        if base_grid[i][j][0] in "<>v^" and (i,j) != start:
            g = copy.deepcopy(lines)
            g[i][j] = "#"
            if (x:=explore(g))[1]:
                tot += 1

print(tot)


        
        

