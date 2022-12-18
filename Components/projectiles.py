import pygame
import os
from Components.pygmtlsv4v2 import Animation
from Components.turret import Turret


class projectile(pygame.sprite.Sprite):
  def __init__(self, group, x: int, y: int, image: pygame.image, animation: Animation, auto_stop: bool = False):
    pygame.sprite.Sprite.__init__(self)
    
    #placeholder
    self.image = image
    self.animation = animation
    self.animation.start()
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.auto_stop = auto_stop
    
    self.add(group)

  def move(self, x_magnitude, y_magnitude):
    self.rect.x += x_magnitude
    self.rect.y += y_magnitude
    
  def animate(self, window: pygame.surface.Surface) -> None:
    self.animation.set_coords(self.rect.x, self.rect.y, self.rect.x, self.rect.y)
    self.animation.play(window, auto_increment_frame = True, auto_stop=self.auto_stop)

class fireball(projectile):
  def __init__(self, x, y):
    self.image = pygame.image.load(os.path.join("Assets", "placeholder.jpg"))
    self.images = []
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.animation = Animation(x, y)
    self.animation.set_frames(
      [pygame.transform.scale(
        x,
        (self.rect.width, self.rect.y)
        ) for x in range(len(self.images))
      ]
    )
    self.animation.set_offsets()
    self.animation.start()
    
    self.auto_stop = False

class all_projectiles(pygame.sprite.Group):
  def __init__(self, turret: Turret):
    print("initialising")
    
    self.types = {
      "fireball": fireball,
    }
    
    self.turret = turret
    
    pygame.sprite.Group.__init__(self)

  def move(self, x_magnitude, y_magnitude) -> None:
    for sprite in self:
      sprite.move(x_magnitude, y_magnitude)
      
  def create(self, proj_type) -> None:
    self.add(self.types[proj_type]())
    
  def animate(self, window) -> None:
    for sprite in self:
      sprite.animate(window)
      
  def delete_off_screen(self, width: int) -> None:
    for sprite in self:
      if sprite.rect.left > width:
        print("deleted")
        sprite.kill()
        
  def get_projectile_collisions(self, projectiles) -> list:
    all_collisions = []
    for sprite in self:
      for proj in projectiles:
        if sprite.rect.colliderect(proj):
          all_collisions.append(sprite)
    return all_collisions
  
  def delete(self, sprite: pygame.sprite.Sprite) -> None:
    sprite.kill()