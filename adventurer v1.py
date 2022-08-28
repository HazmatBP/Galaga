#
# Adventurer Sprite animations
#
#  Create sprite animation based on key presses
#  Using sprites downloaded from https://rvros.itch.io/animated-pixel-hero
# 
# Key pressed       Images used
#   None                idle
#   Right arrow         run
#   Left arrow          run-left
#   Up arrow            crnr-climb
#   Down arrow          fall
#   Space bar           attack1
#
# Written by Mrs Stevenson
# Date: November 2019
#
# Version 1
#   Implemented idle, climb and run left only
#

import pygame
import random

# Defined actions
IDLE = 'idle'
RUN = 'run'
CLIMB = 'climb'
RUN_LEFT = 'run left'
FALL = 'fall'
SWING = 'swing'

def drawSprite(imageSprite, sprite, index, delay = 1):
    # Draw the next sprite in the animation sequence
    #
    # delay indicates the number of times the same sprite image
    # is displayed before going on to the next. Default value is 1.
    index = index + 1
    
    if index//delay >= len(imageSprite):
        index = 0
        
    gameDisplay.blit(imageSprite[index//delay], sprite)
    return index


pygame.init()

displayWidth = 1000
displayHeight = 500

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))

pygame.display.set_caption('Adventurer')

clock = pygame.time.Clock()


# Initial sprite data
spriteBase = 'Adventurer Sprites/adventurer-'

# Load idle images
idleSprite = []
for i in range(4):
    filename = spriteBase+"idle-2-0"+str(i)+"-1.3.png"
    idleSprite.append(pygame.image.load(filename))
                      
# Load run left images
runLeftSprite = []
for i in range(6):
    filename = spriteBase+"run-left-0"+str(i)+"-1.3.png"
    runLeftSprite.append(pygame.image.load(filename))

# Load climb images
climbSprite = []
for i in range(5):
    filename = spriteBase+"crnr-clmb-0"+str(i)+"-1.3.png"
    climbSprite.append(pygame.image.load(filename))
   
# Initial sprite image is idle, speed = 0
sprite = idleSprite[0].get_rect()
sprite.x = random.randint(int(displayWidth/3), int(2*displayWidth/3))
sprite.y = int(4*displayHeight/5)
spriteSpeedx = 0
spriteSpeedy = 0
action = IDLE
index = 0   # index of image currently displayed for given action

active = True
while active:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            index = -1
            if event.key == pygame.K_LEFT:
                action = RUN_LEFT
                spriteSpeedx = -5
            elif event.key == pygame.K_UP:
                action = CLIMB
                spriteSpeedy = -5
            
        if event.type == pygame.KEYUP:
            # Return to idle state
            spriteSpeedx = 0
            spriteSpeedy = 0
            action = IDLE

                          
    gameDisplay.fill(black)


    # Move sprite
    sprite.x += spriteSpeedx
    sprite.y += spriteSpeedy


    # Draw sprite based on current action    
    if action == IDLE:
        index = drawSprite(idleSprite, sprite, index, 6)
    elif action == RUN_LEFT:
        index = drawSprite(runLeftSprite, sprite, index, 2)
    elif action == CLIMB:
        index = drawSprite(climbSprite, sprite, index)
            
        
    pygame.display.update()
  

    clock.tick(30)

pygame.quit()
