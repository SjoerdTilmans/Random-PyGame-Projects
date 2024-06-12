import pygame
import numpy as np
from random import randint
import random

class player():

  def __init__(self,scale,gameDisplay):
    self.scale = scale
  
    body = 'files/pictures/player/body_red.png'
    head = 'files/pictures/player/head.png'
    feet = 'files/pictures/player/feet.png'
    arm = 'files/pictures/player/arm.png'
    head_back = 'files/pictures/player/head_back.png'
    
    bodyIm = pygame.image.load(body).convert_alpha()
    self.w,self.h = bodyIm.get_size()
    self.bodyIm = pygame.transform.scale(bodyIm,(self.scale*self.w,self.scale*self.h))
    headIm = pygame.image.load(head).convert_alpha()
    self.headIm = pygame.transform.scale(headIm,(self.scale*self.w,self.scale*self.h))
    foot1Im = pygame.image.load(feet).convert_alpha()
    self.foot1Im = pygame.transform.scale(foot1Im,(self.scale*self.w/4,self.scale*self.h/4))
    foot2Im = pygame.image.load(feet).convert_alpha()
    self.foot2Im = pygame.transform.scale(foot2Im,(self.scale*self.w/4,self.scale*self.h/4))
    armIm = pygame.image.load(arm).convert_alpha()
    self.armIm = pygame.transform.scale(armIm,(self.scale*self.w/2,self.scale*self.h/2))
    self.headImFlip = pygame.transform.flip(self.headIm,True,False)
    headBackIm = pygame.image.load(head_back)
    self.headBackIm = pygame.transform.scale(headBackIm,(self.scale*self.w,self.scale*self.h))
    self.headBackImFlip = pygame.transform.flip(self.headBackIm,True,False)

    self.gameDisplay = gameDisplay

  def draw_player(self,x,y,sine,state):
    
    if state['down'] == True and state['right'] == True:
      self.gameDisplay.blit(self.armIm,(x+0.9*self.w*self.scale+0.25*self.w*np.sin(4*sine),y+0.15*self.h*self.scale))
      self.gameDisplay.blit(self.bodyIm,(x+0.1*self.w*self.scale*np.sin(4*sine),y))
      self.gameDisplay.blit(self.headIm,(x+0.5*self.w+0.1*self.w*np.sin(4*sine),y-1.75*self.h))
      self.gameDisplay.blit(self.foot1Im,(x+0.25*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine)))
      self.gameDisplay.blit(self.foot2Im,(x+0.65*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine+np.pi)))
      self.gameDisplay.blit(self.armIm,(x+0.25*self.w*np.sin(4*sine+np.pi),y+0.15*self.h*self.scale))
      
    if state['down'] == True and state['left'] == True:
      
      self.gameDisplay.blit(self.bodyIm,(x+0.1*self.w*self.scale*np.sin(4*sine),y))
      self.gameDisplay.blit(self.headImFlip,(x-0.5*self.w+0.1*self.w*np.sin(4*sine),y-1.75*self.h))
      self.gameDisplay.blit(self.foot1Im,(x+0.1*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine)))
      self.gameDisplay.blit(self.foot2Im,(x+0.5*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine+np.pi)))
      self.gameDisplay.blit(self.armIm,(x+0.5*self.w*self.scale+0.25*self.w*np.sin(4*sine+np.pi),y+0.15*self.h*self.scale))
      self.gameDisplay.blit(self.armIm,(x-0.4*self.w*self.scale+0.25*self.w*np.sin(4*sine),y+0.15*self.h*self.scale))
      
    if state['up'] == True and state['right'] == True:
      self.gameDisplay.blit(self.armIm,(x+0.9*self.w*self.scale+0.25*self.w*np.sin(4*sine),y+0.15*self.h*self.scale))
      self.gameDisplay.blit(self.headBackIm,(x+0.5*self.w+0.1*self.w*np.sin(4*sine),y-1.75*self.h))
      self.gameDisplay.blit(self.foot1Im,(x+0.25*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine)))
      self.gameDisplay.blit(self.foot2Im,(x+0.65*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine+np.pi)))
      self.gameDisplay.blit(self.armIm,(x+0.25*self.w*np.sin(4*sine+np.pi),y+0.15*self.h*self.scale))
      self.gameDisplay.blit(self.bodyIm,(x+0.1*self.w*self.scale*np.sin(4*sine),y))
      
    if state['up'] == True and state['left'] == True:
      
      self.gameDisplay.blit(self.headBackImFlip,(x-0.5*self.w+0.1*self.w*np.sin(4*sine),y-1.75*self.h))
      self.gameDisplay.blit(self.foot1Im,(x+0.1*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine)))
      self.gameDisplay.blit(self.foot2Im,(x+0.5*self.scale*self.w,y+0.85*self.scale*self.h+0.1*self.w*np.sin(4*sine+np.pi)))
      self.gameDisplay.blit(self.armIm,(x+0.5*self.w*self.scale+0.25*self.w*np.sin(4*sine+np.pi),y+0.15*self.h*self.scale))
      self.gameDisplay.blit(self.armIm,(x-0.4*self.w*self.scale+0.25*self.w*np.sin(4*sine),y+0.15*self.h*self.scale))
      self.gameDisplay.blit(self.bodyIm,(x+0.1*self.w*self.scale*np.sin(4*sine),y))
      
