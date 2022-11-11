import pygame
import os
from Components.pygmtlsv4v2 import Animation


class marshmellow(pygame.sprite.Sprite):
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
    
class all_marshmellows(pygame.sprite.Group):
  def __init__(self):
    
    self.types = {
      "normal": {
        "width": 100, #placeholder
        "height": 100,
        "speed": 2,
        "image": pygame.image.load(os.path.join("Assets", "placeholder.jpg")),
      }
    }
    
    width = self.types["normal"]["width"]
    height = self.types["normal"]["height"]
    default_anim = Animation(0, 0)
    default_anim.set_frames([pygame.transform.scale(self.types["normal"]["image"], (width, height)), pygame.transform.rotate(pygame.transform.scale(self.types["normal"]["image"], (width, height)), 90)])
    default_anim.set_offsets([[0, 0], [0, 0]])
    default_anim.duplicate_all_frames(20)
    
    self.types.update({"animation" : default_anim})
    pygame.sprite.Group.__init__(self)

  def move(self, x_magnitude, y_magnitude):
    for sprite in self:
      sprite.move(x_magnitude, y_magnitude)
      
  def create(self, x, y, type):
    width = self.types[type]["width"]
    height = self.types[type]["height"]
    self.add(marshmellow(self, x, y, pygame.transform.scale(self.types[type]["image"], (width, height)), self.types[type]["animation"]))
    
  def animate(self, window):
    for sprite in self:
      sprite.animate(window)