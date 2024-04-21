# # # # # # # # # # # # # # # #
#   author: sara john-chuan   #
#   title: ROBOCALYPSE        #
#   date: jan 8 2024          #
# # # # # # # # # # # # # # # #

# imports
import pygame, sys
from random import randint
from pygame import mixer
import math

# constants
WIDTH = 400
HEIGHT = 300
FPS = 12

hudsize = 10
objsize = 10

robowidth = 190
roboheight = 240

floor = 290

robotrect = pygame.Rect(WIDTH/4, HEIGHT/5, robowidth, roboheight)
trashboxrect = pygame.Rect(WIDTH / 2, floor - objsize*4, objsize*5, objsize*4)

# variables
gameloop = True
gamerun = False

background = 10
difficulty = [1, 2, 4, 2, 3, 5, 2, 5, 3, 6, 7, 2, 9, 5, 10]
upgrades = [1, 2, 4, 6, 8, 10]
upgradecheckboxlist = [0, 0, 0, 0, 0, 0]
diff = 0
mode = 10
win = 0
speed = 1
geargeneratetime = 60
lastupgrade = 0
zombgate = 0

# counts
alertcount = 0
gearcount = 0
baggearcount = 0
healthcount = 10

# player
playerx = 300
playery = 100
playermovement = 1

# zombies
zombies = []
zombcoords = []
zombrect = []
zombdraw = []

# bullets
bullets = []
bulletcoords = []
bulletrect = []
bulletdraw = []

# items
item = []
itemcoords = []
itemrect = []
itemdraw = []

# images
# backgrounds
bg1 = pygame.image.load("bg1.png")
bg1 = pygame.transform.scale(bg1, (WIDTH, HEIGHT))

bg2 = pygame.image.load("bg2.png")
bg2 = pygame.transform.scale(bg2, (WIDTH, HEIGHT))

# main hud
gearcounter = pygame.image.load("gearcount.png")
gearcounter = pygame.transform.scale(gearcounter, (hudsize*9, hudsize*4))

health = pygame.image.load("health.png")
health = pygame.transform.scale(health, (hudsize*1.5, hudsize))

alertOFF = pygame.image.load("alertOFF.png")
alertOFF = pygame.transform.scale(alertOFF, (hudsize*4, hudsize*4))

alertON = pygame.image.load("alertON.png")
alertON = pygame.transform.scale(alertON, (hudsize*4, hudsize*4))

# screen 1
robot = pygame.image.load("robo.png")
robot = pygame.transform.scale(robot, (robowidth, roboheight))

zombleft = pygame.image.load("zombleft.png")
zombleft = pygame.transform.scale(zombleft, (objsize*5, objsize*7))

zombright = pygame.image.load("zombleft.png")
zombright = pygame.transform.scale(zombright, (objsize*5, objsize*7))
zombright = pygame.transform.flip(zombright, True, False)

bulletleft = pygame.image.load("bullet.png")
bulletleft = pygame.transform.scale(bulletleft, (objsize*3, objsize*1))

bulletright = pygame.image.load("bullet.png")
bulletright = pygame.transform.scale(bulletright, (objsize*3, objsize*1))
# flip code from awesome cool abigail (formerly from mr rd)
bulletright = pygame.transform.flip(bulletright, True, False)

# player
player = pygame.image.load("player.png")
player = pygame.transform.scale(player, (objsize*3, objsize*5))

# screen 2
trashbox = pygame.image.load("trashbox.png")
trashbox = pygame.transform.scale(trashbox, (objsize*5, objsize*4))

gear = pygame.image.load("gear.png")
gear = pygame.transform.scale(gear, (objsize*3, objsize*3))

trash = pygame.image.load("trash.png")
trash = pygame.transform.scale(trash, (objsize*3, objsize*3))

# other hud
smallbag = pygame.image.load("bagsmall.png")
smallbag = pygame.transform.scale(smallbag, (hudsize*4, hudsize*5))

bigbag = pygame.image.load("bagbig.png")
bigbag = pygame.transform.scale(bigbag, (hudsize*10, hudsize*7))

upgradebox = pygame.image.load("upgradebox.png")
upgradebox = pygame.transform.scale(upgradebox, (hudsize*13, hudsize*8))

# background sound: credit to AZALI
mixer.init()
mixer.music.load("theme of a shop that sells things you dont want.mp3")
mixer.music.set_volume(1)
mixer.music.play(loops = -1)

