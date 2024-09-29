# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license
# Modified by elizabethkushelevsky
# 11/3/21

# "YELLOW", "BLUE", "DARKBLUE", "PURPLE", and "VIOLET" colors generated on coolors.co
# pygame.font.SysFont method for finding pre-downloaded fonts found at https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font
# Deletion method for key-value pairs found at https://www.geeksforgeeks.org/python-delete-items-from-dictionary-while-iterating/
# Edited with in-person and video help from Mr. Pound

import pygame
import random
import sys

from pygame.locals import *

FPS = 15
COMPUTERFPS = 30
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
CELLSIZE = 20
assert WINDOWWIDTH % CELLSIZE == 0, "Window width must be a multiple of cell size."
assert WINDOWHEIGHT % CELLSIZE == 0, "Window height must be a multiple of cell size."
CELLWIDTH = int(WINDOWWIDTH / CELLSIZE)
CELLHEIGHT = int(WINDOWHEIGHT / CELLSIZE)
level = None


#             R    G    B
WHITE     = (255, 255, 255)
BLACK     = (  0,   0,   0)
RED       = (255,   0,   0)
DARKRED   = ( 82,  16,  12)
worm_color= [  0, 255,   0]
GREEN     = (  0, 255,   0)
DARKGREEN = (  0, 155,   0)
DARKGRAY  = ( 40,  40,  40)
YELLOW    = (240, 189,  45)
BLUE      = ( 94, 145, 199)
DARKBLUE  = (  4,  53, 101)
PURPLE    = ( 52,  22,  26)
VIOLET    = (182, 166, 219)
BGCOLOR = BLUE

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

HEAD = 0 # syntactic sugar: index of the worm's head

scores_dict = {}
scores = []


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Wormy')

    showStartScreen()
    while True:
        show_menu()
        runGame()
        showGameOverScreen()

def show_menu():
    global level

    title_font = pygame.font.SysFont("markerfelt", 40)
    body_font = pygame.font.SysFont("lucidagrande", 20)
    menu_header = title_font.render("MAIN MENU", True, WHITE)
    easy_option = body_font.render("1. Play Level 1: Easy", True, DARKBLUE)
    medium_option = body_font.render("2. Play Level 2: Medium", True, BLACK)
    hard_option = body_font.render("3. Play Level 3: Hard", True, DARKRED)
    high_scores = body_font.render("4. Show High Scores", True, YELLOW)
    instructions = body_font.render("5. See the Instructions", True, VIOLET)
    exit = body_font.render("6. Exit Wormy", True, WHITE)

    # fill background
    DISPLAYSURF.fill(BLUE)

    # block image transfer
    DISPLAYSURF.blit(menu_header, ((WINDOWWIDTH/2) -105, 40))
    DISPLAYSURF.blit(easy_option, ((WINDOWWIDTH/2) -105, 100))
    DISPLAYSURF.blit(medium_option, ((WINDOWWIDTH/2) -120, 150))
    DISPLAYSURF.blit(hard_option, ((WINDOWWIDTH/2) -112, 200))
    DISPLAYSURF.blit(high_scores, ((WINDOWWIDTH/2) -110, 250))
    DISPLAYSURF.blit(instructions, ((WINDOWWIDTH/2) -110, 300))
    DISPLAYSURF.blit(exit, ((WINDOWWIDTH/2) -85, 350))
    pygame.display.update()

    # event processing loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                 sys.exit()
            if event.type == (KEYUP):
                if event.key == pygame.K_1:
                    level = 1
                    return
                elif event.key == pygame.K_2:
                    level = 2
                    return
                elif event.key == pygame.K_3:
                    level = 3
                    return
                elif event.key == pygame.K_4:
                    show_high_scores()
                    return
                elif event.key == pygame.K_5:
                    show_instructions()
                    return
                elif event.key == pygame.K_6:
                    sys.exit()

