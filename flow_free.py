import pprint

from bauhaus import Encoding, proposition, constraint
from bauhaus.utils import count_solutions, likelihood
from nnf import config
config.sat_backend = "kissat"

# Create global encoding
E = Encoding()

@proposition(E)
class Cell(object):
    def __init__(self, x, y, color=None):
        self.x = x
        self.y = y
        self.color = color

    def _prop_name(self):
        return f"Cell({x},{y},{color})"


@proposition(E)
class Connection(object):
    def __init__(self, cell1, cell2, color):
        self.cell1 = cell1
        self.cell2 = cell2
        self.color = color
    
    def _prop_name(self):
        return f"Connection({cell1}->{cell2}, {color})"

class FlowFree:
    def __init__(self, filename):
        self.encoding = E
        self.grid, self.colors, self.size = self._read_input(filename)
        self.cells = self._create_cells()
        self.connections = self._create_connections()
        self.color_endpoints = self._find_endpoints()

    def _read_input(self, filename):
        grid = []
        colors = set()
        with open(filename) as f:
            for line in f:
                grid.append(list(line.strip()))
        
        for row in grid:
            for cell in row:
                if cell != '.':
                    colors.add(cell)
        
        return grid, colors, len(grid)

    def _create_cells(self):
        cells = {}
        for i in range(self.size):
            for j in range(self.size):
                color = self.grid[i][j] if self.grid[i][j] != '.' else None
                cells[(i,j)] = Cell(i, j, color)
        return cells

    def _create_connections(self):
        connections = []
        for i in range(self.size):
            for j in range(self.size):
                # Check adjacent cells (right and down only to avoid duplicates)
                if j < self.size - 1:  # right
                    for color in self.colors:
                        connections.append(Connection(
                            self.cells[(i,j)],
                            self.cells[(i,j+1)],
                            color
                        ))
                if i < self.size - 1:  # down
                    for color in self.colors:
                        connections.append(Connection(
                            self.cells[(i,j)],
                            self.cells[(i+1,j)],
                            color
                        ))
        return connections

    def _find_endpoints(self):
        endpoints = {}
        for color in self.colors:
            endpoints[color] = []
            for i in range(self.size):
                for j in range(self.size):
                    if self.grid[i][j] == color:
                        endpoints[color].append(self.cells[(i,j)])
        return endpoints

    def encode(self):
        # CONSTRAINTS:

        # 1. Each cell must be used exactly once

        # 2. Colored endpoints must connect to exactly one neighbor

        # 3. Non-endpoint cells must connect to exactly two neighbors

        # 4. Paths must be continuous

        # 5. Paths cannot cross

        # 7. Grid must be n x n
        pass

    def solve(self):
        theory = self.encoding.compile()
        solution = theory.solve()
        if solution:
            return self._extract_paths(solution)
        return None

    def _extract_paths(self, solution):
        paths = {}
        for conn in self.connections:
            if solution[conn]:
                color = conn.color
                if color not in paths:
                    paths[color] = []
                paths[color].append(
                    (conn.cell1.x, conn.cell1.y, conn.cell2.x, conn.cell2.y)
                )
        return paths