# Python program for A* Search Algorithm
import math
import heapq
import attrs
import typing as tp

@attrs.define
class Coord:
    row: int
    col: int

    def from_diff(self, d_row, d_col):
        return Coord(self.row + d_row, self.col + d_col)

@attrs.define
class Cell:
    parent: tp.Optional[Coord] = None
    f: float = float('inf')
    g: float = float('inf')
    h: float = 0

# Check if a cell is valid (within the grid)


def is_valid(grid, c: Coord):
    return (c.row >= 0) and (c.row < len(grid)) and (c.col >= 0) and (c.col < len(grid[c.row]))

# Check if a cell is unblocked


def is_unblocked(grid, c: Coord):
    return grid[c.row][c.col] == 1

# Check if a cell is the destination


def is_destination(cur: Coord, dest: Coord):
    return cur == dest

# Calculate the heuristic value of a cell (Euclidean distance to destination)


def calculate_h_value(c: Coord, dest: Coord):
    return ((c.row - dest.row) ** 2 + (c.col - dest.col) ** 2) ** 0.5

# Trace the path from source to destination


def trace_path(cell_details: tp.List[tp.List[Cell]], dest: Coord):
    print("The Path is ")
    path = []

    current = dest

    # Trace the path from destination to source using parent cells
    while not (cell_details[current.row][current.col].parent == current):
        path.append(current)
        current = cell_details[current.row][current.col].parent

    # Add the source cell to the path
    path.append(current)
    # Reverse the path to get the path from source to destination
    path.reverse()

    # Print the path
    for i in path:
        print(i)
    print()

# Implement the A* search algorithm


def a_star_search(grid, src: Coord, dest: Coord):
    # Check if the source and destination are valid
    if not is_valid(grid, src) or not is_valid(grid, dest):
        print("Source or destination is invalid")
        return

    # Check if the source and destination are unblocked
    if not is_unblocked(grid, src) or not is_unblocked(grid, dest):
        print("Source or the destination is blocked")
        return

    # Check if we are already at the destination
    if is_destination(src, dest):
        print("We are already at the destination")
        return

    # Initialize the closed list (visited cells)
    closed_list = [[False for _ in range(len(grid[0]))] for _ in range(len(grid))]
    # Initialize the details of each cell
    cell_details = [[Cell() for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # Initialize the start cell details
    cur_coord = src
    cell_details[cur_coord.row][cur_coord.col].f = 0
    cell_details[cur_coord.row][cur_coord.col].g = 0
    cell_details[cur_coord.row][cur_coord.col].h = 0
    cell_details[cur_coord.row][cur_coord.col].parent = cur_coord    

    # Initialize the open list (cells to be visited) with the start cell
    open_list = []
    heapq.heappush(open_list, (0.0, cur_coord))

    # Initialize the flag for whether destination is found
    found_dest = False

    # Main loop of A* search algorithm
    while len(open_list) > 0:
        # Pop the cell with the smallest f value from the open list
        p = heapq.heappop(open_list)

        coord: Coord = p[1]

        # Mark the cell as visited
        closed_list[coord.row][coord.col] = True

        # For each direction, check the successors
        directions = [(0, 1), (0, -1), (1, 0), (-1, 0),
                      (1, 1), (1, -1), (-1, 1), (-1, -1)]
        for dir in directions:
            new_c = coord.from_diff(dir[0], dir[1])

            # If the successor is valid, unblocked, and not visited
            if is_valid(grid, new_c) and is_unblocked(grid, new_c) and not closed_list[new_c.row][new_c.col]:
                # If the successor is the destination
                if is_destination(new_c, dest):
                    # Set the parent of the destination cell
                    cell_details[new_c.row][new_c.col].parent = coord
                    print("The destination cell is found")
                    # Trace and print the path from source to destination
                    trace_path(cell_details, dest)
                    found_dest = True
                    return
                else:
                    # Calculate the new f, g, and h values
                    g_new = cell_details[coord.row][coord.col].g + 1.0
                    h_new = calculate_h_value(new_c, dest)
                    f_new = g_new + h_new

                    # If the cell is not in the open list or the new f value is smaller
                    if cell_details[new_c.row][new_c.col].f == float('inf') or cell_details[new_c.row][new_c.col].f > f_new:
                        # Add the cell to the open list
                        heapq.heappush(open_list, (f_new, new_c))
                        # Update the cell details
                        cell_details[new_c.row][new_c.col].f = f_new
                        cell_details[new_c.row][new_c.col].g = g_new
                        cell_details[new_c.row][new_c.col].h = h_new
                        cell_details[new_c.row][new_c.col].parent = coord

    # If the destination is not found after visiting all cells
    if not found_dest:
        print("Failed to find the destination cell")

# Driver Code


def main():
    # Define the grid (1 for unblocked, 0 for blocked)
    grid = [
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 1],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1, 0, 1, 0],
        [1, 0, 1, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 0, 1, 1, 1],
        [1, 1, 1, 0, 0, 0, 1, 0, 0, 1]
    ]

    # Define the source and destination
    src = Coord(8,9)
    dest = Coord(0,0)

    # Run the A* search algorithm
    a_star_search(grid, src, dest)

main()