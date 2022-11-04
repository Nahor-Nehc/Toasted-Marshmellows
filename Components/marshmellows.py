import pygame
import os


class marshmellow(pygame.sprite.Sprite):
  def __init__(self, group, x, y, image):
    pygame.sprite.Sprite.__init__(self)
    
    #placeholder
    self.image = image
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.add(group)

  def move(self, x_magnitude, y_magnitude):
    self.rect.x += x_magnitude
    self.rect.y += y_magnitude
    
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
    pygame.sprite.Group.__init__(self)
    pass

  def move(self, x_magnitude, y_magnitude):
    for sprite in self:
      sprite.move(x_magnitude, y_magnitude)
      
  def create(self, x, y, type):
    width = self.types[type]["width"]
    height = self.types[type]["height"]
    self.add(marshmellow(self, x, y, pygame.transform.scale(self.types[type]["image"], (width, height))))