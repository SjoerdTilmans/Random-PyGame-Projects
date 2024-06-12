import pygame
import myLib
import numpy as np
import time as T

pygame.init()

display_width = 1200
display_height = 675
scale = 3
FPS = 60

black = (0,0,0)
white = (255,255,255)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('My first game')
clock = pygame.time.Clock()

player = myLib.player(3,gameDisplay)
grid = myLib.grid(3,gameDisplay)

def part(x1,y1):
  gameDisplay.blit(tree1Im,(x1,y1))
  
x = 0.5*display_width
y = 0.5*display_height
x_grid = 0
y_grid = 0
v_glob = 10
x_change = 0
y_change = 0
sine = 0

crashed = False
moving = False

keys = {}
state = {}
state['right'] = True
state['down'] = True
state['left'] = False
state['up'] = False

time = pygame.time.get_ticks()

while not crashed:
  
  v = v_glob*FPS
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      crashed = True
    if event.type == pygame.KEYDOWN:
      if event.key == pygame.K_LEFT:
        x_change = -v/FPS
        moving = True
        keys['left'] = True
        state['left'] = True
        state['right'] = False
      elif event.key == pygame.K_RIGHT:
        state['right'] = True
        state['left'] = False
        x_change = v/FPS
        moving = True
        keys['right'] = True
      if event.key == pygame.K_UP:
        state['up'] = True
        state['down'] = False
        y_change = -v/FPS
        moving = True
        keys['up'] = True
      elif event.key == pygame.K_DOWN:
        state['down'] = True
        state['up'] = False
        y_change = v/FPS
        moving = True
        keys['down'] = True
        
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_DOWN:
        y_change = 0
        keys['down'] = False
      if event.key == pygame.K_UP:
        y_change = 0
        keys['up'] = False
      if event.key == pygame.K_LEFT:
        x_change = 0
        keys['left'] = False
      if event.key == pygame.K_RIGHT:
        x_change = 0
        keys['right'] = False
    
    if all( value == False for value in keys.values() ):
      moving = False
        
  if moving == False:
    sine = 0.0
  else:
    sine = sine + 2*np.pi/FPS
    
  if x < 0.25*display_width and keys['left'] == True or x > 0.75*display_width and keys['right'] == True:
    x_grid = x_grid - x_change
  else:
    x = x + x_change
    
  if y < 0.25*display_height and keys['up'] == True or y > 0.75*display_height and keys['down'] == True:
    y_grid = y_grid - y_change
  else:
    y = y + y_change
  
  grid.draw_grid(x_grid,y_grid)
  player.draw_player(x,y,sine,state)
  pygame.display.update()
  
  time_passed = (pygame.time.get_ticks() - time)
  if time_passed < 1000/FPS:
    T.sleep((1000.0/FPS - time_passed)/1000.0)
  time = pygame.time.get_ticks()
  
  print( 'FPS: ' + str(1.0 / (time_passed/1000.0) ) )
  
pygame.quit()
quit()
