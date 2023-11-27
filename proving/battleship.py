# Write a method that takes a field for well-known board game "Battleship" as an argument and returns true if it has a valid disposition of ships, false otherwise. 
# Argument is guaranteed to be 10*10 two-dimension array. Elements in the array are numbers, 0 if the cell is free and 1 if occupied by ship.

# Battleship (also Battleships or Sea Battle) is a guessing game for two players. Each player has a 10x10 grid containing several "ships" and objective is 
# to destroy enemys forces by targetting individual cells on his field. The ship occupies one or more cells in the grid. Size and number of ships may differ from 
# version to version. In this kata we will use Soviet/Russian version of the game.

# Before the game begins, players set up the board and place the ships accordingly to the following rules:
# There must be single battleship (size of 4 cells), 2 cruisers (size 3), 3 destroyers (size 2) and 4 submarines (size 1).
#  Any additional ships are not allowed, as well as missing ships.
# Each ship must be a straight line, except for submarines, which are just single cell.

# The ship cannot overlap or be in contact with any other ship, neither by edge nor by corner.

def validate_battlefield(field):
    validated = [[False for y in range(10)] for x in range(10)]
    count = [0,4,3,2,1]

    for i in range(10):
        for j in range(10):
            if field[i][j] == 1 and not validated[i][j]:
                if not look_around(i=i,j=j,validated=validated):
                    return False
                validated[i][j] = True
                size = 1  
                n = i+1
                while n < 10 and field[n][j] == 1:
                    if not look_around(j=j,n=n,validated=validated):
                        return False
                    validated[n][j] = True
                    size += 1
                    n += 1
                if size < 2:
                    m = j+1
                    while m < 10 and field[i][m] == 1:
                        if not look_around(i=i,m=m,validated=validated):
                            return False
                        validated[i][m] = True
                        size += 1
                        m += 1
                if size > 4:
                    return False
                count[size] -= 1

    return count.count(0) == 5

def look_around(i = None, j =None, n = None, m = None, validated=[]):
    if n != None:
        for idx in range(-1,2,1):
            aux = j + idx
            if aux >= 0 and aux % 10 > 0:
                if (n+1) % 10 > 0 and validated[n+1][aux]:
                    return False
                if idx != 0:
                    if (n % 10 > 0 or n == 0) and validated[n][aux]:
                        return False
                    if n-1 > 0 and ((n-1) % 10 > 0 or n-1 == 0) and validated[n-1][aux]:
                        return False
    elif m != None:
        if (i % 10 > 0 or i == 0) and (m + 1) % 10 > 0 and validated[i][m+1]:
                return False
        for idx in range(-1,2,1):
            aux = m + idx
            if aux >= 0 and aux % 10 > 0:
                if (i+1) % 10 > 0 and validated[i+1][aux]:
                    return False
                if i-1 > 0 and ((i-1) % 10 > 0 or i == 0) and validated[i-1][aux]:
                    return False
    else:
        for idx in range(-1,2,1):
            aux = j + idx
            if aux >= 0 and aux % 10 > 0:
                if (i+1) % 10 > 0 and validated[i+1][aux]:
                    return False
                if i-1 > 0 and ((i-1) % 10 > 0 or i-1 == 0) and validated[i-1][aux]:
                    return False
                if idx != 0:
                    if (i % 10 > 0 or i == 0) and validated[i][aux]:
                        return False
    return True