class tile():
  def __init__(self, x, y, mode,size):
    self.mode = mode
    self.mirX = randint(0,1)
    self.mirY = randint(0,1)
    self.x = x
    self.y = y
    self.drawn = False
    
  def draw(self,gameDisplay,x,y,size):
  
    square = 'files/pictures/objects/square.png'
    dirt = 'files/pictures/background/mud.png'
    gras = 'files/pictures/background/grass.png'
    dry = 'files/pictures/background/dry.png'
    
    if self.drawn == False:
      if self.mode == 1:
        Im = pygame.image.load(dirt).convert_alpha()
      elif self.mode == 2:
        Im = pygame.image.load(gras).convert_alpha()
      else:
        Im = pygame.image.load(dry).convert_alpha()
      if self.mirX == 1:
        Im = pygame.transform.flip(Im,True,False)
      if self.mirX == 1:
        Im = pygame.transform.flip(Im,False,True)
      
      self.Im = pygame.transform.scale(Im,(size,size))
      self.drawn = True
  
    gameDisplay.blit(self.Im,(x,y))
    
    
class grid():
  gridsize = 100
  chance = 0.35

  def __init__(self,scale,gameDisplay):
    self.gameDisplay = gameDisplay
    square = 'files/pictures/objects/square.png'
    dirt = 'files/pictures/background/mud.png'
    
    self.dimx = 400
    self.dimy = 400
    
    self.grid_list = {}
    
    for i in range(0,self.dimx):
      for j in range(0,self.dimy):
        if i == 0 and j == 0:
          mode = randint(0,2)
          
        elif j == 0:
          mode_last = self.grid_list[(i-1,j)].mode
          number = random.uniform(0,1.0)
          if number > 1.0 - self.chance:
            mode = randint(0,2)
          else:
            mode = mode_last
            
        elif i == 0:
          mode_last = self.grid_list[(i,j-1)].mode
          number = random.uniform(0.0,1.0)
          if number > 1.0 - self.chance:
            mode = randint(0,2)
          else:
            mode = mode_last
            
        else:
          tile1 = self.grid_list[(i-1,j)].mode
          tile2 = self.grid_list[(i,j-1)].mode
          tile3 = self.grid_list[(i-1,j-1)].mode
          number = random.uniform(0.0,1.0)
          if number > self.chance:
            mode = tile1
          elif number > 2*self.chance:
            mode = tile2
          elif number > 3*self.chance:
            mode = tile3
          else:
            mode = randint(0,2)
            
        self.grid_list[(i,j)] = tile(i*self.gridsize - self.gridsize*self.gridsize,j*self.gridsize-self.gridsize*self.gridsize, mode, self.gridsize)
    self.imin = 0
    self.imax = i
    self.jmin = 0
    self.jmax = j  
        
        
  def draw_grid(self,x,y):
    
    i, j = self.calcGrid(x,y)
    x,y = self.calcStart(x,y)
    x_start, y_start = x, y
    i_start, j_start = i,j
   
    while x < 1200:
      while y < 775:
        self.grid_list[(i,j)].draw(self.gameDisplay,x,y,self.gridsize)
        y = y + self.gridsize
        j += 1
      x = x + self.gridsize
      y = y_start
      j = j_start
      i += 1
    
  def calcGrid(self,x,y):
    
    xmin = -int(x/self.gridsize) + self.dimx/2
    ymin = -int(y/self.gridsize) + self.dimy/2
    return xmin, ymin
    
  def calcStart(self,x,y):
    
    return x%self.gridsize-self.gridsize,y%self.gridsize-self.gridsize
    
    
    
    
    
    
    
    