# functions
# hud displays
def huddisplay(mode):
    # health bar
    pygame.draw.rect(screen, "black", (hudsize - 2, hudsize, hudsize*20, hudsize))
    for i in range(healthcount):
        screen.blit(health, (hudsize + hudsize*2*i, hudsize))
    # gear counter
    screen.blit(gearcounter, (hudsize, hudsize*3))
    font = pygame.font.Font("kongtext.ttf", (hudsize*2))
    graphics = font.render(str(gearcount), True, "black")
    screen.blit(graphics, (hudsize*6, hudsize*4))
    # enemy alert 
    screen.blit(alert, (hudsize*11, hudsize*3))

    # specialized hud displays for diff modes
    if mode == 0:
        screen.blit(smallbag, (WIDTH - hudsize*5, hudsize))
        graphics = font.render(str(baggearcount), True, "black")
        screen.blit(graphics, (WIDTH - hudsize*4, hudsize*3))

    elif mode == 1:
        screen.blit(bigbag, (hudsize, HEIGHT - hudsize*10))
        graphics = font.render(str(baggearcount), True, "black")
        screen.blit(graphics, (hudsize*3, HEIGHT - hudsize*6))

    else:
        # upgrade box display
        screen.blit(upgradebox, (WIDTH - hudsize*14, hudsize))
        x = 0
        for i in range(len(upgrades)):
            if i == 3:
                x = 1
            if upgradecheckboxlist[i] == 0:
                # non-bought upgrades are black
                graphics = font.render(str(upgrades[i]), True, "black")
                if x == 1:
                    i = i - 3
                screen.blit(graphics, (WIDTH - hudsize*13 + hudsize*4*i, hudsize*2 + x*hudsize*4))
            else:
                # bought upgrades are red
                graphics = font.render(str(upgrades[i]), True, "red")
                if x == 1:
                    i = i - 3
                screen.blit(graphics, (WIDTH - hudsize*13 + hudsize*4*i, hudsize*2 + x*hudsize*4))

def zombiechance(diff, numdiff):
    # generates zombies
    print("generating", diff[numdiff], "zombies")
    # if max difficulty, repeats last wave
    if numdiff >= 14:
        numdiff = 14
    for i in range(diff[numdiff]):
        if randint(1, 2) == 1:
            zombies.append(zombleft)
            zombcoords.append(WIDTH - objsize*5 + randint(1, 5))
            zombrect.append(pygame.Rect(WIDTH - objsize*5, floor - objsize*7, objsize*5, objsize*7))
            zombdraw.append(1)
        else:
            zombies.append(zombright)
            zombcoords.append(0 - randint(1, 5))
            zombrect.append(pygame.Rect(0, floor - objsize*7, objsize*5, objsize*7))
            zombdraw.append(1)
    numdiff = numdiff + 1
    return numdiff

def collisions(healthcount):
    dead = 0
    bulletused = 0
    for i in range(len(zombies)):
        # i think you told us colliderect but if not: https://www.pygame.org/docs/ref/rect.html#pygame.Rect.colliderect
        # collidelist: https://www.pygame.org/docs/ref/rect.html#pygame.Rect.collidelist
        if zombdraw[i] == 1:
            if zombrect[i].collidelist(bulletrect) != -1 and bulletdraw[zombrect[i].collidelist(bulletrect)] == 1:
                # bullet zombie collisions
                zombdraw[i] = 0
                bulletdraw[zombrect[i].collidelist(bulletrect)] = 0
                dead = dead + 1
                bulletused = bulletused + 1

            # zombie robot collisions
        elif robotrect.colliderect(zombrect[i]):
            healthcount = healthcount - 1
            zombdraw[i] = 0
            dead += 1

    # bullet wall collisions
    for y in range(len(bullets)):
        if bulletcoords[y] <= 0 or bulletcoords[y] + objsize*3 >= WIDTH and bulletdraw[y] == 1:
            bulletdraw[y] = 0
            bulletused += 1
    return dead, healthcount, bulletused, zombdraw, bulletdraw

def generategear():
    # draws trash / gears
    for i in range(len(item)):
            if itemdraw[i] == 1:
                screen.blit(item[i], itemcoords[i])
    if elapsed % geargeneratetime == 0:
        # generates new gears / trash
        for i in range(randint(2, 6)):
            if randint(0, 1) == 0:
                itemx, itemy = (randint(0, WIDTH - objsize*3)), (randint(0, HEIGHT - objsize*3))
                screen.blit(gear, (itemx, itemy))
                item.append(gear)
                itemcoords.append((itemx, itemy))
                itemrect.append(pygame.Rect(itemx, itemy, objsize*3, objsize*3))
                itemdraw.append(1)
            else:
                itemx, itemy = (randint(0, WIDTH - objsize*3)), (randint(0, HEIGHT - objsize*3))
                screen.blit(trash, (itemx, itemy))
                item.append(trash)
                itemcoords.append((itemx, itemy))
                itemrect.append(pygame.Rect(itemx, itemy, objsize*3, objsize*3))
                itemdraw.append(1)

