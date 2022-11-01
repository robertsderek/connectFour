import pygame 
import numpy as np
import sys 
import math 
import random


##BOARD##

BLUE = (0,0,255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)
 
num_rows = 6
num_cols = 7

#creates a typical 6*7 Connect Four board
def create_board():
    board = np.zeros((num_rows,num_cols))
    return board
 
#Adds a checker to the board
def add_checker(board, row, col, checker):
    board[row][col] = checker

#removes the top checker of a specified column
def remove_checker(board, col):    
    row = (num_rows - 1)
    while row >= 0: 
        if board[row][col] == 1 or board[row][col] == 2:
            break
        else:
            row -= 1
    board[row][col] = 0
        

#makes sure that we aren't trying to drop a checker in a full column
#returns False if placement is invalid
def can_add_to(board, col):
    if (col >= 0 and col < num_cols) and board[num_rows-1][col] == 0:
        return True
    else:
        return False

#returns True if board is completely full of checkers
def is_full(board):
    for col in range(num_cols):
        if can_add_to(board, col) == True:
            return False  
    return True 

def get_next_open_row(board, col):
    for row in range(num_rows):
        if board[row][col] == 0:
            return row

def get_first_open_col(board):
    for col in range(num_cols):
        if board[num_rows-1][col] == 0:
            return col

 
#prints a board where the elements are reordered
def print_board(board):
    print(np.flip(board, 0))


#checks for a horizontal win
def is_horizontal_win(board, checker):
    for row in range(num_rows):
        for col in range(num_cols - 3):                  
            if (board[row][col] == checker) and (board[row][col + 1] == checker) and (board[row][col + 2] == checker) and (board[row][col + 3] == checker):
                return True 
    return False

#checks for a vertical win
def is_vertical_win(board, checker):
    for row in range(num_rows-3):
        for col in range(num_cols):
            if (board[row][col] == checker) and (board[row+1][col] == checker) and (board[row+2][col] == checker) and (board[row+3][col] == checker):
                return True
    return False

#checks for a down diagonal win
def is_down_diagonal_win(board, checker):
    for row in range(num_rows - 3):
        for col in range(num_cols - 3):                  
            if (board[row][col] == checker) and (board[row + 1][col + 1] == checker) and (board[row + 2][col + 2] == checker) and (board[row + 3][col + 3] == checker):
                return True  
    return False
        
#checks for an up diagonal win
def is_up_diagonal_win(board, checker):
    for row in range(3, num_rows):
        for col in range(num_cols - 3):                  
            if (board[row][col] == checker) and (board[row - 1][col + 1] == checker) and (board[row - 2][col + 2] == checker) and (board[row - 3][col + 3] == checker):
                return True     
    return False

#checks for a win
def is_win(board, checker):
    if (is_horizontal_win(board, checker)) or (is_vertical_win(board, checker)) or (is_down_diagonal_win(board, checker)) or (is_up_diagonal_win(board, checker)):
        return True
    else:
        return False 


def draw_board(board):
    #define our screen size
    SQUARESIZE = 100
    RADIUS = int(SQUARESIZE/2 - 5)

    #define width and height of board
    width = (num_cols) * SQUARESIZE
    height = (num_rows+1) * SQUARESIZE
    size = (width, height)

    screen = pygame.display.set_mode(size)


    for col in range(num_cols):
        for row in range(num_rows):
            pygame.draw.rect(screen, BLUE, (col*SQUARESIZE, row*SQUARESIZE+SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE+SQUARESIZE/2)), RADIUS)
     
    for c in range(num_cols):
        for r in range(num_rows):      
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
            elif board[r][c] == 2: 
                pygame.draw.circle(screen, YELLOW, (int(c*SQUARESIZE+SQUARESIZE/2), height-int(r*SQUARESIZE+SQUARESIZE/2)), RADIUS)
    pygame.display.update()


##AI PLAYER##

