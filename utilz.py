def gridConversion(fileName):
    newList = []
    endpointCells = {}
    with open(f"{fileName}.txt", 'r') as myFile:
        lines = myFile.readlines()
        lines = [line.strip() for line in lines]  # Remove newline characters
        print(lines)
        
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

x = gridConversion('example')
print(x)