def show_high_scores():

    # fill background
    DISPLAYSURF.fill(YELLOW)

    title_font = pygame.font.SysFont("markerfelt", 40)
    body_font = pygame.font.SysFont("lucidagrande", 20)
    scores_header = title_font.render("HIGH SCORES", True, WHITE)

    # block image transfer
    DISPLAYSURF.blit(scores_header, ((WINDOWWIDTH/2) -105, 40))

    # only show top 5 scores
    # for j in scores_dict.keys():
    for j in scores:
        if int(j) > 5:
            # del scores_dict[int(j)]
            del scores[j+1]



    # display high scores list
    for i in range(len(scores)):
        high_score = body_font.render((str(scores[i])), True, WHITE)
        DISPLAYSURF.blit(high_score, ((WINDOWWIDTH/2) +50, 100 + (i*30)))

    pygame.display.update()

    score_position1 = body_font.render("1:", True, WHITE)
    score_position2 = body_font.render("2:", True, WHITE)
    score_position3 = body_font.render("3:", True, WHITE)
    score_position4 = body_font.render("4:", True, WHITE)
    score_position5 = body_font.render("5:", True, WHITE)
    score_position6 = body_font.render("Can you beat your best score?", True, WHITE)

    drawPressKeyMsg()

    DISPLAYSURF.blit(score_position1, ((WINDOWWIDTH/2) -50, 100))
    DISPLAYSURF.blit(score_position2, ((WINDOWWIDTH/2) -50, 130))
    DISPLAYSURF.blit(score_position3, ((WINDOWWIDTH/2) -50, 160))
    DISPLAYSURF.blit(score_position4, ((WINDOWWIDTH/2) -50, 190))
    DISPLAYSURF.blit(score_position5, ((WINDOWWIDTH/2) -50, 220))
    DISPLAYSURF.blit(score_position6, ((WINDOWWIDTH/2) -150, 280))


    pygame.display.update()

    pygame.time.wait(500)
    drawPressKeyMsg()
    checkForKeyPress()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYUP:
                show_menu()
                return

def show_instructions():
    DISPLAYSURF.fill(VIOLET)

    title_font = pygame.font.SysFont("markerfelt", 40)
    body_font = pygame.font.SysFont("lucidagrande", 20)
    instruction_header = title_font.render("INSTRUCTIONS", True, WHITE)
    instructions1 = body_font.render("For easy and medium levels, use your up, down, left, and right ", True, WHITE)
    instructions2 = body_font.render("buttons or WASD controls to change the direction of the worm.", True, WHITE)
    instructions3 = body_font.render("Any red apples you eat will increase your score by 1 point,", True, WHITE)
    instructions4 = body_font.render("or by 3 points for green apples. Yellow apples give you a", True, WHITE)
    instructions5 = body_font.render("point and an extra life. If you hit yourself or the edge of the", True, WHITE)
    instructions6 = body_font.render("screen, you lose a life. The game ends when you run out of lives.", True, WHITE)
    instructions7 = body_font.render("In the hard level, a computer snake will move around the screen.", True, WHITE)
    instructions8 = body_font.render("Hitting it with your head takes away a life. The computer snake ", True, WHITE)
    instructions9 = body_font.render("can also eat any non-red apples if it gets there first. ", True, WHITE)
    instructions10 = body_font.render("Your best scores are stored on the high scores list!", True, WHITE)

    drawPressKeyMsg()

    DISPLAYSURF.blit(instruction_header, ((WINDOWWIDTH/2) -105, 40))
    DISPLAYSURF.blit(instructions1, ((WINDOWWIDTH/2) -300, 100))
    DISPLAYSURF.blit(instructions2, ((WINDOWWIDTH/2) -300, 130))
    DISPLAYSURF.blit(instructions3, ((WINDOWWIDTH/2) -300, 160))
    DISPLAYSURF.blit(instructions4, ((WINDOWWIDTH/2) -300, 190))
    DISPLAYSURF.blit(instructions5, ((WINDOWWIDTH/2) -300, 220))
    DISPLAYSURF.blit(instructions6, ((WINDOWWIDTH/2) -300, 250))
    DISPLAYSURF.blit(instructions7, ((WINDOWWIDTH/2) -300, 280))
    DISPLAYSURF.blit(instructions8, ((WINDOWWIDTH/2) -300, 310))
    DISPLAYSURF.blit(instructions9, ((WINDOWWIDTH/2) -300, 340))
    DISPLAYSURF.blit(instructions10, ((WINDOWWIDTH/2) -300, 370))
    pygame.display.update()

    # event processing loop
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
            elif event.type == KEYUP:
                show_menu()
                return

