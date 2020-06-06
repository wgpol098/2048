import pygame,sys,time
import pyautogui
from pygame.locals import *
from constants import *
from math import *
from AI import *
import datetime

#macierz planszy
MatrixGame = np.zeros((Size,Size), dtype=int)
ListGame = np.zeros(Size*Size, dtype=int)
PreviousListGame = []
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
    global MatrixGame
    global PreviousListGame
    global Score
    global ScorePrevious
    global AI1Flag
    global AI2Flag
    global AI3Flag
    global AI5Flag
    global ListGame   
    ListGame = addRand(ListGame)
    ListGame = addRand(ListGame)
    PreviousListGame = ListGame.copy()
    MatrixGame = ListToMatrix(ListGame)
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
                    if event.key == pygame.K_UP:
                        Move(UP)
                    if event.key == pygame.K_LEFT:
                        Move(LEFT)
                    if event.key == pygame.K_DOWN:
                        Move(DOWN)
                    if event.key == pygame.K_RIGHT:
                        Move(RIGHT)
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
                
        pygame.display.update()            

def Move(move):
    global MatrixGame
    global ScorePrevious
    global Score
    global ListGame
    global PreviousListGame
    if IsSame(ListGame,nextMove(ListGame,move)) == False:
        ScorePrevious = Score
        PreviousListGame = ListGame
        ListGame = nextMove(ListGame,move)
        ListGame = addRand(ListGame)
        Score = ScoreCountL(ListGame)
        MatrixGame = ListToMatrix(ListGame)
 
def addRand(board):
    rand = floor(random() * pow(Size,2)) 
    while board[rand] != 0:
        rand = floor(random() * pow(Size,2))
        
    board[rand]=2
    return board
    
#cofanie planszy
def Undo():
    global MatrixGame
    global Score
    global ScorePrevious
    global ListGame
    global PreviousListGame
    tmps = Score
    tmpp = PreviousListGame.copy()
    PreviousListGame = ListGame.copy()
    ListGame = tmpp
    MatrixGame = ListToMatrix(ListGame)
    Score = ScorePrevious
    ScorePrevious=tmps
    
    
#restart gry
def Restart():
    global MatrixGame
    global ScorePrevious
    global Score
    global ListGame
    global PreviousListGame
    ListGame = np.zeros(Size*Size, dtype=int)
    Score=0
    ScorePrevious=0
    ListGame = addRand(ListGame)
    ListGame = addRand(ListGame)
    PreviousListGame = ListGame.copy()
    MatrixGame = ListToMatrix(ListGame)

#macierz do listy
def MatrixToList(Matrix):
    currentValues = []
    for i in range(0,Size):
        for j in range(0,Size):
            currentValues.append(Matrix[floor((i+Size*j)/Size)][(i+Size*j)%Size])         
    return currentValues
    
#lista do macierzy
def ListToMatrix(List):
    currentValues = np.zeros((Size,Size), dtype=int)
    for i in range(0,Size):
        for j in range(0,Size):
            currentValues[i][j] = List[j*Size+i]
    return currentValues
 
def MoveAI5():
    GetMove(BestMoveAI5(ListGame,4))
#Monte Carlo
def MoveAI3():  
    GetMove(BestMoveAI3(ListGame,10,10)) 
#funkcja odpowiedzialana za ruch sztucznej inteligencji (zachłanne z patrzeniem w przód)
def MoveAI2():
    GetMove(BestMoveAI22(ListGame,3)) 
#zachłanny algorytm, najlepsze wyjście w danej chwili
def MoveAI1():     
    GetMove(BestMoveAI(ListGame))
    
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
                label = myfont.render(str(MatrixGame[i][j]),1,(118,108,97))
            elif MatrixGame[i][j] == 8:
                pygame.draw.rect(WindowSurface,(245,117,121),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 16:
                pygame.draw.rect(WindowSurface,(245,149,99),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 32:
                pygame.draw.rect(WindowSurface,(245,124,95),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 64:
                pygame.draw.rect(WindowSurface,(245,95,55),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 128:
                pygame.draw.rect(WindowSurface,(245,207,144),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 256:
                pygame.draw.rect(WindowSurface,(245,204,97),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 512:
                pygame.draw.rect(WindowSurface,(245,197,91),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 1024:
                pygame.draw.rect(WindowSurface,(245,207,121),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 2048:
                pygame.draw.rect(WindowSurface,(245,194,46),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(247,245,241))
            elif MatrixGame[i][j] == 4096: 
                pygame.draw.rect(WindowSurface,(253,61,59),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(255,255,255))
            else: 
                pygame.draw.rect(WindowSurface,(253,25,30),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                label = myfont.render(str(MatrixGame[i][j]),1,(255,255,255))
            
            labelscore = myfont.render("SCORE: "+str(Score),1,(255,255,255))
            
            if MatrixGame[i][j] > 100 and MatrixGame[i][j] <= 1000:
                WindowSurface.blit(label,(i*(Width/Size)+15,j*(Width/Size)+130))
            elif MatrixGame[i][j] > 1000:
                WindowSurface.blit(label,(i*(Width/Size)+5,j*(Width/Size)+130))
            else:
                WindowSurface.blit(label,(i*(Width/Size)+30,j*(Width/Size)+130))
            
            WindowSurface.blit(labelscore,(10,20))
        
#odpalenie funkcji main
main()