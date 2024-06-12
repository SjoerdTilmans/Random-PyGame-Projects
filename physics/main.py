import pygame
import myPhysics
import time
import numpy as np

def main(   display_width         = 1200         ,
            display_height        = 675          ,
            white                 = (255,255,255),
            FPS                   = 60          ,
            r                     = 5           ,
            r0                    = 60          ,
            N                     = 50          ,
            physics_updates_frame = 2           ,
            N_obj_per_s           = 0.5            ):

  pygame.init()
  clock = pygame.time.Clock()
  gameDisplay = pygame.display.set_mode((display_width,display_height))
  pygame.display.set_caption('Physics')
  dt = 1000.0/FPS/physics_updates_frame
  
  physics = myPhysics.Physics( dt, gameDisplay )
  player = myPhysics.Player( r0, r, N, np.array([display_width/2,display_height/2]), physics  )
  physics.add_object()
  physics.add_object()
  
  quit = False
  left = False
  right = False
  
  t = 0.0
  
  count = physics_updates_frame
  
  while not quit:
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
          player.jump()
        elif event.key == pygame.K_UP:
          player.jump()
        if event.key == pygame.K_LEFT:
          left = True
        if event.key == pygame.K_RIGHT:
          right = True
          
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT:
          left = False
        if event.key == pygame.K_RIGHT:
          right = False
          
      if event.type == pygame.QUIT:
        quit = True
        
    if left == True:
      player.left()
    if right == True:
      player.right()
    
    t += dt
    
    if t > 1000/N_obj_per_s:
      physics.add_object()
      t = 0.0
    
    physics.calc_forces()
    physics.update_position()
    
    if count == physics_updates_frame:
      gameDisplay.fill(white)
      physics.draw()
      pygame.display.update()
      count = 0
    else:
      count += 1
    
    clock.tick(FPS*physics_updates_frame)
        
  pygame.quit()

main()
