import pygame,sys,time
import pyautogui
from pygame.locals import *
from constants import *
from random import *
from math import *
import numpy as np

#Rozmiar planszy
Size=4
Width = Size*100
Height = Size*125
#macierz planszy
MatrixGame = np.zeros((Size,Size), dtype=int)
#Macierz planszy ruch wcześniej
MatrixPreviousGame = np.zeros((Size,Size), dtype=int)
#licznik punktów
Score = 0
#Ruchy
UP = 101
LEFT = 102
DOWN = 103
RIGHT = 104
#Flagi dla AI
AI1Flag = False
AI2Flag = False
AI3Flag = False


#inicjalizacja pygame
pygame.init()

#WindowSurface
WindowSurface = pygame.display.set_mode((Width,Height),0,32)
pygame.display.set_caption("2048")


def main():
    global MatrixPreviousGame
    global Score
    global AI1Flag
    global AI2Flag
    global AI3Flag
    addRandom()
    addRandom()
    Refresh()
    
    #obsługa zdarzeń i działanie gry
    while True:
        for event in pygame.event.get():
            #wyjscie z gry
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            #sprawdzanie czy można wykonać ruch
            if Check() == True:
                if event.type == KEYDOWN:
                    direction = -1
                    if event.key == pygame.K_UP:
                        direction = 0
                    if event.key == pygame.K_LEFT:
                        direction = 1
                    if event.key == pygame.K_DOWN:
                        direction = 2
                    if event.key == pygame.K_RIGHT:
                        direction = 3
                    #sztuczna inteligencja włącz/wyłącz
                    if event.key == pygame.K_1:
                        #zachłany bez patrzenia w przód
                        if AI1Flag == True:
                            AI1Flag=False
                        else:
                            AI1Flag=True
                            AI2Flag=False
                            AI3Flag=False
                    if event.key == pygame.K_2:
                        #zachałanny z patrzeniem w przód
                        if AI2Flag == True:
                            AI2Flag=False
                        else:
                            AI2Flag=True
                            AI1Flag=False
                            AI3Flag=False
                    if event.key == pygame.K_3:
                        #patrzenie w przód monte carlo
                        if AI3Flag == True:
                            AI3Flag=False
                        else:
                            AI3Flag=True
                            AI1Flag=False
                            AI2Flag=False
                    
                    if direction!=-1:
                        MatrixPreviousGame = np.copy(MatrixGame)

                        #rotacja macierzy
                        for i in range(0,direction):
                            Rotate()
                        
                        #wykonanie ruchu    
                        if Check1() == True:
                            Move()
                            Merge()
                            addRandom()
                            Score = ScoreCountM(MatrixGame)
                         
                        #powrót macierzy do dawnego stanu
                        for i in range(0,(4-direction)%4):
                            Rotate()  
                    #Wywoływanie ruchu sztucznej inteligencji
                    if AI1Flag == True:
                        MoveAI1()
                    if AI2Flag == True:
                        MoveAI2()
                    if AI3Flag == True:
                        MoveAI3()
                        
                    #restart gry
                    if event.key == pygame.K_r:
                        Restart()
                        
                    #cofnięcie ruchu
                    if event.key == pygame.K_c:
                        Undo()
                    Refresh()
            #przegrana gra        
            else:
                GameOver()
                
        pygame.display.update()            
 
#cofanie planszy
def Undo():
    global MatrixGame
    global MatrixPreviousGame
    tmp = np.copy(MatrixGame)
    MatrixGame = np.copy(MatrixPreviousGame)
    MatrixPreviousGame = np.copy(tmp)
    
#restart gry
def Restart():
    global MatrixGame
    global Score
    MatrixGame = np.zeros((Size,Size),dtype=int)
    Score=0
    addRandom()
    addRandom()

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