class AIPlayer:
# a class that represents an intelligent AI  player which picks the move with the best known outcome. 

    def __init__(self, checker, lookahead):
        #constructs a new AI player object
        assert(checker == 2 or checker == 1)
        assert(lookahead >= 0)
        
        self.checker = checker
        self.lookahead = lookahead
        

    def max_score_column(self, scores):
        # takes a list scores containing a score for each column of the board, and that returns the index of the column with the maximum score

        scorelist = [] 
        
        maxscore = max(scores)
        for i in range(len(scores)):
            if scores[i] == maxscore:
                scorelist += [i]
        
        return random.choice(scorelist)
                
    
    def scores_for(self, board):
        scores = [50] * num_cols
        if self.checker == 2:
            opponent_checker = 1
        else:
            opponent_checker = 2
            
        for col in range(num_cols):
            if can_add_to(board, col) == False:
                scores[col] = -1
            elif is_win(board, self.checker) == True:
                scores[col] = 100
            elif is_win(board, opponent_checker) == True:
                scores[col] = 0
            elif self.lookahead == 0:
                scores[col] = 50
            else:
                add_checker(board, (get_next_open_row(board, col)), col, self.checker)   
                opponent = AIPlayer(opponent_checker, self.lookahead - 1)
                opponent_scores = opponent.scores_for(board)
                if max(opponent_scores) == 100:
                    scores[col] = 0
                elif max(opponent_scores) == 0:
                    scores[col] = 100
                elif max(opponent_scores) == 50:
                    scores[col] = 50
                remove_checker(board, col)
        return scores
                    
    def next_move(self, b):
        scores = self.scores_for(b)   
        return self.max_score_column(scores)
        


##GAME AND MENUS##

def playGame(mode):

    #initialize board
    board = create_board()
    print_board(board)
    game_over = False
    turn = 0

    pygame.init()

    #define our screen size
    SQUARESIZE = 100

    #define width and height of board
    width = (num_cols) * SQUARESIZE
    height = (num_rows+1) * SQUARESIZE
    size = (width, height)

    RADIUS = int(SQUARESIZE/2 - 5)
 

    screen = pygame.display.set_mode(size)

    #Calling function draw_board again
    draw_board(board)
    pygame.display.update()


    # change caption based on difficulty
    if mode == 44:
        pygame.display.set_caption('Connect Four - Easy')
    elif mode == 50:
        pygame.display.set_caption('Connect Four - Medium')
    elif mode == 58:
        pygame.display.set_caption('Connect Four - Hard')
    elif mode == 64:
        pygame.display.set_caption('Connect Four - PvP')
 
    myfont = pygame.font.SysFont("monospace", 50)


    while not game_over:
 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
 
            if event.type == pygame.MOUSEMOTION:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                posx = event.pos[0]
                if turn == 0:
                    pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE/2)), RADIUS)
                else: 
                    pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE/2)), RADIUS)
            pygame.display.update()
 
            if event.type == pygame.MOUSEBUTTONUP:
                pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
                #print(event.pos)
                # Ask for Player 1 Input
                if turn == 0:
                    posx = event.pos[0]
                    col = int(math.floor(posx/SQUARESIZE))

                    #makes sure you can add to the intended column
                    if can_add_to(board, col):
                        row = get_next_open_row(board, col)
                        add_checker(board, row, col, 1)
 
                        #checks if you won and the game must end
                        if is_win(board, 1):
                            label = myfont.render("Player 1 wins!!", 1, RED)
                            game_over = True

                        #checks if the board is full and the game must end
                        if is_full(board):
                            game_over = True

                    #if you are adding to a full column, the game place a checker in first open column instead
                    else:
                            col = get_first_open_col(board)
                            row = get_next_open_row(board,col)
                            add_checker(board, row, col, 2)

 
 
                #Ask for Player 2 Input
                else:

                    #if playing against easy AI
                    if mode == 44:
                        bot = AIPlayer(2,1)
                        col = bot.next_move(board)
                        row = get_next_open_row(board, col)
                        add_checker(board, row, col, 2)

                        if is_win(board, 2):
                            label = myfont.render("The AI Wins!!", 1, YELLOW)
                            game_over = True
                            
                        if is_full(board):
                            game_over = True


                    #if playing against medium AI
                    if mode == 50:
                        bot = AIPlayer(2,2)
                        col = bot.next_move(board)
                        row = get_next_open_row(board, col)
                        add_checker(board, row, col, 2)

                        if is_win(board, 2):
                            label = myfont.render("The AI Wins!!", 1, YELLOW)
                            game_over = True
                            
                        if is_full(board):
                            game_over = True


                    #if playing against hard AI
                    if mode == 58:
                        bot = AIPlayer(2, 4)
                        col = bot.next_move(board)
                        row = get_next_open_row(board, col)
                        add_checker(board, row, col, 2)

                        if is_win(board, 2):
                            label = myfont.render("The AI Wins!!", 1, YELLOW)
                            game_over = True
                            
                        if is_full(board):
                            game_over = True


                    # If playing PVP
                    if mode == 64:               
                        posx = event.pos[0]
                        col = int(math.floor(posx/SQUARESIZE))

 
                        if can_add_to(board, col):
                            row = get_next_open_row(board, col)
                            add_checker(board, row, col, 2)
 
                            if is_win(board, 2):
                                label = myfont.render("Player 2 wins!!", 1, YELLOW)
                                game_over = True
                            
                            if is_full(board):
                                game_over = True

                        else:
                            col = get_first_open_col(board)
                            row = get_next_open_row(board,col)
                            add_checker(board, row, col, 2)


                print_board(board)
                draw_board(board)
 
                turn += 1
                turn = turn % 2
 
                if game_over:
                    screen.blit(label, (40,10))
                    pygame.display.update()
                    pygame.time.wait(3000)
                    main()



