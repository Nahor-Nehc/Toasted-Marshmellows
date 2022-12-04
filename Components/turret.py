import pygame
import os

class Turret:
  def __init__(self, rows : list, row_height, width):
    self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "placeholder.jpg")), (70, 70))
    self.rows = rows
    self.current = 0
    self.x = (width//9)*2
    self.y_offset = (row_height*4)//5
    
  def move_up(self):
    self.current -= 1
    if self.current < 0:
      self.current = len(self.rows) - 1
      
  def move_down(self):
    self.current += 1
    if self.current >= len(self.rows):
      self.current = 0
  
  def draw(self, window : pygame.surface.Surface):
    window.blit(self.image, (self.x, self.y_offset + self.rows[self.current] - self.image.get_height()))