#obliczanie liczby punktów na danej planszy (macierz)
def ScoreCountM(board):
    score = 0
    for i in range(0,Size):
        for j in range(0,Size):
            if board[i][j] != 0 and board[i][j] != 2:
                c=0
                b=1
                while b != board[i][j]:
                    b=b+b
                    c+=1
                score += (c-1)*pow(2,c)    
    return int(score)

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
            
                c=0
                for i in range(0,Size*Size):
                    if b1[i]==0:
                        c+=1
            
                if c == 0:
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
            
                c=0
                for i in range(0,Size*Size):
                    if b2[i]==0:
                        c+=1
            
                if c == 0:
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
            
                c=0
                for i in range(0,Size*Size):
                    if b3[i]==0:
                        c+=1
            
                if c == 0:
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
            
                c=0
                for i in range(0,Size*Size):
                    if b4[i]==0:
                        c+=1
            
                if c == 0:
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
                
        #if c!=int(pow(Size,2)):
         #   sleft = BestMoveAI2(nextMoveAI(board,LEFT),board.copy(),depth,prevdepth,score)
        
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
        
        sdown = sdown/int(pow(4,depth))
        sright = sright/int(pow(4,depth))
        #sleft = sleft/int(pow(4,depth))
        sup = sup/int(pow(4,depth))
        print(sdown)
        print(sright)
        #print(sleft)
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
        #print("left")
        ####
        #####
        ######
        #Głupota niby ale działa
        ######
        #####
        ####
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
            
            
    elif depth > 0:
        #print("elo")
        depth-=1
        sup=0
        sleft=0
        sdown=0
        sright=0
        
        c=0
        b=nextMoveAI(board,UP)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sup += BestMoveAI2(nextMoveAI(board,UP),depth,prevdepth,score)
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sup += BestMoveAI2(nextMoveAI(board,UP),depth,prevdepth,score)
                    board[i]=0
                
            if c!=0:
                sup = sup/(c+1)
  
        c=0
        #b=nextMoveAI(board,LEFT)
        #for i in range(0,int(pow(Size,2))):
        #    if board[i]==b[i]:
        #        c+=1
                
        #if c!=int(pow(Size,2)):
        #    c=0
        #    sleft += BestMoveAI2(nextMoveAI(board,LEFT),board.copy(),depth,prevdepth,score)
        #    for i in range(0,int(pow(Size,2))):
        #        if board[i]==0:
        #            board[i]=2
        #            c+=1
        #            sleft += BestMoveAI2(nextMoveAI(board,LEFT),board.copy(),depth,prevdepth,score)
        #            board[i]=0
             
        #    if c != 0:
         #       sleft = sleft/(c+1)
        
        c=0
        b=nextMoveAI(board,DOWN)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sdown += BestMoveAI2(nextMoveAI(board,DOWN),depth,prevdepth,score)
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sdown += BestMoveAI2(nextMoveAI(board,DOWN),depth,prevdepth,score)
                    board[i]=0
            if c!=0:
                sdown = sdown/(c+1)
        
        c=0
        b=nextMoveAI(board,RIGHT)
        for i in range(0,int(pow(Size,2))):
            if board[i]==b[i]:
                c+=1
                
        if c!=int(pow(Size,2)):
            c=0
            sright += BestMoveAI2(nextMoveAI(board,RIGHT),depth,prevdepth,score)
            for i in range(0,int(pow(Size,2))):
                if board[i]==0:
                    board[i]=2
                    c+=1
                    sright += BestMoveAI2(nextMoveAI(board,RIGHT),depth,prevdepth,score)
                    board[i]=0
            
            if c!=0:       
                sright = sright/(c+1)
        
            
        return (sup+sleft+sdown+sright)
          
    elif depth == 0:
        return ScoreCountL(board)

#funkcja odpowiedzialana za ruch sztucznej inteligencji (zachłanne z patrzeniem w przód z randomem)
def MoveAI3():
    currentValues = []
    for i in range(0,Size):
        for j in range(0,Size):
            currentValues.append(MatrixGame[floor((i+Size*j)/Size)][(i+Size*j)%Size])
        
    GetMove(BestMoveAI3(currentValues)) 
 
#funkcja odpowiedzialana za ruch sztucznej inteligencji (zachłanne z patrzeniem w przód)
def MoveAI2():
    currentValues = []
    for i in range(0,Size):
        for j in range(0,Size):
            currentValues.append(MatrixGame[floor((i+Size*j)/Size)][(i+Size*j)%Size])
        
    GetMove(BestMoveAI2(currentValues,2,2,Score)) 
 
#funkcja odpowiedzialana za ruch sztucznej inteligencji (zachłanne bez patrzenia w przód)
def MoveAI1():
    currentValues = []
    for i in range(0,Size):
        for j in range(0,Size):
            currentValues.append(MatrixGame[floor((i+Size*j)/Size)][(i+Size*j)%Size])
        
    GetMove(BestMoveAI(currentValues,Score))
        
def GetMove(move):
    if move == UP:
        pyautogui.keyDown('up')
        pyautogui.keyUp('up')
    elif move == DOWN:
        pyautogui.keyDown('down')
        pyautogui.keyUp('down')
    elif move == LEFT:
        pyautogui.keyDown('left')
        pyautogui.keyUp('left')
    elif move == RIGHT:
        pyautogui.keyDown('right')
        pyautogui.keyUp('right')       

#Ocenianie najlepszego ruchu w danym momencie dla zachłannego bez patrzenia w przód
def BestMoveAI(board,score):
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
  
