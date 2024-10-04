# https://www.codewars.com/kata/534e01fbbb17187c7e0000c6
# Your task, is to create a NxN spiral with a given size.

# For example, spiral with size 5 should look like this:

# 00000
# ....0
# 000.0
# 0...0
# 00000
# and with the size 10:

# 0000000000
# .........0
# 00000000.0
# 0......0.0
# 0.0000.0.0
# 0.0..0.0.0
# 0.0....0.0
# 0.000000.0
# 0........0
# 0000000000
# Return value should contain array of arrays, of 0 and 1, with the first row being composed of 1s. For example for given size 5 result should be:

# [[1,1,1,1,1],[0,0,0,0,1],[1,1,1,0,1],[1,0,0,0,1],[1,1,1,1,1]]
# Because of the edge-cases for tiny spirals, the size will be at least 5.

# General rule-of-a-thumb is, that the snake made with '1' cannot touch to itself.

from gameoflife import AdaptedArray

dictaux = {
    'right' : lambda y,x,z: [y,min(x+1,z)],
    'down' : lambda y,x,z: [min(y+1,z),x],
    'left' : lambda y,x,z: [y,max(0,x-1)],
    'up' : lambda y,x,z : [max(0,y-1),x]
}
order = ['right','down','left','up']

def spiralize(size : int) -> list[list[int]]:

    spiral = [[0 for j in range(size)] for i in range(size)]
    actual_i, actual_j, last_i, last_j, direction, verifi = [0,0,0,0,0,True]
    while verifi:
        verifi, next_i, next_j = continuee(spiral,actual_i,actual_j,direction)

        if not verifi:
            actual_i,actual_j,direction = change_direction(last_i,last_j,direction,size)
            verifi,next_i,next_j = continuee(spiral,actual_i,actual_j,direction)

        if verifi:
            spiral[actual_i][actual_j] = 1
        else:
            return spiral

        last_i = actual_i
        last_j = actual_j
        actual_i = next_i
        actual_j = next_j

def change_direction(i : int,j : int,direction : int ,size: int) -> list[int]:
    direction = direction + 1 if direction < 3 else 0
    actual_i,actual_j = dictaux[order[direction]](i,j,size-1)
    return [actual_i,actual_j,direction]


def continuee(spiral : list[list[int]],index_i : int, index_j :int,going:int) -> list[bool,int,int]:

    i_90,j_90 = dictaux[order[going]](index_i,index_j,len(spiral)-1)
    i_180,j_180 = dictaux[order[going + 1 if going < 3 else 0]](i_90,j_90,len(spiral)-1)

    res = spiral[i_90][j_90] + spiral[i_180][j_180] + 1

    if res == 1:
        return True, i_90, j_90

    return False, -1, -1


if __name__ == '__main__':
    size = 10
    print(f"\nspiralize size: {size}")
    aux = AdaptedArray(spiralize(size))
    print(aux)
