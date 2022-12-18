import pygame
from Components.marshmellows import *
from Components.attacks import *
from Components.state import State
from Components.transition import alpha
from Components.turret import Turret
from Components.projectiles import projectile, all_projectiles
import sys
import shelve
import time

pygame.init()

WIDTH, HEIGHT = 990, 540

FPS = 30

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
ROWHEIGHT = 75

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toasted Marshmellows")

FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)

STARTTRANSITION = pygame.USEREVENT + 1


def draw(state, marshmellows: all_marshmellows, fade: alpha, start: alpha, turret: Turret):
  background = pygame.Surface([WIDTH, HEIGHT])
  background.fill((255, 255, 255))
  WIN.blit(background, (0, 0))
  
  if state.get_state() == "start":
    start.drawText(WIN)
    
  elif state.get_state() == "menu":
    pass
  
  elif state.get_state() == "game":
    background.fill((255, 255, 255))
    WIN.blit(background, (0, 0))
    
    for x in range(1, 6):
      pygame.draw.line(WIN, BLACK, (0, HEIGHT-ROWHEIGHT*x), (WIDTH, HEIGHT-ROWHEIGHT*x), 2)
    
    turret.draw(WIN)
    
    #marshmellows.draw(WIN)
    marshmellows.animate(WIN)
    
  if fade.start == True:

    #draw the fade
    fade.drawRect(WIN)
    fade.drawText(WIN)

    #if the transition has ended ...
    if fade.end == True:

      #ends the transition
      fade.start = False
      

  pygame.display.flip()

def main():
  
  #initiates the clock
  clock = pygame.time.Clock()
  
  state = State("start")
  
  marshmellows = all_marshmellows()
  
  turret = Turret([ROWHEIGHT*x+90 for x in range(1, 6)], ROWHEIGHT, WIDTH)
  
  fade = alpha()
  text = "Loading..."
  textf = FONT(60).render(text, 1, WHITE)
  fade.text(text, FONT(60), position=((WIDTH - textf.get_width())/2, (HEIGHT - textf.get_height())/2), colour=WHITE)
  
  start = alpha()
  start.text("Press ENTER to start", FONT(60), position=((WIDTH - textf.get_width())/2, (HEIGHT - textf.get_height()-PADDING)), change = 2, colour=BLACK, repeat=True)
  
  #load saves
  stored_data = shelve.open(os.path.join("Saves", "data"))
  stored_data.clear()
  try:
    _ = stored_data["do_tutorial"]
    levels_completed = stored_data["levels_completed"]
    toasted_marshmellows = stored_data["toasted_marshmellows"]
  except KeyError:
    stored_data["do_tutorial"] = "yes"
    levels_completed = 0
    toasted_marshmellows = 0
    
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
        stored_data = shelve.open(os.path.join("Saves", "data"))
        stored_data["do_tutorial"] = "no"
        stored_data["levels_completed"] = levels_completed
        stored_data["toasted_marshmellows"] = toasted_marshmellows
        stored_data.close()

        #ends game loop
        run = False

        #terminates pygame
        pygame.quit()

        #terminates system
        sys.exit()
        
      elif event.type == pygame.MOUSEBUTTONDOWN:
        
        if state.get_state() == "game":###################################
          marshmellows.create(100, 100, "normal", marshmellows)
      
      elif event.type == pygame.KEYDOWN:
        
        if state.get_state() == "start":
          if event.key == pygame.K_RETURN:
            pygame.event.post(pygame.event.Event(STARTTRANSITION))
        
        elif state.get_state() == "game":
          if event.key == pygame.K_UP:
            turret.move_up()
          elif event.key == pygame.K_DOWN:
            turret.move_down()
        
      elif event.type == STARTTRANSITION:
        #starts the transition
        fade.rect(BLACK, WIDTH, HEIGHT)
        fade.start = True
        
    if fade.start == True:
      if fade.fade == "out":
        if state.get_state() == "start":
          state.set_state("game") ###################################
          time.sleep(0.5)
          
    marshmellows.delete_off_screen()
    marshmellows.move(-2, 0)
    
    draw(state, marshmellows, fade, start, turret)

main()