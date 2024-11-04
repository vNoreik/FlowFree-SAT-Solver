from bauhaus import Encoding, proposition, constraint
from nnf import Var

from example import example2

cells = []
endpoints = []

e = Encoding()


def gridTranslate(grid):
    mydict = {}    
    for row in grid:
        for cell in row:
            if len(cell) == 3:
                color = cell[2]
                if color in mydict:
                    endpoints.append(endpoint(mydict[color], e_cell(cell[0], cell[1]), color))
                else:
                    mydict[color] = e_cell(cell[0], cell[1])
            cells.append(e_cell(cell[0], cell[1]))
                
@proposition(e)
class endpoint(object):
    def __init__(self, cell_1, cell_2, color) -> None:
            self.cell_1 = cell_1
            self.cell_2 = cell_2
            self.color = color
    def _prop_name(self):
         return f"{self.color}: {self.cell_1} -> {self.cell_2}"


@proposition(e)
class e_cell(object):
    def __init__(self, x, y) -> None:
            self.x = x
            self.y = y
    def _prop_name(self):
         return f"{self.x , self.y}"


gridTranslate(example2)
print(cells, endpoints)