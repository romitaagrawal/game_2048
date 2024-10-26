import pygame                     #pygame is a cross platform set of python modules designed for writing video games using python programming language
import random
pygame.init()

#(1)  initial set-up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH , HEIGHT])   #display set up
pygame.display.set_caption('2048')                   #display caption
timer = pygame.time.Clock()                          #it is a type of function to set frame rate
fps = 60                                             #frames per second
font = pygame.font.Font('freesansbold.ttf', 24)      #pygame comes with default font and this sentence is used to initialise the fond and freesansbold is a type of font

#(color) 2048 game colour library                           #this whole library code are like spcefic color codes for each number tile in the game , numbers are available online 
colors = {0:(204, 192, 179),
          2:(238, 228,218),
          4:(237, 224, 200),
          8:(242, 177,121),
          16:(245, 149, 99),
          32:(246, 124, 59),
          64:(246, 94, 59),
          128:(237, 207, 114),
          256:(237, 204,97),
          512:(237, 200, 80),
          1024:(237, 197, 63),
          2048:(237, 194, 46),
          'light text':(246, 246, 242),
          'dark text':(119, 110, 101),
          'other':(0, 0, 0),
          'bg':(187, 173, 160)}

#(3)  game variable initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
score = 0

#(8) draw game over and restart text
def draw_over():                                                       #this shows a little rectangular box which says games over and if u wanna restart press enter
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


#(7)  take our turns based on directions
def take_turn(direc, board):
    global score
    merged = [[False for _ in range(4)] for _ in range(4)]                    #here this function is made to move the numbers to top of the screen known by shift command
    if direc == 'UP':                                                         #if number is 2 is is shifted upwards it add and becomes no 2 if the no. 4 is already there and 2 have been added in that step then 4 and 4 wont add theselves like one addition at a time     
        for i in range(4):                                                    #same goes for other numbers and if there is no shift then it means theere is no space for shift or addition and simly one block of no. will be added 
            for j in range(4):
                shift = 0
                if i > 0:
                    for q in range(i):
                        if board[q][j] == 0:
                            shift += 1
                    if shift > 0:
                        board[i - shift][j] = board[i][j]
                        board[i][j] = 0
                    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
                            and not merged[i - shift - 1][j]:
                        board[i - shift - 1][j] *= 2                #in this line here we add the 2 times of the number to our score board to keep track of our game 
                        score += board[i - shift - 1][j]
                        board[i - shift][j] = 0
                        merged[i - shift - 1][j] = True

    elif direc == 'DOWN':                                                    #it works on the same principle as UP key just instead of upward motion no.s moves in downward motion
        for i in range(3):
            for j in range(4):
                shift = 0
                for q in range(i + 1):
                    if board[3 - q][j] == 0:
                        shift += 1
                if shift > 0:
                    board[2 - i + shift][j] = board[2 - i][j]
                    board[2 - i][j] = 0
                if 3 - i + shift <= 3:
                    if board[2 - i + shift][j] == board[3 - i + shift][j] and not merged[3 - i + shift][j] \
                            and not merged[2 - i + shift][j]:
                        board[3 - i + shift][j] *= 2
                        score += board[3 - i + shift][j]
                        board[2 - i + shift][j] = 0
                        merged[3 - i + shift][j] = True

    elif direc == 'LEFT':                                           #it also works on the same principle but instead of upward movement blocks moves toward the left of the screen
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][j - shift] = board[i][j]
                    board[i][j] = 0
                if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
                        and not merged[i][j - shift]:
                    board[i][j - shift - 1] *= 2
                    score += board[i][j - shift - 1]
                    board[i][j - shift] = 0
                    merged[i][j - shift - 1] = True

    elif direc == 'RIGHT':                                         #it also works on the same principle but the block of numbers moves toward the right of the screen
        for i in range(4):
            for j in range(4):
                shift = 0
                for q in range(j):
                    if board[i][3 - q] == 0:
                        shift += 1
                if shift > 0:
                    board[i][3 - j + shift] = board[i][3 - j]
                    board[i][3 - j] = 0
                if 4 - j + shift <= 3:
                    if board[i][4 - j + shift] == board[i][3 - j + shift] and not merged[i][4 - j + shift] \
                            and not merged[i][3 - j + shift]:
                        board[i][4 - j + shift] *= 2
                        score += board[i][4 - j + shift]
                        board[i][3 - j + shift] = 0
                        merged[i][4 - j + shift] = True
    return board



#(6)  spawn in new pieces randomly when turns start
def new_pieces(board):                                    #this whole set of code basically checks if there is a empty space in any row and if yes then it gives another number in the row 
    count = 0                                             #if the values in the row is less than or equal to 10 then it gives number 4 else 2 and if there is no space left then it gives full
    full = False
    while any(0 in row for row in board) and count < 1:
         row = random.randint(0, 3)
         col = random.randint(0, 3)
         if board[row][col] == 0:
             count += 1
             if random.randint(1, 10) == 10:
                 board[row][col] = 4
             else:
                 board[row][col] = 2
    if count < 1 :
         full = True

    return board, full

#(4)  draw background for the board
def draw_board():
    pygame.draw.rect(screen,colors['bg'],[0,0,400,400],0,10) #the first round bracket is used to give colour to the rectangle we made and next box bracket is size of rectangle
    score_text = font.render(f'Score: {score}', True, 'black')
    screen.blit(score_text, (10, 410))
    pass


#(5)  draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <=2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)   #this is used to make smaller boxes for our texts
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5* value_len))       #here it reduces the font of the number as the number gets bigger so 48 is the base line and it reduces it by 5 times of value length
                value_text = font.render(str(value), True, value_color)                # font render helps displaying the number onto another surface
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))   # keeps font in the centre of the rectangle
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)  #it gives our boxes an otline of size 2       

#(2)  main game loop
run = True
while run:
    timer.tick(fps)                                  #initialise frame rate
    screen.fill('gray')                              #fills the backgroung colour
    draw_board()                                    #its like a background where we can put our score and highscore  
    draw_pieces(board_values)
    if spawn_new or init_count < 2:                       # it is the initialization for new pieces in the game it runs the loop 2 times in the start as we need atleat 2 number at the start of the game 
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':                                    # here it says if dirrection is not equal to empty string the add another spawn piece to the game 
        board_value = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:                                   # here when game is over it keeps track of our high scores in the text file that we made by rewritting and arranging the scores
        draw_over()
        
    for event in pygame.event.get():                 #it is used to register all ebents from user into queue which can be recieved with code
        if event.type == pygame.QUIT:                #here quit is basically the red cross over the screen used to close the window
            run = False                              #this for function here is used to end the while infinite loop 
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:             #here we have declared another event whether the key is moving upward or in anyother direction
                direction = 'UP'                     #we have assigned the direction to different variable
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

    if game_over:                                   # here when games is over it reaaranges the whole set up to its initial dehault set up that is all zeros
                if event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    score = 0
                    direction = ''
                    game_over = False

    
       
    pygame.display.flip()                           #used to display the whole set up on the screen {flip means show} 
pygame.quit()
    
  
