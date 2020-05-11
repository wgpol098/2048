import numpy as np
from math import *
from random import *
from settings import *

#obliczanie liczby punktów dla danej planszy (lista)
def ScoreCountL(board):
    score = 0
    for i in range(0,Size*Size):
        if board[i] != 0 and board[i] != 2:
            c=0
            b=1
            while b!= board[i]:
                b=b+b
                c+=1
            score += (c-1)*pow(2,c)
    return int(score)
    
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
  
#False - jeśli plansza nie ma wolnych miejsc
#True - jeśli plansza ma wolne miejsca
def IsEmpty(board):
    c=0
    for i in range(0,Size*Size):
        if board[i]==0:
            c+=1
            
    if c == 0:
        return False
    return True
#Monte Carlo
def BestMoveAI3(board):

    N=100
    moves=300
    sup=0
    sright=0
    sdown=0
    sleft=0
    for i in range(0,N):
        b1 = nextMoveAI(board,UP)
        b2 = nextMoveAI(board,DOWN)
        b3 = nextMoveAI(board,LEFT)
        b4 = nextMoveAI(board,RIGHT)
        
        #Sprawdzanie czy w ogóle warto liczyć dla danego ruchu
        b11=0
        b22=0
        b33=0
        b44=0
        for i in range(0,Size*Size):
            if b1[i] == board[i]:
                b11+=1
            if b2[i] == board[i]:
                b22+=1
            if b3[i] == board[i]:
                b33+=1
            if b4[i] == board[i]:
                b44+=1
        
        #UP
        if b11 != Size*Size:
            for i in range(0,moves):
                rand = floor(random() * 4)
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b1) == False:
                    break
                while b1[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
            
                b1[rand2]=2
                if rand == 0:
                    b1 = nextMoveAI(b1,UP)
                elif rand == 1:
                    b1 = nextMoveAI(b1,LEFT)
                elif rand == 2:
                    b1 = nextMoveAI(b1,DOWN)
                elif rand == 3:
                    b1 = nextMoveAI(b1,RIGHT)
            sup += ScoreCountL(b1)
        #DOWN
        if b22 != Size*Size:
            for i in range(0,moves):
                rand = floor(random() * 4)
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b2) == False:
                    break
                while b2[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
            
                b2[rand2]=2
                if rand == 0:
                    b2 = nextMoveAI(b2,UP)
                elif rand == 1:
                    b2 = nextMoveAI(b2,LEFT)
                elif rand == 2:
                    b2 = nextMoveAI(b2,DOWN)
                elif rand == 3:
                    b2 = nextMoveAI(b2,RIGHT)
            sdown += ScoreCountL(b2)
        #LEFT
        if b33 != Size*Size:
            for i in range(0,moves):
                rand = floor(random() * 4)
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b3) == False:
                    break
                while b3[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
            
                b3[rand2]=2
                if rand == 0:
                    b3 = nextMoveAI(b3,UP)
                elif rand == 1:
                    b3 = nextMoveAI(b3,LEFT)
                elif rand == 2:
                    b3 = nextMoveAI(b3,DOWN)
                elif rand == 3:
                    b3 = nextMoveAI(b3,RIGHT)
            sleft += ScoreCountL(b3)
        #RIGHT
        if b44 != Size*Size:
            for i in range(0,moves):
                rand = floor(random() * 4)
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b4) == False:
                    break
                while b4[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
            
                b4[rand2]=2
                if rand == 0:
                    b4 = nextMoveAI(b4,UP)
                elif rand == 1:
                    b4 = nextMoveAI(b4,LEFT)
                elif rand == 2:
                    b4 = nextMoveAI(b4,DOWN)
                elif rand == 3:
                    b4 = nextMoveAI(b4,RIGHT)
            sright += ScoreCountL(b4)
    
    sup = sup/N
    sdown = sdown/N
    sleft = sleft/N
    sright = sright/N
    print(sup)
    print(sdown)
    print(sright)
    print(sleft)
    
    smax = max(sup,sright,sdown,sleft)
    if sup == smax:
        print("up")
        return UP
    elif sdown == smax:
        print("down")
        return DOWN
    elif sleft == smax:
        print("left")
        return LEFT
    elif sright == smax:
        print("right")
        return RIGHT
        
        
        
#Zwracanie planszy dla następnego ruchu
def nextMoveAI(board, move):
    tmp = np.zeros(Size*Size, dtype=int)
    if move == UP:
        for i in range(Size):
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
    
    
    
#Ocenianie najlepszego ruchu w danym momencie dla zachłannego z patrzeniem w przód
def BestMoveAI2(board,depth,prevdepth,score):
    #jeśli jest to pierwszy poziom rekurencji to zwróc ruch
    #trzeba tu analizować, który ruch będzie najlepszy
    if depth == prevdepth:
        print("elo")
        depth-=1
        sup=0
        sdown=0
        sright=0
        sleft=0
        c=0
        b=nextMoveAI(board,UP)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            sup = BestMoveAI2(nextMoveAI(board,UP),depth,prevdepth,score)
        
        c=0
        b=nextMoveAI(board,LEFT)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            sleft = BestMoveAI2(nextMoveAI(board,LEFT),depth,prevdepth,score)
        
        c=0
        b=nextMoveAI(board,DOWN)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            sdown = BestMoveAI2(nextMoveAI(board,DOWN),depth,prevdepth,score)
        
        c=0
        b=nextMoveAI(board,RIGHT)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            sright = BestMoveAI2(nextMoveAI(board,RIGHT),depth,prevdepth,score)
        
        depth = prevdepth-1
        
        #sdown = sdown/int(pow(4,depth))
        #sright = sright/int(pow(4,depth))
        #sleft = sleft/int(pow(4,depth))
        #sup = sup/int(pow(4,depth))
        print(sdown)
        print(sright)
        print(sleft)
        print(sup)
        
        if sup == sdown and sdown == sleft and sleft ==sright:
            rand = floor(random() * 4)
            if rand == 0:
                sup=+1
            elif rand == 1:
                sleft+1
            elif rand == 2:
                sdown+=1
            elif rand == 3:
                sright+=1
    
        smax = max(sup, sdown, sleft, sright)
        
        if sup == smax:
            print("up")
            return UP
        elif sdown == smax:
            print("down")
            return DOWN
        elif sleft == smax:
            print("left")
        ####
        #####
        ######
        #Głupota niby ale działa
        ######
        #####
        ####
            return LEFT
            #smax = max(sup,sdown,sright)
            #if sup == smax:
            #    print("up")
            #    return UP
            #elif sdown == smax:
            #    print("down")
            #    return DOWN
            #elif sright == smax:
            #    print("right")
            #    return RIGHT
        elif sright == smax:
            print("right")
            return RIGHT
            
            
    elif depth > 0:
        #print("elo")
        depth-=1
        sup= []
        sleft= []
        sdown= []
        sright= []
        
        c=0
        b=nextMoveAI(board,UP)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sup.append(BestMoveAI2(nextMoveAI(board,UP),depth,prevdepth,score))
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sup.append(BestMoveAI2(nextMoveAI(board,UP),depth,prevdepth,score))
                    board[i]=0
                
            #if c!=0:
                #sup = sup/(c+1)
  
        c=0
        b=nextMoveAI(board,LEFT)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sleft.append(BestMoveAI2(nextMoveAI(board,LEFT),depth,prevdepth,score))
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sleft.append(BestMoveAI2(nextMoveAI(board,LEFT),depth,prevdepth,score))
                    board[i]=0
             
        #    if c != 0:
         #       sleft = sleft/(c+1)
        
        c=0
        b=nextMoveAI(board,DOWN)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sdown.append(BestMoveAI2(nextMoveAI(board,DOWN),depth,prevdepth,score))
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sdown.append(BestMoveAI2(nextMoveAI(board,DOWN),depth,prevdepth,score))
                    board[i]=0
            #if c!=0:
                #sdown = sdown/(c+1)
        
        c=0
        b=nextMoveAI(board,RIGHT)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sright.append(BestMoveAI2(nextMoveAI(board,RIGHT),depth,prevdepth,score))
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sright.append(BestMoveAI2(nextMoveAI(board,RIGHT),depth,prevdepth,score))
                    board[i]=0
            
            #if c!=0:       
                #sright = sright/(c+1)
        u=0
        d=0
        r=0
        l=0
        if depth%2==0:
            if len(sleft) != 0:
                l = max(sleft)
            if len(sright) != 0:
                r = max(sright)
            if len(sup) != 0:
                u = max(sup)
            if len(sdown) != 0:
                d = max(sdown)
            return max(r,u,d,l)
        else:
            u=999999999
            d=999999999
            r=999999999
            l=999999999
            if len(sleft) != 0:
                l = min(sleft)
            if len(sright) != 0:
                r = min(sright)
            if len(sup) != 0:
                u = min(sup)
            if len(sdown) != 0:
                d = min(sdown)
            return min(r,u,d,l)
            
        #return (sup+sleft+sdown+sright)
          
    elif depth == 0:
        return ScoreCountL(board)
        
        
        
#Ocenianie najlepszego ruchu w danym momencie dla zachłannego bez patrzenia w przód
def BestMoveAI(board):
    sup = ScoreCountL(nextMoveAI(board,UP))
    sdown = ScoreCountL(nextMoveAI(board,DOWN))
    sleft = ScoreCountL(nextMoveAI(board,LEFT))
    sright = ScoreCountL(nextMoveAI(board,RIGHT))
    
    #inne możliwości, że trzy takie same np
    if sup == sdown and sdown == sleft and sleft ==sright:
        rand = floor(random() * 4)
        if rand == 0:
            sup=+1
        elif rand == 1:
            sleft+1
        elif rand == 2:
            sdown+=1
        elif rand == 3:
            sright+=1
    
    smax = max(sup, sdown, sleft, sright)
    if sup == smax:
        print("up")
        return UP
    elif sdown == smax:
        print("down")
        return DOWN
    elif sleft == smax:
        #return LEFT
        smax = max(sup,sdown,sright)
        if sup == smax:
            print("up")
            return UP
        elif sdown == smax:
            print("down")
            return DOWN
        elif sright == smax:
            print("right")
            return RIGHT
    elif sright == smax:
        print("right")
        return RIGHT