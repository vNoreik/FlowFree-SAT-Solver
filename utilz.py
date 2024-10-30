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