def runGame():
    global level, FPS, COMPUTERFPS, BGCOLOR, score, scores, scores_dict, computer_worm_coords


    if level == 1:
        FPS = 12
        BGCOLOR = DARKBLUE
    elif level == 2:
        FPS = 18
        BGCOLOR = BLACK
    elif level == 3:
        BGCOLOR = DARKRED
        FPS = 15

    # Set a random start point.
    startx = random.randint(5, CELLWIDTH - 6)
    starty = random.randint(5, CELLHEIGHT - 6)
    wormCoords = [{'x': startx,     'y': starty},
    {'x': startx - 1, 'y': starty},
    {'x': startx - 2, 'y': starty}]
    direction = RIGHT
    # Start the apple in a random place.
    apple = getRandomLocation()
    # start special apple off the screen
    special_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
    special_apple_shown = False
    yellow_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
    yellow_apple_shown = False
    lives = 3
    score = 0

    if level == 3:
        computer_startx = random.randint(5, CELLWIDTH - 6)
        computer_starty = random.randint(5, CELLHEIGHT - 6)
        computer_worm_coords = [{'x': computer_startx,     'y': computer_starty},
        {'x': computer_startx + 1, 'y': computer_starty},
        {'x': computer_startx + 2, 'y': computer_starty}]
        computer_direction = LEFT




    while True: # main game loop
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    direction = LEFT
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    direction = RIGHT
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    direction = UP
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    direction = DOWN
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the worm has hit the edge
        if wormCoords[HEAD]['x'] == -1 or wormCoords[HEAD]['x'] == CELLWIDTH or wormCoords[HEAD]['y'] == -1 or wormCoords[HEAD]['y'] == CELLHEIGHT:
            lives -= 1
            if lives > 0:
                # reset worm position
                wormCoords = [{'x': startx,     'y': starty},
                {'x': startx - 1, 'y': starty},
                {'x': startx - 2, 'y': starty}]
                direction = RIGHT
                apple = getRandomLocation()

            elif lives == 0:
                scores.append(score)
                scores.sort(reverse=True)
                for i in range(len(scores)):
                    scores_dict[str(i+1)] = scores[i]
                return # game over

        # check if the worm has hit itself
        for wormBody in wormCoords[1:]:
            if wormBody['x'] == wormCoords[HEAD]['x'] and wormBody['y'] == wormCoords[HEAD]['y']:
                return # game over

        # check if worm has hit th computer worm

        # check if worm has eaten an apple
        if wormCoords[HEAD]['x'] == apple['x'] and wormCoords[HEAD]['y'] == apple['y']:
            # don't remove worm's tail segment
            score +=1
            special_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
            special_apple_shown = False
            yellow_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
            yellow_apple_shown = False
            apple = getRandomLocation()
        else:
            del wormCoords[-1] # remove worm's tail segment

        if score % 5 == 0 and special_apple_shown == False:
            special_apple = getRandomLocation()
            special_apple_shown = True

        if wormCoords[HEAD]['x'] == special_apple['x'] and wormCoords[HEAD]['y'] == special_apple['y']:
            special_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
            special_apple_shown = False
            yellow_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
            yellow_apple_shown = False
            apple = getRandomLocation()
            score += 3

        if score % 7 == 0 and score != 0 and yellow_apple_shown == False:
            yellow_apple = getRandomLocation()
            yellow_apple_shown = True

        if wormCoords[HEAD]['x'] == yellow_apple['x'] and wormCoords[HEAD]['y'] == yellow_apple['y']:
            special_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
            special_apple_shown = False
            yellow_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
            yellow_apple_shown = False
            apple = getRandomLocation()
            worm_color[0] = random.randint(0,255)
            worm_color[1] = random.randint(0,255)
            worm_color[2] = random.randint(0,255)
            lives += 1
            score += 1

        if level == 3:
            # Checks if computer worm is on the screen and bring it back on
            if computer_worm_coords[HEAD]['x'] == -1 or computer_worm_coords[HEAD]['x'] == CELLWIDTH or computer_worm_coords[HEAD]['y'] == -1 or computer_worm_coords[HEAD]['y'] == CELLHEIGHT:
                computer_startx = random.randint(5, CELLWIDTH - 6)
                computer_starty = random.randint(5, CELLHEIGHT - 6)
                computer_worm_coords = [{'x': computer_startx,     'y': computer_starty},
                {'x': computer_startx + 1, 'y': computer_starty},
                {'x': computer_startx + 2, 'y': computer_starty}]
                computer_direction = LEFT
            # Makes it so the computer worm is always moving the opposite direction of the player
            if direction == RIGHT:
                computer_direction = DOWN
            if direction == LEFT:
                computer_direction = UP
            if direction == UP:
                computer_direction = LEFT
            if direction == DOWN:
                computer_direction = RIGHT

            #checks if the head of the player worm has hit any part of the computer worm
            for i in range(len(computer_worm_coords)):
                if wormCoords[HEAD]['x'] == computer_worm_coords[i]['x'] and wormCoords[HEAD]['y'] == computer_worm_coords[i]['y']:
                    lives -= 1
                    if lives > 0:
                        wormCoords = [{'x': startx,     'y': starty},
                        {'x': startx - 1, 'y': starty},
                        {'x': startx - 2, 'y': starty}]
                        direction = RIGHT

                    elif lives == 0:
                        scores.append(score)
                        scores.sort(reverse=True)
                        for i in range(len(scores)):
                            scores_dict[str(i+1)] = scores[i]
                        return # game over

            # allows the computer worm to "steal" the special apples only
            if computer_worm_coords[HEAD]['x'] == special_apple['y'] and computer_worm_coords[HEAD]['y'] == special_apple['y'] or computer_worm_coords[HEAD]['x'] == yellow_apple['y'] and computer_worm_coords[HEAD]['y'] == yellow_apple['y']:
                special_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
                special_apple_shown = False
                yellow_apple = {'x': WINDOWWIDTH+10, 'y': WINDOWHEIGHT+10}
                yellow_apple_shown = False

        # move the worm by adding a segment in the direction it is moving
        if direction == UP:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] - 1}
        elif direction == DOWN:
            newHead = {'x': wormCoords[HEAD]['x'], 'y': wormCoords[HEAD]['y'] + 1}
        elif direction == LEFT:
            newHead = {'x': wormCoords[HEAD]['x'] - 1, 'y': wormCoords[HEAD]['y']}
        elif direction == RIGHT:
            newHead = {'x': wormCoords[HEAD]['x'] + 1, 'y': wormCoords[HEAD]['y']}

        wormCoords.insert(0, newHead)

        # move the computer worm
        if level == 3:
            if computer_direction == UP:
                computer_new_head = {'x': computer_worm_coords[HEAD]['x'], 'y': computer_worm_coords[HEAD]['y'] - 1}
            elif computer_direction == DOWN:
                computer_new_head = {'x': computer_worm_coords[HEAD]['x'], 'y': computer_worm_coords[HEAD]['y'] + 1}
            elif computer_direction == LEFT:
                computer_new_head = {'x': computer_worm_coords[HEAD]['x'] - 1, 'y': computer_worm_coords[HEAD]['y']}
            elif computer_direction == RIGHT:
                computer_new_head = {'x': computer_worm_coords[HEAD]['x'] + 1, 'y': computer_worm_coords[HEAD]['y']}
            computer_worm_coords.insert(0, computer_new_head)
            del computer_worm_coords[-1]

        DISPLAYSURF.fill(BGCOLOR)
        drawGrid()
        drawWorm(wormCoords)
        if level == 3:
            draw_computer_worm(computer_worm_coords)
        drawApple(apple)
        draw_special_apple(special_apple)
        draw_yellow_apple(yellow_apple)
        drawScore(score)
        draw_lives(lives)
        pygame.display.update()
        FPSCLOCK.tick(FPS)

