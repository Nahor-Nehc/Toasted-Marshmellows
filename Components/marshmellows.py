import pygame
import os
import time
from Components.pygmtlsv4v2 import Animation
from Components.projectiles import all_projectiles

images= {
    "normal" : pygame.transform.scale(pygame.image.load(os.path.join("Assets", "placeholder.jpg")),
      (100, 100)),
    }

NORMAL_IMAGES = [pygame.transform.scale(
    pygame.image.load(
      os.path.join(
        "Assets", "Animations", "marshmellows", "normal", f"{x}.png")), (100, 100)) for x in range(1, 3)]

class marshmellow(pygame.sprite.Sprite):
  def move(self, x_magnitude, y_magnitude):
    self.rect.x += x_magnitude
    self.rect.y += y_magnitude
    
  def animate(self, window):
    self.animation.set_coords(self.rect.x, self.rect.y, self.rect.x, self.rect.y)
    self.animation.play(window, auto_increment_frame = True)
    
  def hurt(self, damage:int):
    self.health -= damage
    if self.health <= 0:
      self.kill()

class normal(marshmellow):
  def __init__(self, x, y, group):
    pygame.sprite.Sprite.__init__(self)
    self.image = [*NORMAL_IMAGES][0]
    self.images = [*NORMAL_IMAGES]
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.animation = Animation(self.rect.x, self.rect.y)
    self.animation.set_frames(self.images)
    self.animation.set_offsets([[0, 0] for _ in range(len(self.images))])
    self.animation.duplicate_all_frames(20)
    self.animation.start()
    
    self.auto_stop = False
    
    self.add(group)
    
    self.maxhealth = 2
    self.health = 2

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
        
  def calculate_projectile_collisions(self, projectiles:all_projectiles):
    all_collisions = []
    for sprite in self:
      for proj in projectiles:
        if sprite.rect.colliderect(proj.rect):
          all_collisions.append([sprite, proj])
    return all_collisions
  
  def process_projectile_collisions(self, collisions):
    used_projectiles = []
    for collision in collisions:
      if collision[1] not in used_projectiles:
        collision[0].hurt(collision[1].damage)
        collision[1].pierced()
        used_projectiles.append(collision[1])
      
  
  def delete(self, sprite:pygame.sprite.Sprite):
    sprite.kill()