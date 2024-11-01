import sys
from flow_free import FlowFree

def main():
    if len(sys.argv) != 2:
        print("Usage: python test.py <input_file>")
        sys.exit(1)
    
    puzzle = FlowFree(sys.argv[1])
    puzzle.encode()
    solution = puzzle.solve()
    
    if solution:
        for color, path in solution.items():
            print(f"Path for color {color}:")
            print(path)
    else:
        print("No solution exists")

if __name__ == "__main__":
    main()