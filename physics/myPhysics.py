import pygame
import numpy as np
from random import randint

class Player():
  
  jump_force = 0.1
  move_force = 0.001
  
  def __init__( self, r0, r, N, x, physics ):
    self.r0 = r0
    self.r = r
    self.N = N
    self.x = x
    self.physics = physics
    self.contact = False
    dtheta = 2*np.pi/N
    theta = 0.0
    
    for i in range(0,N):
      coord = x + np.array( [r0*np.cos(theta),r0*np.sin(theta)] )
      theta += dtheta
      physics.add_node( coord, r, Draw = True )
      
    for node in physics.nodes:
      if node < len(physics.nodes)-1:
        physics.add_elem( physics.nodes[node], physics.nodes[node+1] )
      else:
        physics.add_elem( physics.nodes[node], physics.nodes[0] )
    
    for node1 in physics.nodes:
      count = 0
      for node2 in physics.nodes:
        if node1 is not node2 and count == 0:
          physics.add_elem( physics.nodes[node1], physics.nodes[node2], Draw = False )
          count = 0
        else:
          count += 1
        
  def jump( self ):
    self.contact = self.physics.get_contact()
    
    if self.contact == True:
      direction = self.get_jump_direction()
      for node in self.physics.nodes:
        self.physics.nodes[node].F = self.physics.nodes[node].F + direction * self.jump_force
        
  def left( self ):
  
    F = self.move_force
    for node in self.physics.nodes:
      self.physics.nodes[node].F[0] = self.physics.nodes[node].F[0] - F
      
  def right( self ):
  
    F = self.move_force
    for node in self.physics.nodes:
      self.physics.nodes[node].F[0] = self.physics.nodes[node].F[0] + F

  def get_jump_direction( self ):
    
    midpoint = np.array([0.0,0.0])
    N = len( self.physics.nodes )
    for node in self.physics.nodes:
      midpoint = midpoint + self.physics.nodes[node].x / N
    
    direction = np.array([0.0,0.0])
    for node in self.physics.nodes:
      if self.physics.nodes[node].contact == True:
        direction = direction + midpoint - self.physics.nodes[node].x

    direction = (( direction ) / np.linalg.norm( direction ) + 2*np.array([0.0,-1.0]))/3
    
    return direction
    
class Physics():
  
  g = 0.001
  d = 50
  m = 1.0
  a = 0.8
  k_contact = 0.025
  v_max = 1.0
  d_contact = 0.1

  def __init__( self, dt, gameDisplay ):
    self.nodes = {}
    self.elems = {}
    self.objects = {}
    self.dt = dt
    self.gameDisplay = gameDisplay
    
  def add_node( self, x, r, Draw=True ):
    self.nodes[len(self.nodes)] = Node( x,r,Draw )
    
  def add_elem( self, node1, node2, Draw=True ):
    self.elems[len(self.elems)] = Element( node1, node2, Draw )
    
  def add_object( self ):
    r = randint(80,120)
    self.objects[len(self.objects)] = Object( np.array([randint(0,1200-2*r),-2*r]), r )
    
  def calc_forces( self ):
    for node in self.nodes:
      self.nodes[node].calc_force( )
      for obj in self.objects:
        self.calc_contact( self.nodes[node], self.objects[obj] )
      
    for elem in self.elems:
      self.elems[elem].calc_force( )
      
    for obj in self.objects:
      self.objects[obj].calc_force( )
      for obj2 in self.objects:
        if obj is not obj2:
          self.calc_contact( self.objects[obj], self.objects[obj2] )
  
  def calc_contact( self, obj1, obj2 ):
    dist_sq = (obj1.x[0] + obj1.r - obj2.x[0] - obj2.r) ** 2 + (obj1.x[1] + obj1.r - obj2.x[1] - obj2.r) ** 2
    if dist_sq < (obj1.r+obj2.r) ** 2:
      dist = - np.sqrt( dist_sq ) + obj1.r + obj2.r
      direction = obj1.x + np.array([obj1.r,obj1.r]) - obj2.x - np.array([obj2.r,obj2.r])
      direction = direction / np.linalg.norm( direction )
      obj1.F = dist * self.k_contact * direction
      obj2.F = - obj1.F
    
  def update_position( self ):
    for node in self.nodes:
      self.nodes[node].a = 1.0/self.m*self.nodes[node].F
      self.nodes[node].a = self.nodes[node].a + np.array([0.0,self.g])
      self.nodes[node].v = self.nodes[node].v + self.dt*self.nodes[node].a
      if np.sqrt( self.nodes[node].v[0]**2 + self.nodes[node].v[1]**2 ) > self.v_max:
        self.nodes[node].v = self.v_max * self.nodes[node].v / np.sqrt( self.nodes[node].v[0]**2 + self.nodes[node].v[1]**2 )
      self.nodes[node].x = self.nodes[node].x + self.dt*self.nodes[node].v
      
      if self.nodes[node].x[1] > 675 - 2*self.nodes[node].r:
        self.nodes[node].v[1] = - self.a * abs( self.nodes[node].v[1] )
        self.nodes[node].x[1] = 675 - 2*self.nodes[node].r
        self.nodes[node].contact = True
        self.nodes[node].N = np.array([0.0,1.0])
        
      if self.nodes[node].x[0] > 1200 - 2*self.nodes[node].r:
        self.nodes[node].v[0] = - self.a * abs( self.nodes[node].v[0] )
        self.nodes[node].x[0] = 1200 - 2*self.nodes[node].r
        self.nodes[node].contact = True
        self.nodes[node].N = np.array([-1.0,0.0])
        
      if self.nodes[node].x[0] < 0:
        self.nodes[node].v[0] = self.a * abs( self.nodes[node].v[0] )
        self.nodes[node].x[0] = 0
        self.nodes[node].contact = True
        self.nodes[node].N = np.array([-1.0,0.0])
      
      self.nodes[node].F = np.array( [0.0,0.0] )
      
    for obj in self.objects:
      self.objects[obj].a = 1.0/self.objects[obj].m*self.objects[obj].F
      self.objects[obj].a = self.objects[obj].a + np.array([0.0,self.g])
      self.objects[obj].v = self.objects[obj].v + self.dt*self.objects[obj].a
      if np.sqrt( self.objects[obj].v[0] ** 2 + self.objects[obj].v[1] ** 2 ) > self.v_max:
        self.objects[obj].v = self.v_max * self.objects[obj].v / np.sqrt( self.objects[obj].v[0] ** 2 + self.objects[obj].v[1] ** 2 )
      self.objects[obj].x = self.objects[obj].x + self.dt*self.objects[obj].v
      
      if self.objects[obj].x[1] > 675 - 2*self.objects[obj].r:
        self.objects[obj].v[1] = - self.a * abs( self.objects[obj].v[1] )
        self.objects[obj].x[1] = 675 - 2*self.objects[obj].r
        self.objects[obj].contact = True
        self.objects[obj].N = np.array([0.0,1.0])
        
      if self.objects[obj].x[0] > 1200 - 2*self.objects[obj].r:
        self.objects[obj].v[0] = - self.a * abs( self.objects[obj].v[0] )
        self.objects[obj].x[0] = 1200 - 2*self.objects[obj].r
        self.objects[obj].contact = True
        self.objects[obj].N = np.array([-1.0,0.0])
        
      if self.objects[obj].x[0] < 0:
        self.objects[obj].v[0] = self.a * abs( self.objects[obj].v[0] )
        self.objects[obj].x[0] = 0
        self.objects[obj].contact = True
        self.objects[obj].N = np.array([-1.0,0.0])
      
      self.objects[obj].F = np.array( [0.0,0.0] )
      
  def draw(self):
    for node in self.nodes:
      self.nodes[node].draw( self.gameDisplay )
      
    for elem in self.elems:
      self.elems[elem].draw( self.gameDisplay )
      
    for object in self.objects:
      self.objects[object].draw( self.gameDisplay )
      
  def get_contact(self):
    for node in self.nodes:
      if self.nodes[node].contact == True:
        return True
    
    return False
    
