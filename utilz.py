def gridConversion(fileName):
    newList = []
    endpointCells = {}
    with open(f"{fileName}.txt", 'r') as myFile:
        lines = myFile.readlines()
        lines = [line.strip() for line in lines] 
        
        for i in range(len(lines)):
            temp_List = []
            for j in range(len(lines[i])):
                temp_tuple = (i, j)
                temp_List.append(temp_tuple)

                if lines[i][j] != '.':  # If the cell is not a dot
                    # If the key doesn't exist, initialize it with a list
                    if lines[i][j] not in endpointCells:
                        endpointCells[lines[i][j]] = []
                    # Append the tuple (i, j) to the list for that key
                    endpointCells[lines[i][j]].append((i, j))

            newList.append(temp_List)
    
    return newList, endpointCells

def connections(coordinate, grid):
    posList = []
    # gives all of the possible connection cells from the given coordinate
    row = coordinate[0]
    col = coordinate[1]
    
    # Check boundaries and add valid adjacent cells
    if row > 0:  # Check up
        posList.append((row - 1, col))
    if row < len(grid) - 1:  # Check down
        posList.append((row + 1, col))
    if col > 0:  # Check left
        posList.append((row, col - 1))
    if col < len(grid[0]) - 1:  # Check right
        posList.append((row, col + 1))
    
    return posList

def gridToOneDimension(grid):
    oneDList = []
    for row in grid:
        for cell in row:
            oneDList.append(cell)
    return oneDList

def gridCellProperties(cellsList):
    myDict = {}
    for i in cellsList:
        myDict[cellsList] = {}
    #checks if the coordinate (cell) given has at most one connection.

def check_single_source_constraint(grid):
    """
    Ensures that each cell in the grid has only one 'parent' cell, i.e., 
    it comes from at most one other place of the same color.
    
    Parameters:
    - grid: 2D list representing the puzzle grid where each cell has either 
      None (no color) or a color identifier.
      
    Returns:
    - A Boolean indicating if the grid satisfies the 'single source' constraint.
    """
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            color = grid[i][j]
            if color is not None:  # If cell has a color, check neighbors
                neighbors = connections((i, j), grid)  # Use connections function
                sources = [n for n in neighbors if grid[n[0]][n[1]] == color]
                
                # Constraint: there should be at most one source
                if len(sources) > 1:
                    return False  # Constraint violated
    return True  # All cells satisfy the constraint

class MyCell:
    def __init__(self, coordinate, connectedTo, color, endpoint):
        self.coordinate = coordinate
        self.connectedTo = connectedTo
        self.color = color 
        self.endpoint = endpoint
    

cell1 = MyCell((1,2), (2,2), "Blue", True)
print(cell1.coordinate)
## for each of the new coordinates for the grid 

# Example usage:
try:
    grid, endpoints = gridConversion("example")
    print("Grid:", grid)
    print("Endpoints:", endpoints)
    
    # Test connections
    test_coord = (1, 2)
    if len(grid) > test_coord[0] and len(grid[0]) > test_coord[1]:
        connected_cells = connections(test_coord, grid)
        print(f"Connected cells to {test_coord}:", connected_cells)
    else:
        print("Test coordinates out of grid bounds")
        
except FileNotFoundError:
    print("File 'example.txt' not found")
except Exception as e:
    print(f"An error occurred: {e}")