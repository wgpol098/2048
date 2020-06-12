from AI import *
import datetime

#ilość wykowywanych testów
N=10

def addRand(board):
    rand = floor(random() * pow(Size,2)) 
    while board[rand] != 0:
        rand = floor(random() * pow(Size,2))
        
    board[rand]=2
    return board

def AI_test(filename,function,depth):
    f = open(filename, "w")
    for i in range(0,N):
        board = np.zeros(Size*Size, dtype=int)
        board = addRand(board)
        board = addRand(board)
        moves=0
        start = datetime.datetime.now() 
        while True: 
            board = nextMove(board,function(board,depth))
            moves+=1
            if IsEmpty(board) == False:
                break
            board = addRand(board)
        end = datetime.datetime.now() - start
        f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
        print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
    f.close()

def AI3_test(filename,iteration,depth):
    f = open(filename, "w")
    for i in range(0,N):
        board = np.zeros(Size*Size, dtype=int)
        board = addRand(board)
        board = addRand(board)
        moves=0
        start = datetime.datetime.now() 
        while True: 
            board = nextMove(board,BestMoveAI3(board,iteration,depth))
            moves+=1
            if IsEmpty(board) == False:
                break
            board = addRand(board)
        end = datetime.datetime.now() - start
        f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
        print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
    f.close()

def AI1_test(filename):
    f = open(filename, "w")
    for i in range(0,N):
        board = np.zeros(Size*Size, dtype=int)
        board = addRand(board)
        board = addRand(board)
        moves=0
        start = datetime.datetime.now() 
        while True: 
            board = nextMove(board,BestMoveAI(board))
            moves+=1
            if IsEmpty(board) == False:
                break
            board = addRand(board)
        end = datetime.datetime.now() - start
        f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
        print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
    f.close()

print ("-------AI1-------")
AI1_test("ai1.txt")

for i in range(2,4):
    print ("-------AI2_"+str(i)+"-------")
    AI_test("ai2_"+str(i)+".txt",BestMoveAI22,i)

ai3 = [[10,10],[10,100],[50,10],[100,10]]
for i in range(0,len(ai3)):
    print ("-------AI3_"+str(ai3[i][0])+"_"+str(ai3[i][1])+"-------")
    AI3_test("ai3_"+str(ai3[i][0])+"_"+str(ai3[i][1])+".txt",ai3[i][0],ai3[i][1])

for i in range(2,8):
    print ("-------AI5_"+str(i)+"-------")
    AI_test("ai5_"+str(i)+".txt",BestMoveAI5,i)