from random import *
from boardandAI import *
import operator

#spróbowanie innej oceny sytuacji
def ScoreCount(board):
    g = Size+(Size-1)
    m=np.zeros(Size*Size, dtype=int)
    tmp=0
    for i in range(0,Size*Size):
        if tmp == Size:
            tmp=1
            g+=(Size-2)
        else:
            g-=1
            tmp+=1
        m[i]=g
    #[6,5,4,3,
    #[6,5,4,3,
    #5,4,3,2,
    #4,3,2,1,
    #3,2,1,0]
    return (sum(board*m))

def BM(grid, depth, agent):
    if depth == 0:
        return ScoreCount(grid)
    elif agent == 10001:
        score = 0
        empty = np.where(grid == 0)[0]
        for i in empty:
            newGrid = grid.copy()
            newGrid[i] = 2
            score += BM(newGrid,depth-1,10002)
        if len(empty) !=0:
            return score/len(empty)
        return score
    elif agent is 10002:
        score = 0
        for i in [LEFT, UP, RIGHT, DOWN]:
            newGrid = nextMove(grid,i)
            score = max(score,BM(newGrid,depth-1,10001))
        return score       
 
def BestMoveAI5(board,depth):
    sup=0
    sdown=0
    sleft=0
    sright=0
    
    b1 = nextMove(board,UP)
    b2 = nextMove(board,DOWN)
    b3 = nextMove(board,LEFT)
    b4 = nextMove(board,RIGHT)
    
    if IsSame(board,b1) == False:
        sup = BM(b1,depth,10001)
    if IsSame(board,b2) == False:    
        sdown = BM(b2,depth,10001)
    if IsSame(board,b3) == False:
        sleft = BM(b3,depth,10001)
    if IsSame(board,b4) == False:
        sright = BM(b4,depth,10001)
 
    smax = max(sup, sdown, sleft, sright)
    if sup == smax:
        return UP
    elif sdown == smax:
        return DOWN
    elif sleft == smax:
        return LEFT
    elif sright == smax:
        return RIGHT
        
