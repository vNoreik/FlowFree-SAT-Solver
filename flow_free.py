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
    
    def _find_endpoints(self):
        endpoints = {}
        for color in self.colors:
            endpoints[color] = []
            for i in range(self.size):
                for j in range(self.size):
                    if self.grid[i][j] == color:
                        endpoints[color].append((i, j))
        return endpoints

    def _create_propositions(self):
        connections = []
        # Create possible connections between adjacent cells
        for i in range(self.size):
            for j in range(self.size):
                # Horizontal connections
                if j < self.size - 1:
                    for color in self.colors:
                        connections.append(CellConnection(i, j, i, j+1, color))
                        connections.append(CellConnection(i, j+1, i, j, color))
                # Vertical connections
                if i < self.size - 1:
                    for color in self.colors:
                        connections.append(CellConnection(i, j, i+1, j, color))
                        connections.append(CellConnection(i+1, j, i, j, color))
        return connections

    def _get_connections_for_cell(self, x, y):
        return [conn for conn in self.connections 
                if (conn.x1 == x and conn.y1 == y) or (conn.x2 == x and conn.y2 == y)]

    def encode(self):
        # 1. Each cell must be used exactly once
        for i in range(self.size):
            for j in range(self.size):
                cell_connections = self._get_connections_for_cell(i, j)
                constraint.add_exactly_one(self.E, cell_connections)

        # 2. Colored endpoints must connect to exactly one neighbor
        for color, endpoints in self.color_endpoints.items():
            for x, y in endpoints:
                # Get all possible connections for this endpoint of this color
                endpoint_connections = [conn for conn in self._get_connections_for_cell(x, y)
                                     if conn.color == color]
                constraint.add_exactly_one(self.E, endpoint_connections)
                
                # Forbid connections of other colors
                other_color_connections = [conn for conn in self._get_connections_for_cell(x, y)
                                        if conn.color != color]
                for conn in other_color_connections:
                    self.E.add_constraint(~conn)

        # 3. Non-endpoint cells must connect to exactly two neighbors
        for i in range(self.size):
            for j in range(self.size):
                if self.grid[i][j] == '.':  # Non-endpoint cell
                    cell_connections = self._get_connections_for_cell(i, j)
                    # Group connections by color
                    for color in self.colors:
                        color_connections = [conn for conn in cell_connections 
                                          if conn.color == color]
                        # If this cell is used by this color, it must have exactly two connections
                        if color_connections:
                            constraint.add_exactly_k(self.E, color_connections, 2)

        # 4. Paths must be continuous
        for color in self.colors:
            start, end = self.color_endpoints[color]
            # For each intermediate cell
            for i in range(self.size):
                for j in range(self.size):
                    if (i,j) != start and (i,j) != end:
                        incoming = [conn for conn in self.connections 
                                  if conn.color == color and (conn.x2,conn.y2) == (i,j)]
                        outgoing = [conn for conn in self.connections 
                                  if conn.color == color and (conn.x1,conn.y1) == (i,j)]
                        
                        # If there's an incoming connection, there must be an outgoing one
                        for inc in incoming:
                            self.E.add_constraint(inc >> Or(outgoing))

        # 5. Paths cannot cross
        for i in range(self.size):
            for j in range(self.size):
                # For each cell, ensure only one color can use it
                for color1 in self.colors:
                    for color2 in self.colors:
                        if color1 < color2:  # Avoid duplicate constraints
                            color1_conns = [conn for conn in self._get_connections_for_cell(i, j)
                                          if conn.color == color1]
                            color2_conns = [conn for conn in self._get_connections_for_cell(i, j)
                                          if conn.color == color2]
                            for c1 in color1_conns:
                                for c2 in color2_conns:
                                    self.E.add_constraint(~(c1 & c2))

    def solve(self):
        theory = self.E.compile()
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
                paths[color].append((conn.x1, conn.y1, conn.x2, conn.y2))
        return paths