class Object():

  d = 0.005

  def __init__( self, x, r ):
    self.x = x
    self.v = np.array([0.0,0.0])
    self.a = np.array([0.0,0.0])
    self.F = np.array([0.0,0.0])
    self.r = r
    Im = pygame.image.load('files/obj.png').convert_alpha()
    self.Im = pygame.transform.scale(Im,(2*r,2*r))
    self.N = np.array([0.0,0.0])
    self.m = randint(20,40)
    
  def draw( self, gameDisplay ):
    gameDisplay.blit( self.Im,(self.x[0],self.x[1]) )
    
  def calc_force( self ):
    self.F = self.F - self.v * self.d
    
class Node():
  
  d = 0.0025
  fric = 0.1
  
  def __init__( self, x, r, Draw, fixed=False ):
    self.x = x
    self.v = np.array([0.0,0.0])
    self.a = np.array([0.0,0.0])
    self.F = np.array([0.0,0.0])
    self.Draw = Draw
    self.fixed = fixed
    self.r = r
    Im = pygame.image.load('files/node.png').convert_alpha()
    self.Im = pygame.transform.scale(Im,(2*r,2*r))
    self.contact = False
    self.N = np.array([0.0,0.0])
    
  def draw( self, gameDisplay ):
    if self.Draw == True:
      gameDisplay.blit( self.Im,(self.x[0],self.x[1]) )
    
  def calc_force( self ):
  
    self.F = self.F - self.v * self.d
    
    if self.contact == True:
      self.F = self.F - self.fric * self.v * np.array( [self.N[1],-self.N[0]] )

      self.contact = False
    
class Element():
 
  k = 0.0010
  d = 0.0009

  def __init__( self, node1, node2, Draw ):
    self.node1 = node1
    self.node2 = node2
    self.Draw = Draw
    self.l0 = np.sqrt( ( node1.x[0] - node2.x[0] )**2 + ( node1.x[1] - node2.x[1] )**2 )
    
  def calc_force( self ):
    direction = self.calc_direction()
    
    Fd = ( np.sqrt( ( self.node1.x[0] - self.node2.x[0] )**2 + ( self.node1.x[1] - self.node2.x[1] )**2 ) - self.l0 ) * self.d
    Fd = Fd * direction
    
    Fk = ( np.sqrt( ( self.node1.x[0] - self.node2.x[0] )**2 + ( self.node1.x[1] - self.node2.x[1] )**2 ) - self.l0 ) * self.k
    Fk = Fk * direction
    
    self.node1.F = self.node1.F - Fk + Fd
    self.node2.F = self.node2.F + Fk - Fd
    
  def calc_direction( self ):
    
    I = np.array( [ self.node1.x[0] - self.node2.x[0] , self.node1.x[1] - self.node2.x[1] ] )
    I = I / np.linalg.norm(I)
    return I
    
  def draw( self, gameDisplay ):
    if self.Draw == True:
      pygame.draw.line( gameDisplay, (0,0,0), (self.node1.x[0] + self.node1.r, self.node1.x[1] + self.node1.r), (self.node2.x[0] + self.node1.r, self.node2.x[1] + self.node1.r), 2 )
    
