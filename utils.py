
def parse_grid(filename):
    """Read and validate the input grid."""
    with open(filename) as f:
        return [list(line.strip()) for line in f]

def get_adjacent_cells(x, y, size):
    """Get all adjacent cells within grid bounds."""
    adjacent = []
    for dx, dy in [(0,1), (1,0), (0,-1), (-1,0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < size and 0 <= new_y < size:
            adjacent.append((new_x, new_y))
    return adjacent