def listshurtme(death, coords, thing, rect, draw):
    if draw.count(0) > 0:
        # delete items in lists
        for i in range(death):
            coords.pop(draw.index(0))
            thing.pop(draw.index(0))
            rect.pop(draw.index(0))
            draw.pop(draw.index(0))
    return coords, thing, rect, draw

def win(x):
    # displays win / lose screen
    if x == 1:
        screen.fill("honeydew")
        font = pygame.font.Font("kongtext.ttf", 15)
        graphics = font.render("you survived", True, "black")
        screen.blit(graphics, (30, HEIGHT / 4))
        graphics = font.render("the apocalypse!!", True, "black")
        screen.blit(graphics, (50, HEIGHT / 3))
        gamerun = False
    else:
        screen.fill("salmon")
        font = pygame.font.Font("kongtext.ttf", 15)
        graphics = font.render("oops... you got eaten", True, "black")
        screen.blit(graphics, (30, HEIGHT / 4))
        gamerun = False
    return gamerun

# setup
clock = pygame.time.Clock()
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('ROBOCALYPSE')

# game loop ////////////////////////////////////////////////////////////////////////
while gameloop == True:
    
    if mode == 10:
        # start screen
        screen.fill("white")
        # font: kongtext
        # importing fonts: https://stackoverflow.com/questions/38001898/what-fonts-can-i-use-with-pygame-font-font
        font = pygame.font.Font("kongtext.ttf", 15)
        graphics = font.render("welcome to ROBOCALYPSE!", True, "black")
        screen.blit(graphics, (30, HEIGHT / 4))
        font = pygame.font.Font("kongtext.ttf", 10)
        graphics = font.render("click to begin your (sad) life", True, "black")
        screen.blit(graphics, (20, HEIGHT / 2))
        graphics = font.render("as a not-zombie...", True, "black")
        screen.blit(graphics, (60, HEIGHT / 2 + 25))

        # click to begin
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mode = 0
                background = 1
                gamerun = True
                BEGIN = pygame.time.get_ticks()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    # real gameloop !
    if gamerun == True:
        
        elapsed = pygame.time.get_ticks() - BEGIN
        elapsed = elapsed / 100
        elapsed = math.floor(elapsed)
        
        # display background
        if background == 2:
            # display screen 2
            screen.blit(bg2, (0, 0))
            screen.blit(trashbox, (WIDTH / 2, floor - objsize*4))
        else:
            # display screen 1
            screen.blit(bg1, (0, 0))
            screen.blit(robot, (WIDTH/4, floor - roboheight))
            # draw bullets & zombies
            for i in range(len(bullets)):
                if bulletdraw[i] == 1:
                    screen.blit(bullets[i], (bulletcoords[i], floor - objsize*4))
            for i in range(len(zombies)):
                if zombdraw[i] == 1:
                    screen.blit(zombies[i], (zombcoords[i], (floor - objsize*7)))

        # zombies alert
        if len(zombies) == 0:
            alert = alertOFF
        else:
            alert = alertON
        
        # draw hud
        huddisplay(mode)

        # gear count affecting movement
        if baggearcount > 0:
            playermovement = speed - (baggearcount / 10)
        else:
            playermovement = speed

        # player collisions & display
        if mode != 2:
            screen.blit(player, (playerx, playery))
        playerrect = pygame.Rect(playerx, playery, objsize*3, objsize*5)

        # collision with walls & movement from one screen to the next
        if playerx + objsize*3 >= WIDTH:
            playerx = WIDTH - objsize*3
            if background == 1:
                background = 2
                playerx = objsize
        elif playerx <= 0:
            playerx = 0
            if background == 2:
                background = 1
                playerx = WIDTH - objsize*4
                
        if playery + objsize*5 >= HEIGHT:
            playery = HEIGHT - objsize*5
        elif playery <= 0:
            playery = 0

        # zombie generation & movement
        if diff >= 15:
            diff = 15
        if elapsed % 300 == 0 and zombgate == 0:
            zombgate = 1
            diff = zombiechance(difficulty, diff)
        elif elapsed % 300 != 0: 
            zombgate = 0

        # zombie & bullet movement
        if elapsed % 2 == 0:
            for i in range(0, len(zombies)):
                if zombies[i] == zombright:
                    zombcoords[i] = zombcoords[i] + 1
                    zombrect[i] = pygame.Rect(zombcoords[i], floor - objsize*7, objsize*5, objsize*7)
                else: 
                    zombcoords[i] = zombcoords[i] - 1
                    zombrect[i] = pygame.Rect(zombcoords[i], floor - objsize*7, objsize*5, objsize*7)

            for i in range(0, len(bullets)):
                if bullets[i] == bulletright:
                    bulletcoords[i] += 1
                    bulletrect[i] = pygame.Rect(bulletcoords[i], floor - objsize*4, objsize*3, objsize*1)
                else:
                    bulletcoords[i] -= 1
                    bulletrect[i] = pygame.Rect(bulletcoords[i], floor - objsize*4, objsize*3, objsize*1)

        # zombie & bullet collisions
        dead, healthcount, bulletused, zombdraw, bulletdraw = collisions(healthcount)

        # removing dead zombies / bullets
        zombcoords, zombies, zombrect, zombdraw = listshurtme(dead, zombcoords, zombies, zombrect, zombdraw)
        bulletcoords, bullets, bulletrect, bulletdraw = listshurtme(bulletused, bulletcoords, bullets, bulletrect, bulletdraw)

        # trash / gear minigame
        if mode == 1:
            generategear()
        else:
            item.clear()
            itemcoords.clear()
            itemrect.clear()
        
        # upgrade effects
        if lastupgrade > 0 and lastupgrade % 2 == 0:
            geargeneratetime = geargeneratetime - 5
            lastupgrade = 0
        elif lastupgrade > 0:
            speed = speed + 0.4
            lastupgrade = 0
        
        # loss condition
        if healthcount <= 0:
            gamerun = win(0)

        # events
        for event in pygame.event.get():
            # quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if mode == 0:
                    # player movement
                    if event.key == pygame.K_LEFT:
                        playerx = playerx - 10*playermovement
                    elif event.key == pygame.K_RIGHT:
                        playerx = playerx + 10*playermovement
                    elif event.key == pygame.K_UP:
                        playery = playery - 10*playermovement
                    elif event.key == pygame.K_DOWN:
                        playery = playery + 10*playermovement

                elif mode == 2:
                    # bullet generation
                    if gearcount > 0:
                        if event.key == pygame.K_LEFT:
                            bullets.append(bulletleft)
                            bulletcoords.append(WIDTH/4 - objsize*3)
                            bulletdraw.append(1)
                            bulletrect.append(pygame.Rect(WIDTH/4, floor - objsize*4, objsize*3, objsize*1))
                            gearcount -= 1

                        elif event.key == pygame.K_RIGHT:
                            bullets.append(bulletright)
                            bulletcoords.append(WIDTH/4 + robowidth)
                            bulletdraw.append(1)
                            bulletrect.append(pygame.Rect(WIDTH/4 + robowidth, floor - objsize*4, objsize*3, objsize*1))
                            gearcount -= 1

                if event.key == pygame.K_SPACE:
                    # interaction with certain objects / mode changes
                    if mode == 2 or mode == 1:
                        mode = 0
                    elif playerrect.colliderect(robotrect) and background == 1:
                        mode = 2
                        gearcount += baggearcount
                        baggearcount = 0
                    elif playerrect.colliderect(trashboxrect) and background == 2:
                        mode = 1

                elif event.key == pygame.K_z:
                    # healing 
                    if mode == 2:
                        if healthcount < 10 and gearcount > 1:
                            healthcount += 1
                            gearcount -= 2
                
                elif event.key == pygame.K_x:
                    # upgrades 
                    if mode == 2:
                        upgradefocus = upgradecheckboxlist.index(0)
                        if gearcount >= upgrades[upgradefocus]:
                            gearcount = gearcount - upgrades[upgradefocus]
                            upgradecheckboxlist[upgradefocus] = 1
                            lastupgrade = upgradefocus
                            if upgrades[upgradefocus] == 10:
                                gamerun = win(1)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # trash game (clicking gears / trash)
                mousecoords = pygame.mouse.get_pos()
                if mode == 1:
                    itemclicked = 0
                    for i in range(len(item)):
                        if itemrect[i].collidepoint(mousecoords):
                            itemclicked += 1
                            itemdraw[i] = 0
                            if item[i] == gear and baggearcount < 9:
                                baggearcount += 1
                            elif item[i] == trash and baggearcount > 0:
                                baggearcount -= 1
                    itemcoords, item, itemrect, itemdraw = listshurtme(itemclicked, itemcoords, item, itemrect, itemdraw)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # update screen
    pygame.display.update()
    clock.tick(FPS)

pygame.quit()