# flow_free.py
from bauhaus import Encoding, proposition, constraint, And, Or
from bauhaus.utils import count_solutions, likelihood
from nnf import config
config.sat_backend = "kissat"

@proposition
class CellConnection:
    def __init__(self, x1, y1, x2, y2, color):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.color = color
    
    def __repr__(self):
        return f"{self.color}: ({self.x1},{self.y1}) -> ({self.x2},{self.y2})"

class FlowFree:
    def __init__(self, filename):
        self.E = Encoding()
        self.grid, self.colors, self.size = self._read_input(filename)
        self.connections = self._create_propositions()
    
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
    
    def _create_propositions(self):
        connections = []
        # Create possible connections between adjacent cells
        for i in range(self.size):
            for j in range(self.size):
                # Horizontal connections
                if j < self.size - 1:
                    for color in self.colors:
                        connections.append(CellConnection(i, j, i, j+1, color))
                # Vertical connections
                if i < self.size - 1:
                    for color in self.colors:
                        connections.append(CellConnection(i, j, i+1, j, color))
        return connections

def encode(self):
    # 1. Each cell must be used exactly once
    for i in range(self.size):
        for j in range(self.size):
            self.E.add_constraint(ExactlyOne([conn for conn in self.connections 
                if (conn.x1 == i and conn.y1 == j) or (conn.x2 == i and conn.y2 == j)]))

    # 2. Each colored endpoint connects to one matching-color neighbor
    for i in range(self.size):
        for j in range(self.size):
            if self.grid[i][j] != '.':
                color = self.grid[i][j]
                self.E.add_constraint(ExactlyOne([conn for conn in self.connections 
                    if conn.color == color and 
                    ((conn.x1 == i and conn.y1 == j) or (conn.x2 == i and conn.y2 == j))]))

    # 3. Intermediate cells connect to exactly two cells of same color
    for i in range(self.size):
        for j in range(self.size):
            if self.grid[i][j] == '.':
                for color in self.colors:
                    # For each color, either 0 or 2 connections
                    connected_cells = [conn for conn in self.connections 
                        if conn.color == color and 
                        ((conn.x1 == i and conn.y1 == j) or (conn.x2 == i and conn.y2 == j))]
                    self.E.add_constraint(Or(
                        And([Not(conn.active) for conn in connected_cells]),
                        ExactlyTwo(connected_cells)
                    ))

    # 4. Path continuity with color matching
    for conn in self.connections:
        color = conn.color
        # If connection is active, ensure continuation at both ends
        self.E.add_constraint(Implies(conn.active, And(
            Or([other.active for other in self.connections 
                if other != conn and other.color == color and
                ((other.x1 == conn.x2 and other.y1 == conn.y2) or 
                 (other.x2 == conn.x2 and other.y2 == conn.y2))]),
            Or([other.active for other in self.connections 
                if other != conn and other.color == color and
                ((other.x1 == conn.x1 and other.y1 == conn.y1) or 
                 (other.x2 == conn.x1 and other.y2 == conn.y1))])
        )))

    # 5. No shared cells between different colors
    for i in range(self.size):
        for j in range(self.size):
            for color1 in self.colors:
                for color2 in self.colors:
                    if color1 != color2:
                        conns1 = [conn for conn in self.connections 
                            if conn.color == color1 and 
                            ((conn.x1 == i and conn.y1 == j) or (conn.x2 == i and conn.y2 == j))]
                        conns2 = [conn for conn in self.connections 
                            if conn.color == color2 and 
                            ((conn.x1 == i and conn.y1 == j) or (conn.x2 == i and conn.y2 == j))]
                        for c1 in conns1:
                            for c2 in conns2:
                                self.E.add_constraint(Not(And(c1.active, c2.active)))

    def solve(self):
        theory = self.E.compile()
        solution = theory.solve()
        if solution:
            return self._extract_paths(solution)
        return None

    def _extract_paths(self, solution):
        # Extract and format paths from the solution
        paths = {}
        for conn in solution:
            if solution[conn]:
                color = conn.color
                if color not in paths:
                    paths[color] = []
                paths[color].append((conn.x1, conn.y1, conn.x2, conn.y2))
        return paths