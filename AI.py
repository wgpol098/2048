import numpy as np
from math import *
from random import *
from settings import *
import operator

#spróbowanie innej oceny sytuacji
def ScoreCount(board):
    m = [6,5,4,3,
         5,4,3,2,
         4,3,2,1,
         3,2,1,0]
    return (sum(board*m))

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


def BM(grid, depth, agent):
    if depth == 0:
        return ScoreCount(grid)
    elif agent == 10001:
        score = 0
        empty = np.where(grid == 0)[0]
        #print(result)
        for i in empty:
            newGrid = grid.copy()
            newGrid[i] = 2
            score += BM(newGrid,depth-1,10002)
        if len(empty) !=0:
            return score/len(empty)
        return score
    elif agent is 10002:
        score = 0
        #c=0
        for i in [LEFT, UP, RIGHT, DOWN]:
            newGrid = nextMoveAI(grid,i)
            score = max(score,BM(newGrid,depth-1,10001)) # +=
            #penalty=0
            #c+=1
            #for i in range(0,len(newGrid)):
                #penalty += abs(newGrid[i] + newGrid[i+Size])
                #if i>0:
             #       penalty += abs(newGrid[i] - newGrid[i-1])
              #  if i <(Size*Size-1):
               #     penalty += abs(newGrid[i] - newGrid[i+1])
                #if i>Size:
                 #   penalty += abs(newGrid[i] - newGrid[i-Size])
                #if i<Size*Size-Size:
                  #  penalty += abs(newGrid[i] - newGrid[i+Size])
                    
            #score -=penalty
        return score
        
 
def BestMoveAI5(board,depth):
    sup=0
    sdown=0
    sleft=0
    sright=0
    if IsSame(board,nextMoveAI(board,UP)) == False:
        sup = BM(nextMoveAI(board,UP),depth,10001)
    if IsSame(board,nextMoveAI(board,DOWN)) == False:    
        sdown = BM(nextMoveAI(board,DOWN),depth,10001)
    if IsSame(board,nextMoveAI(board,LEFT)) == False:
        sleft = BM(nextMoveAI(board,LEFT),depth,10001)
    if IsSame(board,nextMoveAI(board,RIGHT)) == False:
        sright = BM(nextMoveAI(board,RIGHT),depth,10001)
    

    
    print(sup)
    print(sdown)
    print(sleft)
    print(sright)
    smax = max(sup, sdown, sleft, sright)
    if sup == smax:
        print("up")
        return UP
    elif sdown == smax:
        print("down")
        return DOWN
    elif sleft == smax:
        return LEFT
    elif sright == smax:
        print("right")
        return RIGHT
#Monte Carlo2
def BestMoveAI4(board):
    N=10
    sup=[]
    sdown=[]
    sright=[]
    sleft=[]
    b1 = board.copy()
    for i in range(0,N):
        rand = floor(random() * 4)
        rand2 = floor(random() * Size*Size)
             
        if rand == 0:
            b1 = nextMoveAI(b1,UP)
            sup.append(ScoreCountL(b1))
            #print(b1)
            #print(sup)
        elif rand == 1:
            b1 = nextMoveAI(b1,LEFT)
            sleft.append(ScoreCountL(b1))
        elif rand == 2:
            b1 = nextMoveAI(b1,DOWN)
            sdown.append(ScoreCountL(b1))
        elif rand == 3:
            b1 = nextMoveAI(b1,RIGHT)
            sright.append(ScoreCountL(b1))
            
        if IsEmpty(b1) == False:
            break
        while b1[rand2]!=0:
            rand2 = floor(random() * Size*Size)
            
        b1[rand2]=2
            
    up=0
    down=0
    left=0
    right=0
    if len(sup)!=0:       
        up = sum(sup)/len(sup) 
    if len(sdown)!=0:      
        down = sum(sdown)/len(sdown) 
    if len(sright)!=0:      
        right = sum(sright)/len(sright) 
    if len(sleft)!=0:      
        left = sum(sleft)/len(sleft) 
    print(up)
    print(down)
    print(left)
    print(right)

    smax = max(up,right,down,left)
    if up == smax:
        print("up")
        return UP
    elif down == smax:
        print("down")
        return DOWN
    elif left == smax:
        print("left")
        return LEFT
    elif right == smax:
        print("right")
        return RIGHT
 
