import unittest
import os
from flow_free import FlowFree

class TestFlowFree(unittest.TestCase):
    def setUp(self):
        self.test_files = {}
        self._create_test_files()
        
    def tearDown(self):
        self._cleanup_test_files()

    def test_2x2_simple(self):
        """Test simplest possible puzzle - 2x2 with one color"""
        solver = FlowFree(self.test_files['2x2'])
        solution = solver.solve()
        self.assertIsNotNone(solution)
        self.assertIn('R', solution)
        self.assertEqual(len(solution['R']), 1)  # One connection

    def test_3x3_two_colors(self):
        """Test 3x3 puzzle with two colors"""
        solver = FlowFree(self.test_files['3x3'])
        solution = solver.solve()
        self.assertIsNotNone(solution)
        self.assertIn('R', solution)
        self.assertIn('B', solution)
        self._verify_path_continuity(solution)

    def test_invalid_puzzle(self):
        """Test puzzle with impossible solution"""
        solver = FlowFree(self.test_files['invalid'])
        solution = solver.solve()
        self.assertIsNone(solution)

    def _verify_path_continuity(self, solution):
        """Verify that paths are continuous"""
        for color, path in solution.items():
            connections = set()
            for x1, y1, x2, y2 in path:
                connections.add((x1, y1))
                connections.add((x2, y2))
                # Verify connections are adjacent
                self.assertTrue(abs(x1 - x2) + abs(y1 - y2) == 1)

    def _create_test_files(self):
        test_cases = {
            '2x2': ["R.",
                   ".R"],
            '3x3': ["R.B",
                   "...",
                   "B.R"],
            'invalid': ["RB",
                       "BR"]  # Impossible to connect without crossing
        }
        
        for name, grid in test_cases.items():
            filename = f"test_{name}.txt"
            with open(filename, "w") as f:
                f.write("\n".join(grid))
            self.test_files[name] = filename

    def _cleanup_test_files(self):
        for filename in self.test_files.values():
            if os.path.exists(filename):
                os.remove(filename)

    def _print_solution(self, grid_size, solution):
        """Helper to visualize solution"""
        grid = [['.' for _ in range(grid_size)] for _ in range(grid_size)]
        for color, path in solution.items():
            for x1, y1, x2, y2 in path:
                grid[x1][y1] = color
                grid[x2][y2] = color
        for row in grid:
            print(' '.join(row))

if __name__ == '__main__':
    unittest.main(verbosity=2)