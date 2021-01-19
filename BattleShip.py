# Abdul Rahman Jawad, Ahmed Rehman Chauhan, Saad Khan, Kh Asad, Rao Obaid

import pygame as py, random, time

red, green, blue, black, white = (255,0,0), (0,255,0), (0,191,255), (0,0,0),(255,255,255)
screen_x, screen_y = 725, 550
game_screen = py.display.set_mode((screen_x,screen_y))
aiboard, pboard = {}, {}
aishots, pshots, phits, aihits, pships, aiships = [], [], [], [], [], []

#   Information about BattleShip
def displayInfo():
    font = py.font.SysFont("monospace",20)
    game_screen.blit(font.render("BattleShip Game v1.0",1,black), (225,15))
    font = py.font.SysFont("monospace",15)
    game_screen.blit(font.render("You are playing against the computer. To win you need to destroy all ships.",1,black), (22,45))
    game_screen.blit(font.render("Hit is red, Miss is blue and Player ship is green.",1,black), (22,60))
    game_screen.blit(font.render("5 ships (size): Carrier 5, Battleship 4, Destroyer 3, Submarine 3, Boat 2",1,black), (22,75))
    game_screen.blit(font.render("Ship cannot be set diagonally and cannot overlap other ships.",1,black), (22,90))
    game_screen.blit(font.render("Player set their ships first. Then to start the game take the first shot.",1,black), (22,105))
    game_screen.blit(font.render("Computer Board",1,black), (30,200))
    game_screen.blit(font.render("Player Board",1,black), (390,200))

#   Creates and Display Boards 
def displayBoard():
    for i in range(1,11):
        for j in range(1,11):
            aiboard[chr(64 + i) + str(j)] = py.Rect(30 * i, 200 + 30 * j, 30, 30)
            py.draw.rect(game_screen, black, aiboard[chr(64 + i) + str(j)], 1)
            pboard[chr(64 + i) + str(j)] = py.Rect(360 + 30 * j, 200 + 30 * i, 30, 30)
            py.draw.rect(game_screen, black, pboard[chr(64 + i) + str(j)], 1)

#   Player Ship Placement on Player Board
def playerShip():
    for key in pboard.keys():
        if key not in pships:
            if len(pships) < 17 and pboard[key].collidepoint(event.pos):
                pships.append(key)
                
#   Player Shots on Computer Board
def playerShots():
    for key in aiboard.keys():
        if key not in pshots:
            if aiboard[key].collidepoint(event.pos):
                pshots.append(key)
                return True

#   AI Ships on Computer Board, HOWEVER NOT WORKING LIKE IT SHOULD
def computerShips():
    shipbox = random.choice(list(aiboard))
    while shipbox in aiships:
        shipbox = random.choice(list(aiboard))
    aiships.append(shipbox)

#   AI Shots on Player Board
def computerShots():
    key = random.choice(list(pboard))
    while key in aishots:
        key = random.choice(list(pboard))
    aishots.append(key)    

#   Check if anyone wins
def winner():
    font = py.font.SysFont("monospace",20)
    if set(aihits) == set(pships) and len(pships) == 17:
        game_screen.blit(font.render("Computer Wins! All Player Ships Destroyed",1,black), (1750,150))
        return 1
    elif set(phits) == set(aiships) and len(aiships) == 17:
        game_screen.blit(font.render("Player Wins!  All AI Ships Destroyed",1,black), (175,150))
        return 1
    else: return 0

#   Main Game
py.init()
py.display.set_caption("BattleShip")
py.mouse.set_visible(1)

running, turn = True, False
while running:
    pressed = py.mouse.get_pressed()
    py.key.set_repeat()
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False

    game_screen.fill(white)
    displayBoard()

    while len(aiships) < 17:
        computerShips()
    
    if event.type == py.MOUSEBUTTONDOWN:
        
        playerShip()

        if len(pships) >= 17:
            turn = playerShots()

    #   Player Ship Color
    for i in pships:
        py.draw.rect(game_screen, green,pboard[i] , 0)
                    
    #   Player Shots Color and Check Hit
    for shot in pshots:
        if shot in aiships:
            phits.append(shot)
            py.draw.rect(game_screen, red,aiboard[shot] , 0)
        else:
            py.draw.rect(game_screen, blue,aiboard[shot] , 0)

    if turn:
        computerShots()
        turn = False

    #   AI Shots Color and Check Hit
    for shot in aishots:
        if shot in pships:
            aihits.append(shot)
            py.draw.rect(game_screen, red,pboard[shot] , 0)
        else:
            py.draw.rect(game_screen, blue,pboard[shot] , 0)
    
    displayInfo()

    if winner():
        running = False
    
    py.display.update()

time.sleep(1)
py.quit()
