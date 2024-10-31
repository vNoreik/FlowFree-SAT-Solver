# test_solver.py
from run import FlowSolver
import unittest

class TestFlowSolver(unittest.TestCase):
    def test_simple_2x2(self):
        # Simple 2x2 grid with one path
        grid = [
            ['R', '.'],
            ['.', 'R']
        ]
        solver = FlowSolver(grid)
        result = solver.solve()
        self.assertTrue(result)  # Should be solvable
        self.verify_solution(grid, solver.get_solution())

    def test_simple_3x3(self):
        # 3x3 grid with two colors
        grid = [
            ['R', '.', 'B'],
            ['.', '.', '.'],
            ['B', '.', 'R']
        ]
        solver = FlowSolver(grid)
        result = solver.solve()
        self.assertTrue(result)
        self.verify_solution(grid, solver.get_solution())

    def verify_solution(self, grid, solution):
        size = len(grid)
        # Check all endpoints are connected
        for i in range(size):
            for j in range(size):
                if grid[i][j] != '.':
                    # Should have exactly one connection
                    connected = False
                    color = grid[i][j]
                    for conn in solution:
                        if conn.color == color and (
                            (conn.x1 == i and conn.y1 == j) or 
                            (conn.x2 == i and conn.y2 == j)):
                            connected = True
                    self.assertTrue(connected, f"Endpoint at {i},{j} not connected")

        # Check path continuity
        for i in range(size):
            for j in range(size):
                conns = [c for c in solution if 
                    (c.x1 == i and c.y1 == j) or 
                    (c.x2 == i and c.y2 == j)]
                if grid[i][j] == '.':
                    # Should have 0 or 2 connections of same color
                    colors = set(c.color for c in conns)
                    for color in colors:
                        color_conns = [c for c in conns if c.color == color]
                        self.assertTrue(len(color_conns) in [0, 2])
                else:
                    # Should have exactly 1 connection
                    self.assertEqual(len(conns), 1)

def print_solution(grid, solution):
    """Helper to visualize solution"""
    size = len(grid)
    for i in range(size):
        for j in range(size):
            cell = grid[i][j]
            conns = [c for c in solution if 
                (c.x1 == i and c.y1 == j) or 
                (c.x2 == i and c.y2 == j)]
            if conns:
                print(f"{cell or conns[0].color}", end=' ')
            else:
                print('.', end=' ')
        print()

if __name__ == '__main__':
    unittest.main()