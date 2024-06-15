import pygame
import time
import random
import os

pygame.init()

display_width = 800
display_height = 600

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Highway Havoc')
clock = pygame.time.Clock()

# Use relative paths to load images and fonts
current_path = os.path.dirname(__file__)  # Get the directory of the current script
assets_path = os.path.join(current_path, 'assets')  # Path to the assets directory

carImg = pygame.image.load(os.path.join(assets_path, 'racecar.png'))
carImg = pygame.transform.scale(carImg, (200, 200)) 
carImg = pygame.transform.rotate(carImg, 180)

car_width = carImg.get_width()
car_height = carImg.get_height()

backgroundImg = pygame.image.load(os.path.join(assets_path, 'background.png'))
backgroundImg = pygame.transform.scale(backgroundImg, (800, 600))

roadblockImg = pygame.image.load(os.path.join(assets_path, 'roadblock.png'))
roadblockImg = pygame.transform.scale(roadblockImg, (100, 100))

font_path = os.path.join(assets_path, 'AmericanCaptain-MdEY.otf')

def things_dodged(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Dodged: " + str(count), True, white)
    gameDisplay.blit(text, (0, 0))

def roadblock(thingx, thingy):
    gameDisplay.blit(roadblockImg, (thingx, thingy))

def car(x, y):
    gameDisplay.blit(carImg, (x, y))

def text_objects(text, font):
    textSurface = font.render(text, True, black)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font(font_path, 100)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = (display_width / 2, display_height / 2)
    gameDisplay.blit(backgroundImg, (0, 0))  # Blit the background
    gameDisplay.blit(TextSurf, TextRect)
    pygame.display.update()

def crash():
    message_display('You crashed')
    pygame.time.wait(2000)  # Wait for 2 seconds before restarting
    game_loop()

def game_loop():
    x = (display_width * 0.45)
    y = (display_height * 0.8 - carImg.get_height() / 2)
    x_change = 0

    thing_startx = random.randrange(0, display_width - 100)
    thing_starty = -600
    thing_speed = 4
    thing_width = 100
    thing_height = 100

    dodged = 0

    gameExit = False

    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = 5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change
        gameDisplay.blit(backgroundImg, (0, 0))

        roadblock(thing_startx, thing_starty)
        thing_starty += thing_speed
        car(x, y)
        things_dodged(dodged)
        
        if x > display_width - car_width or x < 0:
            crash()
        
        if thing_starty > display_height:
            thing_starty = 0 - thing_height
            thing_startx = random.randrange(0, display_width - 100)
            dodged += 1
            thing_speed += 1

        if y < thing_starty + thing_height and y + car_height > thing_starty:
            if (x > thing_startx and x < thing_startx + thing_width) or (x + car_width > thing_startx and x + car_width < thing_startx + thing_width):
                crash()

        pygame.display.update()
        clock.tick(60)

game_loop()
pygame.quit()
quit()