def difficultyMenu():
    # difficulty menu
    pygame.init() # initializing the constructor   
    res = (720,720) # screen resolution 

    screen = pygame.display.set_mode(res) # opens up a window 
    pygame.display.set_caption('Difficulty Menu')
    clock = pygame.time.Clock()

    color_light = (170,170,170) # light shade of the button 
    color_dark = (100,100,100) # dark shade of the button
    txtColor = (18, 196, 255) # color of text
    btnColor = (255,255,255) # color of buttons
    quitColor = (255, 0, 0) #color of quit
    title2 = pygame.font.SysFont('Georgia', 50)
    # menu text
    title2Card = title2.render("Choose your difficulty", True, txtColor)
    button = pygame.font.SysFont('Verdana', 35) 
    easyBut = button.render('Easy', True, btnColor) 
    medBut = button.render('Medium', True, btnColor) 
    hardBut = button.render('Hard', True, btnColor) 
    pvpBut = button.render('PvP', True, btnColor) 
    quitBut = button.render('Quit', True, quitColor)

    while True:       

        #stars background and format to fit
        stars = pygame.image.load("/Users/derekroberts/Documents/GitHub/connectFour/images/stars.jpeg").convert()
        stars = pygame.transform.scale(stars, (720, 720))
        scroll = 0
        tiles = math.ceil(720 / stars.get_width()) + 1
  
        #scrolling loop
        while 1:
            #speed
            clock.tick(20)
  
            #appending image to back of same image
            i = 0
            while(i < tiles):
                screen.blit(stars, (stars.get_width()*i + scroll, 0))
                i += 1

            #frame for scrolling
            scroll -= 6
  
            #reset the frams
            if abs(scroll) > stars.get_width():
                scroll = 0


            mouse = pygame.mouse.get_pos()   # stores the (x,y) coordinates into the variable as a tuple    
            for event in pygame.event.get(): 
                if event.type == pygame.QUIT: 
                    pygame.quit()  
                #checks if a mouse is clicked 
                if event.type == pygame.MOUSEBUTTONUP:
                    if 280 <= mouse[0] <= 420 and 220 <= mouse[1] <= 260: 
                        playGame(44) # easy
                    elif 280 <= mouse[0] <= 420 and 320 <= mouse[1] <= 360: 
                        playGame(50) # medium
                    elif 280 <= mouse[0] <= 420 and 420 <= mouse[1] <= 460: 
                        playGame(58) # hard
                    elif 280 <= mouse[0] <= 420 and 520 <= mouse[1] <= 560:
                        playGame(64) # pvp
                    elif 280 <= mouse[0] <= 420 and 620 <= mouse[1] <= 660:
                        pygame.quit() # quit

            # if mouse is hovered on a button it changes to lighter shade 
            if 280 <= mouse[0] <= 420 and 220 <= mouse[1] <= 260:
                pygame.draw.rect(screen,color_light,[280,220,140,40]) 
            elif 280 <= mouse[0] <= 420 and 320 <= mouse[1] <= 360: 
                pygame.draw.rect(screen,color_light,[280,320,140,40]) 
            elif 280 <= mouse[0] <= 420 and 420 <= mouse[1] <= 460: 
                pygame.draw.rect(screen,color_light,[280,420,140,40]) 
            elif 280 <= mouse[0] <= 420 and 520 <= mouse[1] <= 560: 
                pygame.draw.rect(screen,color_light,[280,520,140,40]) 
            elif 280 <= mouse[0] <= 420 and 620 <= mouse[1] <= 660: 
                pygame.draw.rect(screen,color_light,[280,620,140,40]) 
            else:
                pygame.draw.rect(screen,color_dark,[280,220,140,40]) 
                pygame.draw.rect(screen,color_dark,[280,320,140,40]) 
                pygame.draw.rect(screen,color_dark,[280,420,140,40]) 
                pygame.draw.rect(screen,color_dark,[280,520,140,40]) 
                pygame.draw.rect(screen,color_dark,[280,620,140,40])  
        
            # superimposing the text onto our button 
            screen.blit(easyBut, (305, 216))
            screen.blit(medBut, (281, 316))
            screen.blit(hardBut, (305, 418)) 
            screen.blit(pvpBut, (315, 518))  
            screen.blit(quitBut, (305, 616))
            screen.blit(title2Card, (120, 129))  
      
            pygame.display.update() # updates the frames of the game 



