import pygame
import os
from Components.pygmtlsv4v2 import Animation


class projectile(pygame.sprite.Sprite):
  def __init__(self, group, x, y, image, animation):
    pygame.sprite.Sprite.__init__(self)
    
    #placeholder
    self.image = image
    self.animation = animation
    self.animation.start()
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.add(group)

  def move(self, x_magnitude, y_magnitude):
    self.rect.x += x_magnitude
    self.rect.y += y_magnitude
    
  def animate(self, window):
    self.animation.set_coords(self.rect.x, self.rect.y, self.rect.x, self.rect.y)
    self.animation.play(window, auto_increment_frame = True)
    print(self.animation)
    
class all_projectiles(pygame.sprite.Group):
  def __init__(self):
    print("initialising")
    short_range_movements = []
    
    self.types = {
      "normal": {
        "width": 100, #placeholder
        "height": 100,
        #"speed": 2,
        "images": [pygame.image.load(os.path.join("Assets", "placeholder.jpg"))],
        "movements": short_range_movements,
        "animation set frames": lambda anim: anim.set_frames(
          [pygame.transform.scale(
            self.types["normal"]["images"][x],
            (self.types["normal"]["width"], self.types["normal"]["height"])
            ) for x in range(len(self.types["normal"]["images"]))
          ]
        )
      }
    }
    
    pygame.sprite.Group.__init__(self)

  def move(self, x_magnitude, y_magnitude):
    for sprite in self:
      sprite.move(x_magnitude, y_magnitude)
      
  def create(self, x, y, type):
    animation = Animation(0, 0)
    self.types[type]["animation set frames"](animation)
    animation.set_offsets([[0, 0], [0, 0]])
    animation.duplicate_all_frames(20)
    
    width = self.types[type]["width"]
    height = self.types[type]["height"]
    
    self.add(projectile(self, x, y, pygame.transform.scale(self.types[type]["image"], (width, height)), animation))
    
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