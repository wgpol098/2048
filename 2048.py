import pygame,sys,time
import pyautogui
from pygame.locals import *
from constants import *
from math import *
from AI import *
import datetime
import time 

#lista punktow
ListGame = np.zeros(Size*Size, dtype=int)
PreviousListGame = []
#licznik punktów
Score = 0
#Wynik krok wcześniej
ScorePrevious = 0

#inicjalizacja pygame
pygame.init()

#WindowSurface
WindowSurface = pygame.display.set_mode((Width,Height),0,32)
pygame.display.set_caption("2048")


def main():
    global ListGame,PreviousListGame,Score,ScorePrevious
    ListGame = addRand(ListGame)
    ListGame = addRand(ListGame)
    PreviousListGame = ListGame.copy()
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
                        
                    if event.key == pygame.K_1:
                        check = True
                        while(check == True):
                            Move(BestMoveAI(ListGame)) 
                            Refresh()        
                            pygame.display.update() 
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == pygame.K_1:
                                        check = False
                            if (Check() == False or check == False):
                                check=False
                    elif event.key == pygame.K_2:
                        check = True
                        while(check == True):
                            Move(BestMoveAI22(ListGame,3)) 
                            Refresh()        
                            pygame.display.update() 
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == pygame.K_2:
                                        check = False
                            if (Check() == False or check == False):
                                check=False
                    elif event.key == pygame.K_3:
                        check = True
                        while(check == True):
                            Move(BestMoveAI3(ListGame,100,10)) 
                            Refresh()        
                            pygame.display.update() 
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == pygame.K_3:
                                        check = False
                            if (Check() == False or check == False):
                                check=False
                    elif event.key == pygame.K_5:
                        check = True
                        while(check == True):
                            Move(BestMoveAI5(ListGame,4)) 
                            Refresh()        
                            pygame.display.update() 
                            for event in pygame.event.get():
                                if event.type == KEYDOWN:
                                    if event.key == pygame.K_5:
                                        check = False
                            if (Check() == False or check == False):
                                check=False
                   
                    #cofnięcie ruchu
                    elif event.key == pygame.K_c:
                        Undo()
                    #restart gry
                    elif event.key == pygame.K_r:
                        Restart() 
            #przegrana gra        
            else:
                if event.type == KEYDOWN:
                    if event.key == pygame.K_r:
                        Restart()
                  
        Refresh()        
        pygame.display.update()            

def Move(move):
    global ListGame,PreviousListGame,Score,ScorePrevious
    if IsSame(ListGame,nextMove(ListGame,move)) == False:
        ScorePrevious = Score
        PreviousListGame = ListGame
        ListGame = nextMove(ListGame,move)
        ListGame = addRand(ListGame)
        Score = ScoreCountL(ListGame)
 
def addRand(board):
    rand = floor(random() * pow(Size,2)) 
    while board[rand] != 0:
        rand = floor(random() * pow(Size,2))
        
    board[rand]=2
    return board
    
#cofanie planszy
def Undo():
    global ListGame,PreviousListGame,Score,ScorePrevious
    tmps = Score
    tmpp = PreviousListGame.copy()
    PreviousListGame = ListGame.copy()
    ListGame = tmpp
    Score = ScorePrevious
    ScorePrevious=tmps
    
    
#restart gry
def Restart():
    global ListGame,PreviousListGame,Score,ScorePrevious
    ListGame = np.zeros(Size*Size, dtype=int)
    Score=0
    ScorePrevious=0
    ListGame = addRand(ListGame)
    ListGame = addRand(ListGame)
    PreviousListGame = ListGame.copy()   
     
#sprawdzanie czy można dalej grać czy koniec gry
def Check():
    #sprawdzanie czy są wolne pola
    for i in range(0,Size*Size):
        if ListGame[i] == 0:
            return True
    
    #DO ANALIZY
    
    
    #sprawdzanie czy po wykonaniu jakiegoś ruchu będą wolne pola
    for i in range(0,Size):
        for j in range(0,Size-1):
            if ListGame[Size*j+i] == ListGame[Size*j+i+1]:
                return True
            elif ListGame[Size*j+i] == ListGame[Size*(j+1)+i]:
                return True
    
    return False
    
def Refresh():
    WindowSurface.fill((0,0,0))
    
    for i in range(0,Size):
        for j in range(0,Size):
            myfont = pygame.font.SysFont("monospace",40)
            if ListGame[Size*j+i] == 0:
                pygame.draw.rect(WindowSurface,(205,193,179),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))                
            elif ListGame[Size*j+i] == 2:
                pygame.draw.rect(WindowSurface,(245,228,218),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 4:
                pygame.draw.rect(WindowSurface,(245,224,200),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 8:
                pygame.draw.rect(WindowSurface,(245,117,121),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 16:
                pygame.draw.rect(WindowSurface,(245,149,99),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 32:
                pygame.draw.rect(WindowSurface,(245,124,95),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 64:
                pygame.draw.rect(WindowSurface,(245,95,55),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 128:
                pygame.draw.rect(WindowSurface,(245,207,144),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 256:
                pygame.draw.rect(WindowSurface,(245,204,97),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 512:
                pygame.draw.rect(WindowSurface,(245,197,91),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 1024:
                pygame.draw.rect(WindowSurface,(245,207,121),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 2048:
                pygame.draw.rect(WindowSurface,(245,194,46),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            elif ListGame[Size*j+i] == 4096: 
                pygame.draw.rect(WindowSurface,(253,61,59),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
            else: 
                pygame.draw.rect(WindowSurface,(253,25,30),(i*(Width/Size),j*(Width/Size)+100,Width/Size,Width/Size))
                
                
            if ListGame[Size*j+i] < 8:
                label = myfont.render(str(ListGame[Size*j+i]),1,(118,108,97))
            elif ListGame[Size*j+i] < 4096:
                label = myfont.render(str(ListGame[Size*j+i]),1,(247,245,241))
            else:
                label = myfont.render(str(ListGame[Size*j+i]),1,(255,255,255))
                
            labelscore = myfont.render("SCORE: "+str(Score),1,(255,255,255))
            
            if ListGame[Size*j+i] > 100 and ListGame[Size*j+i] <= 1000:
                WindowSurface.blit(label,(i*(Width/Size)+15,j*(Width/Size)+130))
            elif ListGame[Size*j+i] > 1000:
                WindowSurface.blit(label,(i*(Width/Size)+5,j*(Width/Size)+130))
            else:
                WindowSurface.blit(label,(i*(Width/Size)+30,j*(Width/Size)+130))
            
            WindowSurface.blit(labelscore,(10,20))
    
main()