def main():

    #initalize pygame
    pygame.init()
    res = (720,720)

    screen = pygame.display.set_mode(res) # opens up a window 
    pygame.display.set_caption('Main Menu')
    clock = pygame.time.Clock()

    color_light = (170,170,170) # light shade of the button 
    color_dark = (100,100,100) # dark shade of the button 
    txtColor = (18, 196, 255) # color of text
    title = pygame.font.SysFont('Georgia', 60)
    button = pygame.font.SysFont('Verdana', 35) # fonts for text
    info = pygame.font.SysFont('Verdana', 22)
    
    # main menu info
    titleCard = title.render("Derek's Connect Four", True, txtColor)
    startButton = button.render('Start' , True , (0,255,0)) 
    quitButton = button.render('Quit' , True , (255,0,0)) 
    info1 = info.render('Hello and welcome to my Connect Four game! All standard', True, txtColor) 
    info2 = info.render('Connect Four rules apply. To place a checker simply click', True, txtColor) 
    info3 = info.render('above the column you wish to drop it in.', True, txtColor) 
    info4 = info.render('You can play against an AI opponent or one of your friends!', True, txtColor)     

    while True: 

        #stars background and format to fit
        stars = pygame.image.load("/Users/derekroberts/Documents/GitHub/connect_four/images/stars.jpeg").convert()
        stars = pygame.transform.scale(stars, (720, 720))
        scroll = 0
        tiles = math.ceil(720 / stars.get_width()) + 1
  
        #scrolling loop
        while 1:
            #speed
            clock.tick(20)
  
            #appending image to back of same image
            i = 0
            while(i < tiles):
                screen.blit(stars, (stars.get_width()*i + scroll, 0))
                i += 1

            #frame for scrolling
            scroll -= 6
  
            #reset the frams
            if abs(scroll) > stars.get_width():
                scroll = 0

            mouse = pygame.mouse.get_pos() # stores the (x,y) coordinates into the variable as a tuple 
            for event in pygame.event.get(): # any action from user
                if event.type == pygame.QUIT: # quits game
                    pygame.quit()       
                if event.type == pygame.MOUSEBUTTONUP: # checks if a mouse is clicked 
                    if 280 <= mouse[0] <= 420 and 360 <= mouse[1] <= 400: 
                        difficultyMenu() # sends user to difficulty menu
                    if 280 <= mouse[0] <= 420 and 460<= mouse[1] <= 500: 
                        pygame.quit() 

            # if mouse is hovered on a button it changes to lighter shade 
            if 280 <= mouse[0] <= 420 and 360 <= mouse[1] <= 400: 
                pygame.draw.rect(screen,color_light,[280,360,140,40])
            
            elif 280 <= mouse[0] <= 420 and 460 <= mouse[1] <= 500: 
                pygame.draw.rect(screen,color_light,[280,460,140,40]) 
            else:
                pygame.draw.rect(screen,color_dark,[280,360,140,40]) 
                pygame.draw.rect(screen,color_dark,[280,460,140,40]) 

            # superimposing the text onto our button 
            screen.blit(startButton, (303,356))
            screen.blit(quitButton, (310, 455)) 
            screen.blit(info1, (20,535))  
            screen.blit(info2, (20,560))  
            screen.blit(info3, (20,585))  
            screen.blit(info4, (20,630))  
            screen.blit(titleCard, (50, 120))
                
            pygame.display.update() # updates the frames of the game 

main() # starts program
