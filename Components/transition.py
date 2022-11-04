import pygame

class alpha:
  def __init__(self):
    self.start = False
    self.mid = False
    self.start = False

  def text(self, text, font, startalpha = 0, change = 4, colour = (0, 0, 0), repeat = True, position = (0, 0)):
    self.colour = colour
    self.textV = font.render(text, 1, self.colour)
    self.fade = "in"
    self.startalpha = startalpha
    self.alpha = startalpha
    self.change = change
    self.repeat = repeat
    self.cycles = 0
    self.position = position
    self.end = False

  def rect(self, colour, width, height, startalpha = 0, change = 4):
    self.colour = colour
    self.rectV = pygame.Surface((width, height))
    self.rectV.fill(colour)
    self.fade = "in"
    self.startalpha = startalpha
    self.alpha = startalpha
    self.change = change
    self.end = False

  def drawText(self, WIN):
    if self.repeat == True or self.cycles < 1:
      if self.fade == "in":
        self.alpha += self.change
        if self.alpha > 255:
          self.fade = "out"
          self.cycles += 0.5
      else:
        self.alpha -= self.change
        if self.alpha < 0:
          self.cycles += 0.5
          self.fade = "in"
      if self.cycles >= 1:
        self.end = True

      self.textV.set_alpha(self.alpha)
      WIN.blit(self.textV, self.position)

  def drawRect(self, WIN):
    if self.alpha > 255:
      self.fade = "out"
      self.mid = True
    elif self.alpha < 0:
      self.end = True
    if self.fade == "in":
      self.alpha += self.change
    else:
      self.alpha -= self.change
    self.rectV.set_alpha(self.alpha)
    WIN.blit(self.rectV, (0, 0))