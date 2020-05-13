import pygame,sys,time
import pyautogui
from pygame.locals import *
from constants import *
from math import *
from AI import *
import datetime

#macierz planszy
MatrixGame = np.zeros((Size,Size), dtype=int)
#Macierz planszy ruch wcześniej
MatrixPreviousGame = np.zeros((Size,Size), dtype=int)
#licznik punktów
Score = 0
#Wynik krok wcześniej
ScorePrevious = 0
#Flagi dla AI
AI1Flag = False
AI2Flag = False
AI3Flag = False
AI5Flag = False


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
    global AI5Flag
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
                            AI5Flag=False
                    if event.key == pygame.K_2:
                        #zachałanny z patrzeniem w przód
                        if AI2Flag == True:
                            AI2Flag=False
                        else:
                            AI2Flag=True
                            AI1Flag=False
                            AI3Flag=False
                            AI5Flag=False
                    if event.key == pygame.K_3:
                        #patrzenie w przód monte carlo
                        if AI3Flag == True:
                            AI3Flag=False
                        else:
                            AI3Flag=True
                            AI1Flag=False
                            AI2Flag=False
                            AI5Flag=False
                    if event.key == pygame.K_5:
                        #z agentemi i inną oceną
                        if AI5Flag == True:
                            AI5Flag=False
                        else:
                            AI5Flag=True
                            AI1Flag=False
                            AI2Flag=False
                            AI3Flag=False
                    
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
                    if AI5Flag == True:
                        MoveAI5()
                        
                    #restart gry
                    if event.key == pygame.K_r:
                        Restart()
                        
                    #cofnięcie ruchu
                    if event.key == pygame.K_c:
                        Undo()
                    Refresh()
            #przegrana gra        
            else:
                AI1Flag=False
                AI2Flag=False
                AI3Flag=False
                AI5Flag=False
                if event.type == KEYDOWN:
                    if event.key == pygame.K_r:
                        Restart()
                #GameOver()
                
        pygame.display.update()            
 
#cofanie planszy
def Undo():
    global MatrixGame
    global MatrixPreviousGame
    global Score
    global ScorePrevious
    tmp = np.copy(MatrixGame)
    tmps = Score
    MatrixGame = np.copy(MatrixPreviousGame)
    MatrixPreviousGame = np.copy(tmp)
    Score = ScorePrevious
    ScorePrevious=tmps
    
#restart gry
def Restart():
    global MatrixGame
    global Score
    MatrixGame = np.zeros((Size,Size),dtype=int)
    Score=0
    addRandom()
    addRandom()

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

def MatrixToList(Matrix):
    currentValues = []
    for i in range(0,Size):
        for j in range(0,Size):
            currentValues.append(Matrix[floor((i+Size*j)/Size)][(i+Size*j)%Size])         
    return currentValues
    
 
def MoveAI5():
    GetMove(BestMoveAI5(MatrixToList(MatrixGame),4))
#Monte Carlo
def MoveAI3():  
    GetMove(BestMoveAI3(MatrixToList(MatrixGame),10,10)) 
#funkcja odpowiedzialana za ruch sztucznej inteligencji (zachłanne z patrzeniem w przód)
def MoveAI2():
    GetMove(BestMoveAI22(MatrixToList(MatrixGame),3)) 
#zachłanny algorytm, najlepsze wyjście w danej chwili
def MoveAI1():     
    GetMove(BestMoveAI(MatrixToList(MatrixGame)))
    
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
            elif MatrixGame[i][j] == 512:
                pygame.draw.rect(WindowSurface,(245,197,91),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(248,242,229))
            elif MatrixGame[i][j] == 1024:
                pygame.draw.rect(WindowSurface,(245,207,121),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(248,242,224))
            elif MatrixGame[i][j] == 2048:
                pygame.draw.rect(WindowSurface,(245,194,46),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(250,249,250))
            elif MatrixGame[i][j] == 4096: 
                pygame.draw.rect(WindowSurface,(253,61,59),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(255,255,255))
            else: 
                pygame.draw.rect(WindowSurface,(253,25,30),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(255,255,255))
            
            labelscore = myfont.render("SCORE: "+str(Score),1,(255,255,255))
            WindowSurface.blit(label,(i*(Width/Size)+30,j*(Width/Size)+130))
            WindowSurface.blit(labelscore,(10,20))
            
def addRandom():           
    rand = floor(random() * pow(Size,2)) 
    rand2 = random()
    while MatrixGame[floor(rand/Size)][rand%Size] != 0:
        rand = floor(random() * pow(Size,2))
        
    MatrixGame[floor(rand/Size)][rand%Size] = 2
    
    
#odpalenie funkcji main
main()