def drawPressKeyMsg():
    body_font = pygame.font.SysFont("lucidagrande", 20)
    return_to_menu = body_font.render("Press any key to go to the main menu.", True, WHITE)
    DISPLAYSURF.blit(return_to_menu, ((WINDOWWIDTH/2) -200, 420))

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def showStartScreen():
    title_font = pygame.font.SysFont("markerfelt", 100)
    titleSurf1 = title_font.render('Wormy!', True, WHITE, DARKBLUE)
    titleSurf2 = title_font.render('Wormy!', True, VIOLET)

    degrees1 = 0
    degrees2 = 0
    while True:
        DISPLAYSURF.fill(BLUE)
        rotatedSurf1 = pygame.transform.rotate(titleSurf1, degrees1)
        rotatedRect1 = rotatedSurf1.get_rect()
        rotatedRect1.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf1, rotatedRect1)

        rotatedSurf2 = pygame.transform.rotate(titleSurf2, degrees2)
        rotatedRect2 = rotatedSurf2.get_rect()
        rotatedRect2.center = (WINDOWWIDTH / 2, WINDOWHEIGHT / 2)
        DISPLAYSURF.blit(rotatedSurf2, rotatedRect2)

        drawPressKeyMsg()

        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        degrees1 += 3 # rotate by 3 degrees each frame
        degrees2 += 7 # rotate by 7 degrees each frame