#Monte Carlo
def BestMoveAI3(board):

    N=10 #100
    moves=20 #150
    sup=0
    sright=0
    sdown=0
    sleft=0
    for i in range(0,N):
        b1 = nextMoveAI(board,UP)
        b2 = nextMoveAI(board,DOWN)
        b3 = nextMoveAI(board,LEFT)
        b4 = nextMoveAI(board,RIGHT)
        

        
        #UP
        if IsSame(board,b1) == False:
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
        if IsSame(board,b2) == False:
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
        if IsSame(board,b3) == False:
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
        if IsSame(board,b4) == False:
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
    
    
 
def BestMoveAI22(board,depth):
    c=0
    if depth%2 == 1:
        c=1
    return BestMoveAI2(board,depth,depth,c)
 
#Ocenianie najlepszego ruchu w danym momencie dla zachłannego z patrzeniem w przód
def BestMoveAI2(board,depth,prevdepth,ddd):
    #jeśli jest to pierwszy poziom rekurencji to zwróc ruch
    #trzeba tu analizować, który ruch będzie najlepszy
    if depth == prevdepth:
        #print("elo")
        depth-=1
        sup=0
        sdown=0
        sright=0
        sleft=0
        
        b=nextMoveAI(board,UP)      
        if IsSame(board,b) == False:
            sup = BestMoveAI2(b,depth,prevdepth,ddd)
        
        b=nextMoveAI(board,LEFT)       
        if IsSame(board,b) == False:
            sleft = BestMoveAI2(b,depth,prevdepth,ddd)
        
        b=nextMoveAI(board,DOWN)
        if IsSame(board,b) == False:
            sdown = BestMoveAI2(b,depth,prevdepth,ddd)
        
        b=nextMoveAI(board,RIGHT)      
        if IsSame(board,b) == False:
            sright = BestMoveAI2(b,depth,prevdepth,ddd)
        
        
        #print(sdown)
        #print(sright)
        #print(sleft)
        #print(sup)
        
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
            #print("up")
            return UP
        elif sdown == smax:
            #print("down")
            return DOWN
        elif sleft == smax:
            #print("left")
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
            #print("right")
            return RIGHT
            
            
    elif depth > 0:
        depth-=1
        sup= []
        sleft= []
        sdown= []
        sright= []
        
        b=nextMoveAI(board,UP)
        if IsSame(board,b) == False:
            #sup.append(BestMoveAI2(b,depth,prevdepth,ddd))
            for i in range(0,Size*Size):
                if b[i]==0:
                    b[i]=2
                    sup.append(BestMoveAI2(nextMoveAI(b,UP),depth,prevdepth,ddd))
                    b[i]=0
  
        b=nextMoveAI(board,LEFT)
        if IsSame(board,b) == False:
            #sleft.append(BestMoveAI2(b,depth,prevdepth,ddd))
            for i in range(0,Size*Size):
                if b[i]==0:
                    b[i]=2
                    sleft.append(BestMoveAI2(nextMoveAI(b,LEFT),depth,prevdepth,ddd))
                    b[i]=0
        
        b=nextMoveAI(board,DOWN)    
        if IsSame(board,b) == False:
            #sdown.append(BestMoveAI2(b,depth,prevdepth,ddd))
            for i in range(0,Size*Size):
                if b[i]==0:
                    b[i]=2
                    sdown.append(BestMoveAI2(nextMoveAI(b,DOWN),depth,prevdepth,ddd))
                    b[i]=0
        
        b=nextMoveAI(board,RIGHT)   
        if IsSame(board,b) == False:
            #sright.append(BestMoveAI2(b,depth,prevdepth,ddd))
            for i in range(0,Size*Size):
                if b[i]==0:
                    b[i]=2
                    sright.append(BestMoveAI2(nextMoveAI(b,RIGHT),depth,prevdepth,ddd))
                    b[i]=0

        
        #print("---")
        #print(sup)
        #print(sdown)
        #print(sleft)
        #print(sright)
        if depth%2==ddd:
            u=0
            d=0
            r=0
            l=0
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
            
    elif depth == 0:
        #print(board)
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
            sup+=1
        elif rand == 1:
            sleft+=1
        elif rand == 2:
            sdown+=1
        elif rand == 3:
            sright+=1
    
    smax = max(sup, sdown, sleft, sright)
    if sup == smax:
        #print("up")
        return UP
    elif sdown == smax:
        #print("down")
        return DOWN
    elif sleft == smax:
        #return LEFT
        smax = max(sup,sdown,sright)
        if sup == smax:
            #print("up")
            return UP
        elif sdown == smax:
            #print("down")
            return DOWN
        elif sright == smax:
            #print("right")
            return RIGHT
    elif sright == smax:
        #print("right")
        return RIGHT