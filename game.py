import pygame
import random
import math
import time 
# By Harry McGrath, 2022 


# Defining Functions

def drawFighter(fighterAction, fighterIndex, delay = 6):
    
    if fighterIndex // delay >= len(fighterIdle):
        fighterIndex = 0
    if fighterAction == 'IDLE':
        gameRenderPlane.blit(fighterIdle[fighterIndex//delay],fighterRect)
    fighterIndex += 1

    return fighterIndex

    
    
# Pack Setup - Defines the amount of enemies in a pack, and the 4 different packs
packSize = 0
packNumber = 0
distanceBetweenEnemies = 4
startPoints =[(-16, 200), (240,  200)] # Defines a left and right off screen spawnpoint for the enemies


def enemyShoot():
    global enemiesOnScreen, enemyShotsOnScreen, active

    enemyShotSpeed = 0.05
    
    for i in enemiesOnScreen:
        # Checks if the enemy is far away enough horizontally to the fighter, if it is idling, and if there aren't too many projectiles on screen.
        # If so, it will only shoot based on a random chance, so 30 enemies don't shoot at once.
        if math.isclose(i["x"], fighterRect.x, abs_tol = 50) == False and i["state"] == "idle" and len(enemyShotsOnScreen) < 50 and random.randint(1,200) == 200:
            enemyShotsOnScreen.append(enemyShotDict.copy())
            enemyShotsOnScreen[-1]["shootStart"] = (i["x"], i["y"]) 
            enemyShotsOnScreen[-1]["shootGoal"] = (fighterRect.x, fighterRect.y)
            enemyShotsOnScreen[-1]["x"] = i["x"]
            enemyShotsOnScreen[-1]["y"] = i["y"]
            enemyShotsOnScreen[-1]["rect"].center = (i["x"] + 8, i["y"] + 8) # The +8 means the projectiles spawn in the center of the enemy instead of the top left

            

        for k in enemyShotsOnScreen:
            startX = k["shootStart"][0]
            startY = k["shootStart"][1]
            
            goalX = k["shootGoal"][0]
            goalY = k["shootGoal"][1]
            
            if goalX == startX:
                k["gradientBroken"] = True
            
            if k["gradientBroken"] == True:
                k["y"] += enemyShotSpeed
                
            else:
                if goalX > startX:
                    k["x"] += enemyShotSpeed
                    
                elif goalX < startX:
                    k["x"] -= enemyShotSpeed
                    
                k["y"] = (goalY) + (k["x"] - goalX) * ((goalY - startY) / (goalX - startX))
            
            
            # If shot is out of bounds, marks it for deletion
            if k["x"] > 224 or k["y"] > 288: 
                k["alive"] = False
                
            
            # applying x and y to rect
            k["rect"].center = (k["x"], k["y"])
            
            gameRenderPlane.blit(enemyShotSprite[0], k["rect"])
            
            
            # Checks if shot has hit enemy, if so, triggers game over   
            if k["rect"].colliderect(fighterRect):
                active = False
            
        # Deletes shots that were marked for deletion prior 
        for j in range(len(enemyShotsOnScreen)):
            if enemyShotsOnScreen[j - 1]["alive"] == False:
                enemyShotsOnScreen.pop(j - 1)
                







 
def fighterShoot():
    global shotCooldown1, shotCooldown2
    
    if shotCooldown1 < 60:
        # Creates a new fighter projectile
        fighterShotsOnScreen.append(fighterShotDict.copy())
        #Plays the appropriate sound effect.
        pygame.mixer.Sound.play(soundEffects[3])
        
        # Sets attributes of projectile
        fighterShotsOnScreen[-1]["x"] = fighterRect.centerx 
        fighterShotsOnScreen[-1]["y"] = fighterRect.centery - 70
        fighterShotsOnScreen[-1]["rect"].center = (fighterShotsOnScreen[-1]["x"], fighterShotsOnScreen[-1]["y"])


        # Checks if the fighter and enemies are near each other's x-position, and if so, decreases the enemies health by 1
        for i in enemiesOnScreen:
            if math.isclose(i["x"], fighterRect.x, abs_tol = 10):
                i["health"] -= 1
                
                
            if i["health"] == 2:
                i["sprite"] = greenScoutIdle[0]
                
            elif i["health"] == 1:
                i["sprite"] = greenScoutIdle[1]
            # Kills the enemy if its health is 0
            elif i["health"] == 0:
                i["alive"] = False

        shotCooldown1 += 25

        

    
def moveFighterShots():
    
    fighterShotSpeed = 20
    # Goes through all projectiles and moves them up the screen
    for i in fighterShotsOnScreen:
        i["y"] -= fighterShotSpeed
        i["rect"].center = (i["x"], i["y"])
        gameRenderPlane.blit(i["sprite"], i["rect"])
  
# Shifts enemies left and right
def shiftEnemies():
    global enemyXShift
    global enemyXShiftDir
    
    if enemyXShift >= 6:
        enemyXShiftDir = "left"
    elif enemyXShift <= -6:
        enemyXShiftDir = "right"

    if enemyXShiftDir == "left":
        enemyXShift -= 1
    else:
        enemyXShift += 1
    
    



# Defines the individual points that the enemies should end up in. 
# Consists of one big list, with 5 smaller lists, one for each pack. Each pack list has the coordinates for the enemy positions 
# Individual coordinates are listed top to bottom and left to right.
# The coordinate is not the centre of the enemy's position, rather the top left. I did this because there is no exact centre when the enemy is 16x16 pixels

packOneCoords = [(9, 21), (9, 41), (29, 41), (9, 61), (29, 61)]
packTwoCoords = [(54, 21), (54, 41), (74, 41), (94, 41)]
packThreeCoords = [(74, 21), (94, 21), (114, 21), (134, 21)]
packFourCoords = [(154, 21), (114, 41), (134, 41), (154, 41)]
packFiveCoords = [(200, 21), (180, 41), (200, 41), (180, 61), (200, 61)]

arrangeEndList = [packOneCoords, packTwoCoords, packThreeCoords, packFourCoords, packFiveCoords]

alivePacks = [False, False, False, False, False]




def moveArrangeEnemies(i):
    
    enemiesArrangeMoveSpeed = 2
    
    # Sets the end coordinates of the enemy based on its pack, and its position in the pack
    i["arrangeGoal"] = arrangeEndList[i["pack"] - 1][i["positionInPack"]] 
      
    # Redefining the goals and startpoints of the enemies to make the following equation(s) simpler and easier to understand  
    startX = i["arrangeStart"][0]
    startY = i["arrangeStart"][1]

    goalX = i["arrangeGoal"][0]
    goalY = i["arrangeGoal"][1]
    # Checks if the enemy is approxiamately at their goal position, if so, snaps them to that exact position
    if math.isclose(i["y"], i["arrangeGoal"][1], abs_tol = (enemiesArrangeMoveSpeed / 2)) == True:
        i["x"] = i["arrangeGoal"][0]
        i["y"] = i["arrangeGoal"][1]
        i["state"] = "idle"
        
        
    else:
        
        # If the goalX and StartX are the same, then the gradient calculation will divide by 0, and the program will crash. This stops that from happening. 
        if goalX == startX:
            i["gradientBroken"] = True
        else:
            i["arrangeGradient"] = (goalY - startY) / (goalX - startX) 
            i["gradientBroken"] = False        

        # Changes the movement speed of the enemies based on the gradient that they're following. 
        # abs() is used because arrangeGradient is negative for some reason. I could find out why, but if it works, it works. 

        if i["gradientBroken"] == False: 
            if startX < goalX: 
                i["x"] += abs(enemiesArrangeMoveSpeed / i["arrangeGradient"]) 
            elif startX > goalX:
                i["x"] -= abs(enemiesArrangeMoveSpeed / i["arrangeGradient"]) 
                
            i["y"] = (goalY) + (i["x"] - goalX) * ((goalY - startY) / (goalX - startX))

        else:
            i["y"] -= enemiesArrangeMoveSpeed




    
    
    
    
def spawnPack():
    global tick 
    global enemiesOnScreen
    global packNumber
    global alivePacks
    
    leftOrRight = random.randint(0,1) # Decides whether the Top Centre pack will spawn from the left or from the right

    packNumber = random.randint(1,5)

    
    if packNumber == 1 or packNumber == 5:
        packSize = 5
        
    else:
        packSize = 4
    

    for i in range(packSize):
        
        
              
        if packNumber == 1 and alivePacks[0] == False:
            enemiesOnScreen.append(greenScoutDict.copy())
            enemiesOnScreen[-1]["x"] = startPoints[0][0] 
            enemiesOnScreen[-1]["y"] = startPoints[0][1]  
            enemiesOnScreen[-1]["pack"] = 1
            if i > 0:
                enemiesOnScreen[-1]["x"] -= i * 5
            enemiesOnScreen[-1]["positionInPack"] = i             
            enemiesOnScreen[-1]["state"] = "intro"

            
            
        elif packNumber == 2 and alivePacks[1] == False:
            enemiesOnScreen.append(greenScoutDict.copy())
            enemiesOnScreen[-1]["x"] = startPoints[0][0]
            enemiesOnScreen[-1]["y"] = startPoints[0][1]  
            enemiesOnScreen[-1]["pack"] = 2
            if i > 0:
                enemiesOnScreen[-1]["x"] -= i * 8
            enemiesOnScreen[-1]["positionInPack"] = i             
            enemiesOnScreen[-1]["state"] = "intro"

            
            
        elif packNumber == 3 and alivePacks[2] == False:
            enemiesOnScreen.append(greenScoutDict.copy())
            
            if leftOrRight == 0:
                enemiesOnScreen[-1]["x"] = startPoints[0][0]
                enemiesOnScreen[-1]["y"] = startPoints[0][1]
                enemiesOnScreen[-1]["middlePackSide"] = "left"
                enemiesOnScreen[-1]["pack"] = 3
                enemiesOnScreen[-1]["x"] -= i * 10
                
            else:
                enemiesOnScreen[-1]["x"] = startPoints[1][0]
                enemiesOnScreen[-1]["y"] = startPoints[1][1]
                enemiesOnScreen[-1]["middlePackSide"] = "right"
                enemiesOnScreen[-1]["pack"] = 3      
                enemiesOnScreen[-1]["x"] += i * 10
                
            enemiesOnScreen[-1]["positionInPack"] = i             
            enemiesOnScreen[-1]["state"] = "intro"
 
            
                 
        elif packNumber == 4 and alivePacks[3] == False:
            enemiesOnScreen.append(greenScoutDict.copy())
            enemiesOnScreen[-1]["x"] = startPoints[1][0]
            enemiesOnScreen[-1]["y"] = startPoints[1][1]
            enemiesOnScreen[-1]["pack"] = 4 
            if i > 0:
                enemiesOnScreen[-1]["x"] += i * 8
            enemiesOnScreen[-1]["positionInPack"] = i             
            enemiesOnScreen[-1]["state"] = "intro"

            
            
        elif packNumber == 5 and alivePacks[4] == False:
            enemiesOnScreen.append(greenScoutDict.copy())
            enemiesOnScreen[-1]["x"] = startPoints[1][0]
            enemiesOnScreen[-1]["y"] = startPoints[1][1]  
            enemiesOnScreen[-1]["pack"] = 5
            if i > 0:
                enemiesOnScreen[-1]["x"] += i * 5   
            enemiesOnScreen[-1]["positionInPack"] = i             
            enemiesOnScreen[-1]["state"] = "intro"

                  
    

    alivePacks[packNumber - 1] = True
        


def moveIntroEnemies(i):

    enemiesIntroMoveSpeed = 1

    # The reason that Packs 1 and 5 don't have a +1 to their IntroMoveSpeed is because they move along a steeper line, so they automatically move faster than the other enemies.
    # It isn't really possible to get all the enemies moving in the intro at the same speed, because sub-pixel movements arent doable without moving every nth frame, which would look choppy.

    if i["y"] <= 88:
        i["state"] = "arrange"
        i["arrangeStart"] = (i["x"], 88)
    
    if i["state"] == "intro":
        
        if i["pack"] == 1:
            i["x"] += enemiesIntroMoveSpeed
            i["y"] = 59 + (i["x"] - 26) * ((59 - 200) / (26 - (-16)))
            
        elif i["pack"] == 2:
            i["x"] += enemiesIntroMoveSpeed * 2
            i["y"] = 39 + (i["x"] - 71) * ((39 - 200) / (71 - (-16)))
            
        elif i["pack"] == 3:
            if i["middlePackSide"] == "left":
                i["x"] += enemiesIntroMoveSpeed * 2
                i["y"] = 39 + (i["x"] - 111) * ((39 - 200) / (111 - (-16)))
            else:
                i["x"] -= enemiesIntroMoveSpeed * 2
                i["y"] = 39 + (i["x"] - 111) * ((39 - 200) / (111- (240)))
            
        elif i["pack"] == 4:
            i["x"] -= enemiesIntroMoveSpeed * 2 
            i["y"] = 39 + (i["x"] - 152) * ((39 - 200) / (152 - (240)))
            
        elif i["pack"] == 5:
            i["x"] -= enemiesIntroMoveSpeed 
            i["y"] = 59 + (i["x"] - 198) * ((59 - 200) / (198 - (240)))
            

    
            

  

def twinkleStars():
    global holdTwinkle, backgroundIndex, currentBackground
    if random.randint(0,twinkleRarity) == twinkleRarity and holdTwinkle == False: # Randomly decides when to "twinkle" a star, it will not initiate a twinkle if it is already holding one for multiple frames
        currentBackground = random.randint(1,18)
        holdTwinkle = True

    if holdTwinkle == True: 
        if backgroundIndex > twinkleHoldLength:
            currentBackground = 0
            backgroundIndex = 0
            holdTwinkle = False
        else:
            backgroundIndex += 1
    
    gameRenderPlane.blit(background[currentBackground], (0,0))
    

# Setup

pygame.init()

WIDTH = 224 
HEIGHT = 288  

gameRenderPlane = pygame.Surface((WIDTH, HEIGHT))
gameDisplay = pygame.display.set_mode((WIDTH * 3 , HEIGHT * 3))

# Defining Actions

IDLE = 'IDLE'
MOVE_LEFT = 'MOVE_DOWN'
MOVE_RIGHT = 'MOVE_RIGHT'

# Setting variables used to make the background randomly twinkle
background = []
currentBackground = 0
backgroundIndex = 0
holdTwinkle = False
twinkleRarity = 80
twinkleHoldLength = 10


# Load SFX
soundEffects = []
soundEffects.append(pygame.mixer.Sound('Sounds/EnemyDie.wav')) 
soundEffects.append(pygame.mixer.Sound('Sounds/EnemyShoot.wav'))
soundEffects.append(pygame.mixer.Sound('Sounds/ShipDie.wav'))
soundEffects.append(pygame.mixer.Sound('Sounds/Shoot.wav'))


# Importing Background Sprites
for imageNumber in range(19):
    background.append(pygame.image.load(f'Sprites\Background\Twinkle\Twinkle{imageNumber}.png').convert())

# Importing Game Over

gameOverScreen = []
gameOverScreen.append(pygame.image.load('Sprites\Background\GameOver.png'))

    
 
# Importing Fighter Idle Sprites
fighterIdle = []
fighterIndex = 0
fighterAction = IDLE
for imageNumber in range(2):
    fighterIdle.append(pygame.image.load(f'Sprites\Fighter\Idle\Idle{imageNumber}.png').convert_alpha())
    
# Importing Green Scout Idle Sprites
greenScoutIdle = []
greenScoutIndex = 0
greenScoutAction = IDLE
for imageNumber in range(2):
    greenScoutIdle.append(pygame.image.load(f'Sprites\Enemies\Scout\GreenScout\Idle\Idle{imageNumber}.png').convert_alpha())



greenScoutDict = {
     
    "sprite": greenScoutIdle[0], 
    "rect": greenScoutIdle[0].get_rect(), 
    "identifier": "greenScout",
    "x" : 0,
    "y" : 0,
    "pack" : 0,
    "tick" : 0,
    "middlePackSide" : "",
    "state" : "intro",
    "positionInPack" : 0,
    "arrangeGoal" : (0, 0),
    "arrangeStart" : (0, 0),
    "arrangeGradient" : 0,
    "gradientBroken" : True,
    "alive" : True,
    "health" : 2
    

}


enemiesOnScreen = []
screenDead = False

enemyXShift = 0
enemyXShiftDir = "right"
# Creates a rectangle that the fighter is drawn on top of
fighterRect = fighterIdle[0].get_rect()

    
# Importing Fighter Shot Sprite
fighterShotSprite = []
fighterShotSprite.append(pygame.image.load('Sprites\Projectiles\FighterShot.png').convert_alpha())

# Importing Enemy Shot Sprite
enemyShotSprite = []
enemyShotSprite.append(pygame.image.load('Sprites\Projectiles\EnemyShot.png').convert_alpha())

# Importing Fighter Die Sprite
fighterDieSprite = []
fighterDieSprite.append(pygame.image.load('Sprites\Fighter\FighterDie.png').convert_alpha())

fighterShotsOnScreen = []


fighterShotDict = {
    "x" : 0,
    "y" : 0, 
    "sprite" : fighterShotSprite[0],
    "rect" : fighterShotSprite[0].get_rect(),
    
}

# Enemy Setup
enemyShotsOnScreen = []

enemyShotDict = {
    "x" : 0,
    "y" : 0, 
    "sprite" : enemyShotSprite[0],
    "rect" : enemyShotSprite[0].get_rect(),
    "shootStart" : (0,0),
    "shootGoal" : (0,0),
    "gradientBroken" : False,
    "alive" : True
}

 
# Fighter Movement Setup
fighterSpeed = 2
leftPressed = 0
rightPressed = 0
fighterRect.topleft = (0, 241)
   
    
clock = pygame.time.Clock()

shotCooldown1 = 0
shotCooldown2 = 0
tick = 59
active = True
while active:
    
    screenDead = True
    
    # Ticks up once per loop
    tick +=1



    # Randomly twinkle stars in the background       
    twinkleStars() 
    
    for event in pygame.event.get():
        # Makes the quit button work correctly
        if event.type == pygame.QUIT:
            active = False
        
        # Read keypresses 
        if event.type == pygame.KEYDOWN:  
            if event.key == pygame.K_a:
                leftPressed = True
            if event.key == pygame.K_SPACE:
                fighterShoot()

            if event.key == pygame.K_d:
                rightPressed = True
                   
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                leftPressed = False
            if event.key == pygame.K_d:
                rightPressed = False
                
                



                 

            
        
    # Checks if the fighter is touching screen boundaries, and if it is trying to move out of bounds
    if fighterRect.right >= WIDTH: 
        rightPressed = False
    elif fighterRect.left <= 0:
        leftPressed = False
        
    # If the fighter is in bounds, move it left/right.
    if leftPressed and rightPressed:
        None
    elif leftPressed:
        fighterRect.x -= fighterSpeed
    elif rightPressed:
        fighterRect.x += fighterSpeed 
          
            
            

    
    # Sets 2 cooldowns, so the player can shoot twice in rapid succession 
    if shotCooldown1 > 0:
        shotCooldown1 -= 1
        
    if shotCooldown2 > 0:
        shotCooldown2 -= 1
    
    if fighterAction == IDLE:   
        fighterIndex = drawFighter(IDLE, fighterIndex)
    
    
    # Moves fighter shots along the screen vertically 
    moveFighterShots()
    
    if tick % 30 == 0 and screenDead: 
        spawnPack()
    
    if tick % 2 == 0:
        shiftEnemies()
    

    for i in enemiesOnScreen:
        if i["state"] == "intro":
            moveIntroEnemies(i) 
        elif i["state"] == "arrange":
            moveArrangeEnemies(i) 
            

        

        i["rect"].topleft = (i["x"] + enemyXShift , i["y"])           
        
        if i["alive"]:   
            gameRenderPlane.blit(i["sprite"], i["rect"])
        else:
            i["x"] = 500
            
        # Only sets screenDead to True if all enemies on screen are dead 
        if screenDead == True and i["alive"] == True:
            screenDead = False
            
    # Allows new packs to spawn once screenDead is True
    if screenDead == True:
        alivePacks = [False, False, False , False, False]
        
    # Causes enemies within a certain x-distance shoot at the fighter
    enemyShoot()  
    
    # draws the renderplane onto the screen, and upscales it 3x
           
    gameDisplay.blit(pygame.transform.scale(gameRenderPlane, gameDisplay.get_rect().size), (0,0))

    pygame.display.update()
    clock.tick(60)

# Game Over Process

# Draws fighter death sprite and plays death sound
pygame.mixer.Sound.play(soundEffects[2])

gameRenderPlane.blit(fighterDieSprite[0], fighterRect)
gameDisplay.blit(pygame.transform.scale(gameRenderPlane, gameDisplay.get_rect().size), (0,0))
pygame.display.update()
time.sleep(1)


# Draws Game Over Screen
gameRenderPlane.blit(gameOverScreen[0], (0, 0))
gameDisplay.blit(pygame.transform.scale(gameRenderPlane, gameDisplay.get_rect().size), (0,0))
pygame.display.update()
time.sleep(2)


pygame.quit()