def terminate():
    pygame.quit()
    sys.exit()

def getRandomLocation():
    return {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}

def showGameOverScreen():
    global score
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WINDOWWIDTH / 2, 10)
    overRect.midtop = (WINDOWWIDTH / 2, gameRect.height + 10 + 25)

    DISPLAYSURF.blit(gameSurf, gameRect)
    DISPLAYSURF.blit(overSurf, overRect)
    drawPressKeyMsg()
    pygame.display.update()
    pygame.time.wait(500)
    checkForKeyPress() # clear out any key presses in the event queue

    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WINDOWWIDTH - 120, 10)
    DISPLAYSURF.blit(scoreSurf, scoreRect)

def draw_lives(lives):
    lives_surf = BASICFONT.render('Lives: %s' % (lives), True, WHITE)
    lives_rect = lives_surf.get_rect()
    lives_rect.topleft = (WINDOWWIDTH - 120, 40)
    DISPLAYSURF.blit(lives_surf, lives_rect)

def drawWorm(wormCoords):
    for coord in wormCoords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAYSURF, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAYSURF, worm_color, wormInnerSegmentRect)

def draw_computer_worm(computer_worm_coords):
        for coord in computer_worm_coords:
            x = coord['x'] * CELLSIZE
            y = coord['y'] * CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
            pygame.draw.rect(DISPLAYSURF, PURPLE, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
            pygame.draw.rect(DISPLAYSURF, VIOLET, wormInnerSegmentRect)

def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)

def draw_special_apple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    special_apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, GREEN, special_apple_rect)

def draw_yellow_apple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    yellow_apple_rect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAYSURF, YELLOW, yellow_apple_rect)

def drawGrid():
    for x in range(0, WINDOWWIDTH, CELLSIZE): # draw vertical lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (x, 0), (x, WINDOWHEIGHT))
    for y in range(0, WINDOWHEIGHT, CELLSIZE): # draw horizontal lines
        pygame.draw.line(DISPLAYSURF, DARKGRAY, (0, y), (WINDOWWIDTH, y))

if __name__ == '__main__':
    main()
