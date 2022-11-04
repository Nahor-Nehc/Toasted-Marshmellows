import pygame
from Components.marshmellows import *
from Components.attacks import *
from Components.state import State
from Components.transition import alpha
import sys

pygame.init()

WIDTH, HEIGHT = 1980/2, 1080/2

FPS = 60

# general colours
BLACK =  (  0,   0,   0)
WHITE =  (255, 255, 255)
RED =    (211,   0,   0)
GREEN =  (  0, 150,   0)
DGREEN = (  0, 100,   0)
BLUE =   (  0,   0, 211)
LBLUE =  (137, 207, 240)
GREY =   (201, 201, 201)
LGREY =  (231, 231, 231)
DGREY =  ( 50,  50,  50)
LBROWN = (185, 122,  87)
DBROWN = (159, 100,  64)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toasted Marshmellows")

FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)

STARTTRANSITION = pygame.USEREVENT + 1


def draw(state, marshmellows, fade):
  background = pygame.Surface([WIDTH, HEIGHT])
  background.fill((255, 255, 255))
  WIN.blit(background, (0, 0))
  
  
  if state.get_state() == "menu":
    background.fill((255, 255, 255))
    WIN.blit(background, (0, 0))
    
    marshmellows.draw(WIN)
    
  if fade.start == True:

    #draw the fade
    fade.drawRect(WIN)
    
    fade.drawText(WIN)

    #if the transition has ended ...
    if fade.end == True:

      #ends the transition
      fade.start = False
      

  pygame.display.update()


def main():
  
  #initiates the clock
  clock = pygame.time.Clock()
  
  state = State("start")
  
  marshmellows = all_marshmellows()
  
  fade = alpha()
  text = "Loading..."
  text = FONT(60).render("Loading...", 1, WHITE)
  fade.text("Loading...", FONT(60), position=((WIDTH - text.get_width())/2, (HEIGHT - text.get_height())/2), colour=WHITE)
  
  #initiates game loop
  run = True
  while run:
    
    #ticks the clock
    clock.tick(FPS)

    #gets mouse position
    mouse = pygame.mouse.get_pos()
    
    #for everything that the user has inputted ...
    for event in pygame.event.get():

      #if the "x" button is pressed ...
      if event.type == pygame.QUIT:

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        sys.exit()
        
      elif event.type == pygame.MOUSEBUTTONDOWN:
        
        if state.get_state() == "game":
          marshmellows.create(WIDTH, 100, "normal")
      
      elif event.type == pygame.KEYDOWN:
        
        if state.get_state() == "start":
          pygame.event.post(pygame.event.Event(STARTTRANSITION))
          print("set")
        
      elif event.type == STARTTRANSITION:
        #starts the transition
        fade.rect(BLACK, WIDTH, HEIGHT)
        fade.start = True
        
    if fade.start == True:
      if fade.fade == "out":
        if state.get_state() == "start":
          state.set_state("menu")

    marshmellows.move(-2, 0)
    
    draw(state, marshmellows, fade)

main()