#gameover gry
def GameOver():
        WindowSurface.fill((0,0,0))
        myfont = pygame.font.SysFont("monospace",40)
        labelscore = myfont.render("SCORE: "+str(Score),1,(255,255,255))
        WindowSurface.blit(labelscore,(10,20))
    
#scalanie płytek
def Merge():
    for i in range(0,Size):
        for j in range(0,Size-1):
            if MatrixGame[i][j] == MatrixGame[i][j+1] and MatrixGame[i][j] != 0:
                MatrixGame[i][j] = MatrixGame[i][j]*2
                MatrixGame[i][j+1] = 0
                Move()
    
#Wykonywanie ruchu
def Move():
    for i in range(0,Size):
        for j in range(0,Size):
            while MatrixGame[i][j] == 0 and sum(MatrixGame[i][j:]) > 0:
                for p in range(j,Size-1):
                    MatrixGame[i][p] = MatrixGame[i][p+1]
                MatrixGame[i][Size-1] = 0
    
#Czy można wykonać ruch
def Check1():
    for i in range(0,Size):
        for j in range(1,Size):
            if MatrixGame[i][j-1] == 0 and MatrixGame[i][j] > 0:
                return True
            elif MatrixGame[i][j-1] == MatrixGame[i][j] and MatrixGame[i][j-1] != 0:
                return True
    return False
     
def Rotate():
    for i in range(0,floor(Size/2)):
        for j in range(i,Size-i-1):
            tmp1 = MatrixGame[i][j]
            tmp2 = MatrixGame[Size-1-j][i]
            tmp3 = MatrixGame[Size-1-i][Size-1-j]
            tmp4 = MatrixGame[j][Size-1-i]
            
            MatrixGame[Size-1-j][i]=tmp1
            MatrixGame[Size-1-i][Size-1-j] = tmp2
            MatrixGame[j][Size-1-i] = tmp3
            MatrixGame[i][j] = tmp4

#sprawdzanie czy można dalej grać czy koniec gry
def Check():
    #sprawdzanie czy są wolne pola
    for i in range(0,Size):
        for j in range(0,Size):
            if MatrixGame[i][j] == 0:
                return True
                
    #sprawdzanie czy po wykonaniu jakiegoś ruchu będą wolne pola
    for i in range(0,Size):
        for j in range(0,Size-1):
            if MatrixGame[i][j] == MatrixGame[i][j+1]:
                return True
            elif MatrixGame[j][i] == MatrixGame[j+1][i]:
                return True
    
    return False
    
def Refresh():
    WindowSurface.fill((0,0,0))
    
    for i in range(0,Size):
        for j in range(0,Size):
            myfont = pygame.font.SysFont("monospace",40)
            #kolor w zależności od tego jaką wartość ma numer
            #zrób z tego funkcję
            if MatrixGame[i][j] == 0:
                pygame.draw.rect(WindowSurface,(205,193,179),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(118,108,97))
            elif MatrixGame[i][j] == 2:
                pygame.draw.rect(WindowSurface,(245,228,218),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(118,108,97))
            elif MatrixGame[i][j] == 4:
                pygame.draw.rect(WindowSurface,(245,224,200),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(119,110,101))
            elif MatrixGame[i][j] == 8:
                pygame.draw.rect(WindowSurface,(245,117,121),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 16:
                pygame.draw.rect(WindowSurface,(245,149,99),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(243,248,239))
            elif MatrixGame[i][j] == 32:
                pygame.draw.rect(WindowSurface,(245,124,95),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(253,244,238))
            elif MatrixGame[i][j] == 64:
                pygame.draw.rect(WindowSurface,(245,95,55),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(250,246,240))
            elif MatrixGame[i][j] == 128:
                pygame.draw.rect(WindowSurface,(245,207,144),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(250,248,251))
            elif MatrixGame[i][j] == 256:
                pygame.draw.rect(WindowSurface,(245,204,97),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(248,244,234))
            elif MatrixGame[i][j] == 2048:
                pygame.draw.rect(WindowSurface,(245,194,46),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(250,249,250))
            else: 
                pygame.draw.rect(WindowSurface,(0,0,0),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(255,255,255))
            
            labelscore = myfont.render("SCORE: "+str(Score),1,(255,255,255))
            WindowSurface.blit(label,(i*(Width/Size)+30,j*(Width/Size)+130))
            WindowSurface.blit(labelscore,(10,20))
            
def addRandom():           
    rand = floor(random() * pow(Size,2)) 
    while MatrixGame[floor(rand/Size)][rand%Size] != 0:
        rand = floor(random() * pow(Size,2))
        
    MatrixGame[floor(rand/Size)][rand%Size] = 2
    
    
#odpalenie funkcji main
main()