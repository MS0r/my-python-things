# https://www.codewars.com/kata/526c7b931666d07889000a3c/python
import random

downup = {'>': 1, '<': -1, '^': -1, 'v': 1}


def interpret(code):
    output = ""
    stack = []
    grid = []
    for i in code.split('\n'):
        grid.append([j for j in i])
    i = 0
    j = 0
    cr = grid[i][j]
    move = ['<', '>', 'v', '^', '?', '_', '|']
    stackCH = ['$', '.', ',', ':', '\\']
    matheCH = ['+', '-', '*', '/', '%', "`"]
    putget = ['p', 'g']
    going = '>'
    while cr != '@':
        if cr in move:
            going = cr
        elif cr.isnumeric():
            stack.append(int(cr))
        elif cr in stackCH:
            output = outChar(cr, stack, output)
        elif cr in matheCH:
            stack.append(mathe(cr, stack.pop(), stack.pop()))
        elif cr in putget:
            pg(cr, stack, grid)
        elif cr == '!':
            stack.append(1 if stack.pop() == 0 else 0)
        elif cr == '\"':
            cr, i, j, going = moves(going, grid, i, j)
            while cr != '\"':
                stack.append(ord(cr))
                cr, i, j, going = moves(going, grid, i, j)
        elif cr == '#':
            cr, i, j, going = moves(going, grid, i, j)
        going = looking(going, stack)
        cr, i, j, going = moves(going, grid, i, j)
    return output


def pg(cr, stack, grid):
    x = stack.pop()
    y = stack.pop()
    if cr == 'p':
        v = stack.pop()
        grid[x][y] = chr(v)
    else:
        stack.append(ord(grid[x][y]))


def mathe(cr, a, b):
    c = None
    if cr == '+':
        c = a+b
    elif cr == '-':
        c = b-a
    elif cr == '*':
        c = a*b
    elif cr == '/':
        c = int(b/a) if a != 0 else 0
    elif cr == '%':
        c = b % a if a != 0 else 0
    else:
        c = 1 if b > a else 0

    return c


def outChar(cr, stack, output):
    if cr == '.':
        output += str(stack.pop())
    elif cr == ',':
        output += chr(stack.pop())
    elif cr == ':':
        if len(stack) != 0:
            stack.append(stack[-1])
        else:
            stack.append(0)
    elif cr == '$':
        stack.pop()
    else:
        last = stack.pop()
        other = 0 if len(stack) == 0 else stack.pop()
        stack.extend([last, other])

    return output


def looking(going, stack):
    if going == '_' or going == '|':
        if stack.pop() == 0:
            going = '>' if going == '_' else 'v'
        else:
            going = '<' if going == '_' else '^'
    elif going == '?':
        going = random.choice('><v^')

    return going


def moves(going, grid, i, j):
    if going == '>' or going == '<':
        j += downup[going]
    elif going == '^' or going == 'v':
        i += downup[going]

    return [grid[i][j], i, j, going]