#Monte Carlo
def BestMoveAI3(board,N,moves):

    #N=10 #100
    #moves=10 #150
    sup=0
    sright=0
    sdown=0
    sleft=0
    for i in range(0,N):
        b1 = nextMove(board,UP)
        b2 = nextMove(board,DOWN)
        b3 = nextMove(board,LEFT)
        b4 = nextMove(board,RIGHT)
        
        #UP
        if IsSame(board,b1) == False:
            for i in range(0,moves):
                rand2 = floor(random() * Size*Size)
                
                if IsEmpty(b1) == False:
                    break
                while b1[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
                b1[rand2]=2
                
                b1 = nextMoverand(b1)
            sup += ScoreCountL(b1)
        #DOWN
        if IsSame(board,b2) == False:
            for i in range(0,moves):
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b2) == False:
                    break
                while b2[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
                b2[rand2]=2
                
                b2 = nextMoverand(b2)
            sdown += ScoreCountL(b2)
        #LEFT
        if IsSame(board,b3) == False:
            for i in range(0,moves):
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b3) == False:
                    break
                while b3[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
                b3[rand2]=2
                
                b3 = nextMoverand(b3)
            sleft += ScoreCountL(b3)
        #RIGHT
        if IsSame(board,b4) == False:
            for i in range(0,moves):
                rand2 = floor(random() * Size*Size)
            
                if IsEmpty(b4) == False:
                    break
                while b4[rand2]!=0:
                    rand2 = floor(random() * Size*Size)
                b4[rand2]=2
                
                b4 = nextMoverand(b4)
            sright += ScoreCountL(b4)
    
    sup = sup/N
    sdown = sdown/N
    sleft = sleft/N
    sright = sright/N
    
    smax = max(sup,sright,sdown,sleft)
    if sup == smax:
        return UP
    elif sdown == smax:
        return DOWN
    elif sleft == smax:
        return LEFT
    elif sright == smax:
        return RIGHT     
        
#Zwracanie planszy dla randomowego ruchu
def nextMoverand(board):
    rand = floor(random() * 4)
    if rand == 0:
        return nextMove(board,UP)
    elif rand == 1:
        return nextMove(board,LEFT)
    elif rand == 2:
        return nextMove(board,DOWN)
    else:
        return nextMove(board,RIGHT)
 
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
        sup=0
        sdown=0
        sright=0
        sleft=0
        
        b=nextMove(board,UP)      
        if IsSame(board,b) == False:
            sup = BestMoveAI2(b,depth-1,prevdepth,ddd)
        
        b=nextMove(board,LEFT)       
        if IsSame(board,b) == False:
            sleft = BestMoveAI2(b,depth-1,prevdepth,ddd)
        
        b=nextMove(board,DOWN)
        if IsSame(board,b) == False:
            sdown = BestMoveAI2(b,depth-1,prevdepth,ddd)
        
        b=nextMove(board,RIGHT)      
        if IsSame(board,b) == False:
            sright = BestMoveAI2(b,depth-1,prevdepth,ddd)
 
        
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
            return UP
        elif sdown == smax:
            return DOWN
        elif sleft == smax:
            return LEFT
        elif sright == smax:
            return RIGHT
            
            
    elif depth > 0:
        depth-=1
        sup= []
        sleft= []
        sdown= []
        sright= []
        
        b=nextMove(board,UP)
        if IsSame(board,b) == False:
            empty = np.where(b == 0)[0]
            for i in empty:
                b1 = b.copy()
                b1[i]=2
                sdown.append(BestMoveAI2(b1,depth,prevdepth,ddd))
  
        b=nextMove(board,LEFT)
        if IsSame(board,b) == False:
            empty = np.where(b == 0)[0]
            for i in empty:
                b1 = b.copy()
                b1[i]=2
                sdown.append(BestMoveAI2(b1,depth,prevdepth,ddd))
        
        b=nextMove(board,DOWN)    
        if IsSame(board,b) == False:
            empty = np.where(b == 0)[0]
            for i in empty:
                b1 = b.copy()
                b1[i]=2
                sdown.append(BestMoveAI2(b1,depth,prevdepth,ddd))
        
        b=nextMove(board,RIGHT)   
        if IsSame(board,b) == False:
            empty = np.where(b == 0)[0]
            for i in empty:
                b1 = b.copy()
                b1[i]=2
                sdown.append(BestMoveAI2(b1,depth,prevdepth,ddd))

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
            u=np.inf
            d=np.inf
            r=np.inf
            l=np.inf
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
        return ScoreCountL(board)
             
#Ocenianie najlepszego ruchu w danym momencie dla zachłannego bez patrzenia w przód
def BestMoveAI(board):
    sup = 0
    sdown = 0
    sleft = 0
    sright = 0
    b1 = nextMove(board,UP)
    b2 = nextMove(board,DOWN)
    b3 = nextMove(board,LEFT)
    b4 = nextMove(board,RIGHT)
    
    if IsSame(board,b1) != True:
        sup = ScoreCountL(b1)
    if IsSame(board,b2) != True:
        sdown = ScoreCountL(b2)
    if IsSame(board,b3) != True:
        sleft = ScoreCountL(b3)
    if IsSame(board,b4) != True:
        sright = ScoreCountL(b4)
    

    
    smax = max(sup, sdown, sleft, sright)
    if sup == smax:
        return UP
    elif sdown == smax:
        return DOWN
    elif sleft == smax:
        smax = max(sup,sdown,sright)
        if IsSame(board,b1) and IsSame(board,b2) and IsSame(board,b4):
            return LEFT
        if sup == smax:
            return UP
        elif sdown == smax:
            return DOWN
        elif sright == smax:
            return RIGHT
    elif sright == smax:
        return RIGHT