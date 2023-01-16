import pygame
import os

class Turret:
  def __init__(self, rows : list, row_height, width, size = 70):
    self.image = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "images", "turret.png")), (size, size))
    self.rows = rows
    self.size = size
    self.current = 0
    self.x = (width//9)*2
    self.y_offset = (row_height//8)*7
    self.y = self.y_offset + self.rows[self.current] - self.image.get_height()
    self.turret_mouth_x = self.x + (self.size//5)*4
    self.turret_mouth_y = self.y + (size//5)*2

  def move_up(self):
    self.current -= 1
    if self.current < 0:
      self.current = len(self.rows) - 1
    self.y = self.y_offset + self.rows[self.current] - self.image.get_height()
    self.turret_mouth_y = self.y + (self.size//5)*2
    
  def move_down(self):
    self.current += 1
    if self.current >= len(self.rows):
      self.current = 0
    self.y = self.y_offset + self.rows[self.current] - self.image.get_height()
    self.turret_mouth_y = self.y + (self.size//5)*2
  
  def draw(self, window : pygame.surface.Surface):
    window.blit(self.image, (self.x, self.y))
