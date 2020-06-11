from random import *
from boardandAI import *
import operator
from statistics import mean

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
    tup = []
    moves = [UP,LEFT,DOWN,RIGHT]
    
    for i in moves:
        b1 = nextMove(board,i)
        if IsSame(board,b1) == False:
            tup.append(BM(b1,depth,10001))
        else:
            tup.append(0)
            
    return moves[tup.index(max(tup))]
        
#Monte Carlo
def BestMoveAI3(board,N,no_moves):

    #N=10 #100
    #moves=10 #150
    tup = []
    moves = [UP,LEFT,DOWN,RIGHT]

    for j in moves:
        summ=0
        for i in range(0,N):
            b1 = nextMove(board,j)
            
            if IsSame(board,b1) == False:
                for k in range(0,no_moves):
                    rand2 = floor(random() * Size*Size)
                
                    if IsEmpty(b1) == False:
                        break
                    while b1[rand2]!=0:
                        rand2 = floor(random() * Size*Size)
                    b1[rand2]=2
                
                    b1 = nextMoverand(b1)
            summ+= ScoreCountL(b1)
        tup.append(summ/N)
            
    return moves[tup.index(max(tup))]
            
#Zwracanie planszy dla randomowego ruchu
def nextMoverand(board):
    moves = [UP,LEFT,DOWN,RIGHT]
    return nextMove(board,moves[floor(random() * 4)])
 
def BestMoveAI22(board,depth):
    return BestMoveAI2(board,depth,depth)
 
#Ocenianie najlepszego ruchu w danym momencie dla zachłannego z patrzeniem w przód
def BestMoveAI2(board,depth,prevdepth):
    if depth == prevdepth:
        moves = [UP,LEFT,DOWN,RIGHT]
        tup = []
        
        for i in moves:
            b=nextMove(board,i)
            if IsSame(board,b) == False:
                tup.append(BestMoveAI2(b,depth-1,prevdepth))
            else: 
                tup.append(0)
    
        return moves[tup.index(max(tup))]
            
    elif depth > 0:
        tup = []
        moves = [UP,LEFT,DOWN,RIGHT]
        b=board.copy()
        empty = np.where(b == 0)[0]
        for i in empty:
            b[i]=2
            for j in moves:
                b1 = nextMove(b,j)
                if IsSame(board,b1) == False:
                    tup.append(BestMoveAI2(b1,depth-1,prevdepth))
            b[i]=0
  
        if len(tup) == 0:
            return 0
        return mean(tup)
            
    elif depth == 0:
        return ScoreCountL(board)
             
#Ocenianie najlepszego ruchu w danym momencie dla zachłannego bez patrzenia w przód
def BestMoveAI(board):
    tup = []
    moves = [UP,LEFT,DOWN,RIGHT]
    
    for i in moves:
        b1 = nextMove(board,i)
        if IsSame(board,b1) == False:
            tup.append(ScoreCountL(b1))
        else:
            tup.append(0)
        
    mmax = tup.index(max(tup))
    if mmax != 1:
        return moves[mmax]
    else:
        if tup[0] == 0 and tup[2] == 0 and tup[3] == 0:
            return moves[mmax]
        else:
            tup[mmax]=0
            return moves[tup.index(max(tup))]