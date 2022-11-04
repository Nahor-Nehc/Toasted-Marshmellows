import pygame

class attack(pygame.sprite.Sprite):
  def __init__(self, group, x, y, width, height):
    pygame.sprite.Sprite.__init__(self)
    
    #placeholder
    self.image = pygame.Surface([width, height])
    self.image.fill((0, 0, 0))
    
    self.rect = self.image.get_rect()
    self.rect.x = x
    self.rect.y = y
    
    self.add(group)

  def move(self, x_magnitude, y_magnitude):
    self.rect.x += x_magnitude
    self.rect.y += y_magnitude
    
class all_attacks(pygame.sprite.Group):
  def __init__(self):
    pygame.sprite.Group.__init__(self)
    pass