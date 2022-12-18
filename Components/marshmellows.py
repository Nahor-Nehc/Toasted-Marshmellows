import pygame
import os
import time
from Components.pygmtlsv4v2 import Animation

images= {
    "normal" : pygame.transform.scale(pygame.image.load(os.path.join("Assets", "placeholder.jpg")),
      (100, 100)),
    }

class marshmellow(pygame.sprite.Sprite):
  def move(self, x_magnitude, y_magnitude):
    self.rect.x += x_magnitude
    self.rect.y += y_magnitude
    
  def animate(self, window):
    self.animation.set_coords(self.rect.x, self.rect.y, self.rect.x, self.rect.y)
    self.animation.play(window, auto_increment_frame = True)

class normal(marshmellow):
  def __init__(self, x, y, group):
    pygame.sprite.Sprite.__init__(self)
    self.image = images["normal"]
    
    self.images = [self.image, pygame.transform.rotate(self.image, 90)]
    
    self.rect = self.images[0].get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.images = [pygame.transform.scale(
            self.images[0],
            (self.rect.width, self.rect.height)
            ),
          pygame.transform.scale(
            self.images[1],
            (self.rect.width, self.rect.height)
            )]
    
    self.animation = Animation(x, y)
    self.animation.set_frames(self.images)
    self.animation.set_offsets([[0, 0], [0, 0]])
    self.animation.duplicate_all_frames(20)
    self.animation.start()
    
    self.auto_stop = False
    
    self.add(group)

class all_marshmellows(pygame.sprite.Group):
  def __init__(self):
    pygame.sprite.Group.__init__(self)
    
    self.types = {
      "normal": normal
    }

  def move(self, x_magnitude, y_magnitude):
    for sprite in self:
      sprite.move(x_magnitude, y_magnitude)
      
  def create(self, x, y, marsh_type, marshmellows):
    self.types[marsh_type](x, y, marshmellows)
    
  def animate(self, window):
    for sprite in self:
      sprite.animate(window)
      
  def delete_off_screen(self):
    for sprite in self:
      if sprite.rect.right < 0:
        print("deleted")
        sprite.kill()
        
  def get_projectile_collisions(self, projectiles):
    all_collisions = []
    for sprite in self:
      for proj in projectiles:
        if sprite.rect.colliderect(proj):
          all_collisions.append(sprite)
    return all_collisions
  
  def delete(self, sprite:pygame.sprite.Sprite):
    sprite.kill()