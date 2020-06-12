import numpy as np
from math import *
from settings import *

#obliczanie liczby punktów dla danej planszy (lista)
def ScoreCountL(board):
    score = 0
    for i in range(0,Size*Size):
        if board[i] != 0 and board[i] != 2:
            c = log(board[i],2)
            score += (c-1)*pow(2,c)
    return int(score)
    
#False - jeśli plansza nie ma wolnych miejsc
#True - jeśli plansza ma wolne miejsca
def IsEmpty(board):
    if len(np.where(board == 0)[0]) == 0:
        return False
    return True
    
#True - dwie plansze są takie same
#False - plansze różnią się   
def IsSame(board1, board2):
    c = 0
    for i in range(0,Size*Size):
        if board1[i] == board2[i]:
            c+=1
            
    if c == Size*Size:
        return True
    return False
    
#Przesuwanie elementów
def swipeRow(row):
    prev = -1
    i = 0
    temp = np.zeros(Size, dtype=int)
            
    for elem in row:
        if elem != 0:
            if prev == -1:
                prev = elem
                temp[i] = elem
                i += 1
            elif prev == elem:
                temp[i-1] = 2*prev
            else:
                prev = elem
                temp[i] = elem
                i += 1
    return temp
    
#Zwracanie planszy dla następnego ruchu
def nextMove(board, move):
    tmp = np.zeros(Size*Size, dtype=int)
    if move == UP:
        for i in range(0,Size):
            row = []
            for j in range(Size):
                row.append(board[i+Size*j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                tmp[i + Size*j] = val
                
    elif move == DOWN:
        for i in range(0,Size):
            row = []
            for j in range(Size):
                row.append(board[i + Size * (Size-1-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                tmp[i + Size * (Size-1-j)] = val
                
    elif move == LEFT:
        for i in range(0,Size):
            row = []
            for j in range(Size):
                row.append(board[Size*i + j])
            row = swipeRow(row)
            for j, val in enumerate(row):
                tmp[Size*i + j] = val
                
    elif move == RIGHT:
        for i in range(0,Size):
            row = []
            for j in range(Size):
                row.append(board[Size * i + (Size-1-j)])
            row = swipeRow(row)
            for j, val in enumerate(row):
                tmp[Size * i + (Size-1-j)] = val
                
    return tmp