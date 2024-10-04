# https://www.codewars.com/kata/52423db9add6f6fc39000354
# Given a 2D array and a number of generations, compute n timesteps of Conway's Game of Life.

# The rules of the game are:

# Any live cell with fewer than two live neighbours dies, as if caused by underpopulation.
# Any live cell with more than three live neighbours dies, as if by overcrowding.
# Any live cell with two or three live neighbours lives on to the next generation.
# Any dead cell with exactly three live neighbours becomes a live cell.

# Each cell's neighborhood is the 8 cells immediately around it (i.e. Moore Neighborhood). 
# The universe is infinite in both the x and y dimensions and all cells are initially dead - 
# except for those specified in the arguments. The return value should be a 2d array cropped 
# around all of the living cells. (If there are no living cells, then return [[]].)

# For illustration purposes, 0 and 1 will be represented as ░░ and ▓▓ blocks respectively 
# (PHP: plain black and white squares). You can take advantage of the htmlize function 
# to get a text representation of the universe, e.g.:

class AdaptedArray():
    def __init__(self,array):
        self.array = array

    def __str__(self):
        values = ''
        for i in self.array:
            for j in i:
                if j == 1:
                    values += '▓▓'
                else:
                    values += '░░'
            values += '\n'
        return values

from copy import deepcopy
import numpy as np

def get_generation(cells : list[list[int]],generations : int) -> list[list[int]]:
    for _ in range(generations):
        cells = np.array(cells)
        rows = len(cells)
        cols = len(cells[0])
        next_gen = np.pad(cells,((1, 1), (1, 1)),'constant',constant_values=0)
        for i in range(-1,len(next_gen)-1):
            for j in range(-1,len(next_gen[0])-1):
                
                numpylist = cells[max(0,i-1):min(rows,i+2) , max(0,j-1):min(cols,j + 2)]
                count = sum(sum(numpylist)) - next_gen[i+1][j+1]

                if count != 3:
                    if count != 2:
                        next_gen[i+1][j+1] = 0
                else:
                    next_gen[i+1][j+1] = 1

        while sum(next_gen[0]) == 0:
            next_gen = next_gen[1:]
        while sum([i[0] for i in next_gen]) == 0:
            next_gen = next_gen[:, 1:]
        while sum(next_gen[len(next_gen)-1]) == 0:
            next_gen = next_gen[:-1]
        while sum([i[len(next_gen[0])-1] for i in next_gen]) == 0:
            next_gen = next_gen[:, :len(next_gen[0])-1]

        cells = deepcopy(next_gen)

    return cells if type(cells) == list else cells.tolist()



def get_sum(lst,j):
    return sum([i[j] for i in lst])

def without_column(lst,j):
    return [row[:j] + row[j+1:] for row in lst]

def get_generationyd(cells : list[list[int]],generations : int) -> list[list[int]]:
    for _ in range(generations):
        next_gen = deepcopy(cells)
        zeros = [0 for _ in range(len(next_gen[0]))]
        next_gen.insert(0,zeros.copy())
        next_gen.append(zeros.copy())

        for row in next_gen:
            row.insert(0,0)
            row.append(0)

        for i in range(-1,len(next_gen)-1):
            above = i - 1
            below = i + 1
            for j in range(-1,len(next_gen[0])-1):
                
                count = 0

                for idx in range(-1,2,1):
                    aux = j + idx
                    if aux >= 0 and aux < len(cells[0]):
                        if above >= 0:
                            count += cells[above][aux]
                        if below < len(cells):
                            count += cells[below][aux]
                        if aux != j and i >= 0 and i < len(cells): 
                            count += cells[i][aux]

                if count != 3:
                    if count != 2:
                        next_gen[i+1][j+1] = 0
                else:
                    next_gen[i+1][j+1] = 1


        while sum(next_gen[0]) == 0:
            next_gen = next_gen[1:]
        while sum(next_gen[len(next_gen)-1]) == 0:
            next_gen = next_gen[:-1]
        while sum([i[0] for i in next_gen]) == 0:
            next_gen = without_column(next_gen,0)
        while sum([i[len(next_gen[0])-1] for i in next_gen]) == 0:
            next_gen = without_column(next_gen,len(next_gen[0])-1)

        cells = deepcopy(next_gen)

    return cells


if __name__ == '__main__':
    au = [[1,0,0],
          [0,1,1],
          [1,1,0]]
    
    aux = get_generationyd([[1,1,1,0,0,0,1,0],
            [1,0,0,0,0,0,0,1],
            [0,1,0,0,0,1,1,1]
        ], 16)
    
    for it in aux:
       print(it)
    print([[0,0,0],[0,1,0],[0,0,0]].count([0,0,0]))