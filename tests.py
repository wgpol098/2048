from AI import *
import datetime

#ilość wykowywanych testów
N=10
#Plik do testowania działania metod

result = np.zeros(N, dtype=int)

def addRand(board):
    rand = floor(random() * pow(Size,2)) 
    while board[rand] != 0:
        rand = floor(random() * pow(Size,2))
        
    board[rand]=2
    return board


print ("-------AI1-------")
f = open("ai1.txt", "w")
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

print ("-------AI2_2-------")
f = open("ai2_2.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI22(board,2))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI2_3-------")
f = open("ai2_3.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI22(board,3))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()
    
print ("-------AI3_10_10-------")
f = open("ai3_10_10.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI3(board,10,10))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI3_10_100-------")
f = open("ai3_10_100.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    go=True
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI3(board,10,100))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI3_50_10-------")
f = open("ai3_100_100.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    go=True
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI3(board,50,10))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI3_100_10-------")
f = open("ai3_100_10.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI3(board,100,10))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI5_2-------")
f = open("ai5_2.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI5(board,2))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI5_3-------")
f = open("ai5_3.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI5(board,3))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()


print ("-------AI5_4-------")
f = open("ai5_4.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI5(board,4))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI5_5-------")
f = open("ai5_5.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI5(board,5))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI5_6-------")
f = open("ai5_6.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI5(board,6))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()

print ("-------AI5_7-------")
f = open("ai5_7.txt", "w")
for i in range(0,N):
    board = np.zeros(Size*Size, dtype=int)
    board = addRand(board)
    board = addRand(board)
    moves=0
    start = datetime.datetime.now() 
    while True: 
        board = nextMove(board,BestMoveAI5(board,7))
        moves+=1
        if IsEmpty(board) == False:
            break
        board = addRand(board)
    end = datetime.datetime.now() - start
    f.write(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end) + "\n")
    print(str(ScoreCountL(board)) + ";" + str(moves) + ";" + str(max(board)) + ";" + str(end))  
f.close()
