import pygame
import os
from Components.pygmtlsv4v2 import Animation
from Components.turret import Turret

FIREBALL_IMAGES = [pygame.transform.scale(
    pygame.image.load(
      os.path.join(
        "Assets", "Animations", "projectiles", "fireball", f"{x}.png")), (60, 30)) for x in range(1, 6)]

class projectile(pygame.sprite.Sprite):
  def __init__(self):
    pygame.sprite.Sprite.__init__(self)

  def move_direct(self):
    self.rect.x += self.movements
    
  def animate(self, window: pygame.surface.Surface) -> None:
    self.animation.set_coords(self.rect.x, self.rect.y, self.rect.x, self.rect.y)
    self.animation.play(window, auto_increment_frame = True, auto_stop=self.auto_stop)
    
  def pierced(self):
    self.pierce -= 1
    if self.pierce <= 0:
      self.kill()
    

class fireball(projectile):
  def __init__(self, turret: Turret):
    pygame.sprite.Sprite.__init__(self)
    self.image = [*FIREBALL_IMAGES][0]
    self.images = [*FIREBALL_IMAGES]
    self.movements = 17
    self.damage = 1
    self.pierce = 1
    
    self.rect = self.image.get_rect()
    self.rect.x = turret.turret_mouth_x
    self.rect.y = turret.turret_mouth_y - self.rect.height//3
    
    self.row_bound = False
    self.row = turret.current
    
    self.animation = Animation(self.rect.x, self.rect.y)
    self.animation.set_frames(self.images)
    
    self.animation.set_offsets([[0, 0] for _ in range(len(self.images))])
    self.animation.duplicate_all_frames(3)
    
    self.animation.start()
    
    self.auto_stop = False
  
  def move(self):
    self.move_direct()

class all_projectiles(pygame.sprite.Group):
  def __init__(self, turret: Turret):
    self.types = {
      "fireball": fireball,
    }
    self.turret = turret
    pygame.sprite.Group.__init__(self)

  def move(self) -> None:
    for sprite in self:
      sprite.move()
      
  def create(self, proj_type) -> None:
    self.add(self.types[proj_type](self.turret))
    
  def animate(self, window) -> None:
    for sprite in self:
      sprite.animate(window)
      
  def delete_off_screen(self, width: int) -> None:
    for sprite in self:
      if sprite.rect.left > width:
        print("deleted")
        sprite.kill()
  
  def delete(self, sprite: pygame.sprite.Sprite) -> None:
    sprite.kill()