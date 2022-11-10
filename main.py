import pygame
from Components.marshmellows import *
from Components.attacks import *
from Components.state import State
from Components.transition import alpha
import sys
import shelve

pygame.init()

WIDTH, HEIGHT = 990, 540

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

PADDING = WIDTH/(990/20)

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toasted Marshmellows")

FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)

STARTTRANSITION = pygame.USEREVENT + 1


def draw(state, marshmellows, fade, start):
  background = pygame.Surface([WIDTH, HEIGHT])
  background.fill((255, 255, 255))
  WIN.blit(background, (0, 0))
  
  if state.get_state() == "start":
    start.drawText(WIN)
  
  if state.get_state() == "game":
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
  
  start = alpha()
  start.text("Press ENTER to start", FONT(60), position=((WIDTH - text.get_width())/2, (HEIGHT - text.get_height()-PADDING)), change = 2, colour=BLACK, repeat=True)
  
  #load saves
  stored_data = shelve.open(os.path.join("Saves", "data"))
  try:
    _ = stored_data["do_tutorial"]
  except KeyError:
    stored_data["do_tutorial"] = "yes"
    levels_completed = stored_data["levels_completed"]
    burnt_marshmellows = stored_data["burnt_marshmellows"]
    skewered_marshmellows = stored_data["skewered_marshmellows"]
    
  stored_data.close()
  
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
        
        #save game with shelve
        stored_data["do_tutorial"] = "no"
        stored_data["levels_completed"] = levels_completed
        stored_data["burnt_marshmellows"] = burnt_marshmellows
        stored_data["skewered_marshmellows"] = skewered_marshmellows

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
          if event.key == pygame.K_RETURN:
            pygame.event.post(pygame.event.Event(STARTTRANSITION))
        
      elif event.type == STARTTRANSITION:
        #starts the transition
        fade.rect(BLACK, WIDTH, HEIGHT)
        fade.start = True
        
    if fade.start == True:
      if fade.fade == "out":
        if state.get_state() == "start":
          state.set_state("menu")

    marshmellows.move(-2, 0)
    
    draw(state, marshmellows, fade, start)

main()