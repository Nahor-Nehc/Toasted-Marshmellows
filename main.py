import pygame
import os
import sys
import time
import random

pygame.mixer.pre_init(44100, 16, 2, 4096)
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

# padding is relative to width
PADDING = WIDTH/(990/20)

# display window that is drawn to
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Toasted Marshmellows")

#import modules
from Components.marshmellows import all_marshmellows
from Components.state import State
from Components.transition import alpha
from Components.turret import Turret
from Components.loadlevels import Levels
from Components.projectiles import all_projectiles

# variable font sizing
FONT = lambda x: pygame.font.SysFont("consolas.ttf", x)

# user events
STARTTRANSITION = pygame.USEREVENT + 1
STARTLEVEL = pygame.USEREVENT + 2
USEREVENTS = [STARTTRANSITION, STARTLEVEL]

ROWHEIGHT = 75
#this variable holds the y co-ordinate of the top of the row
ROWS = [ROWHEIGHT*x+90 for x in range(1, 6)]

def draw(state, marshmellows: all_marshmellows, projectiles: all_projectiles, fade: alpha, start: alpha, turret: Turret):
  background = pygame.Surface([WIDTH, HEIGHT])
  background.fill((255, 255, 255))
  
  if state.get_state() == "start":
    # paints background white
    WIN.blit(background, (0, 0))
    
    # initiates introduction text
    start.drawText(WIN)
    
  elif state.get_state() == "menu":
    #paints background white
    WIN.blit(background, (0, 0))
  
  elif state.get_state() == "game":
    if state.get_substate() != "paused":
      WIN.blit(background, (0, 0))
    else:
      pass
      # when the game is paused, only refresh the menu screen so that background remains seen
    
    # draws the lines for the rows
    for x in range(0, 5):
      pygame.draw.line(WIN, BLACK, (0, ROWS[x]), (WIDTH, ROWS[x]), 2)
    
    # draws the turret
    turret.draw(WIN)
    
    # marshmellows.draw(WIN)
    marshmellows.animate(WIN)
    projectiles.animate(WIN)
    
  if fade.start == True:

    #draw the fade
    fade.drawRect(WIN)
    fade.drawText(WIN)

    #if the transition has ended ...
    if fade.end == True:

      #ends the transition
      fade.start = False
      
  # update screen at the end of the processing
  pygame.display.flip()

def update_game(marshmellows, projectiles):
  # remove unnecessary sprites
  marshmellows.delete_off_screen()
  projectiles.delete_off_screen(WIDTH)
  
  # move the rest of the sprites
  marshmellows.move()
  projectiles.move()
  
  # caluculate and process collisions
  collisions = marshmellows.calculate_projectile_collisions(projectiles)
  marshmellows.process_projectile_collisions(collisions)

def main():
  
  #initiates the clock
  clock = pygame.time.Clock()
  
  # initialise all the class objects
  state = State("start")
  turret = Turret(ROWS, ROWHEIGHT, WIDTH)
  marshmellows = all_marshmellows(ROWHEIGHT, ROWS, WIDTH)
  projectiles = all_projectiles(turret)
  levels = Levels()
  fade = alpha()
  start = alpha()
  
  # setting the fade texts
  # getting textf for the width
  textf = FONT(60).render("Loading...", 1, WHITE)
  fade.text("Loading...", FONT(60), position=((WIDTH - textf.get_width())/2, (HEIGHT - textf.get_height())/2), colour=WHITE)
  
  start.text("Press ENTER to start", FONT(60), position=((WIDTH - textf.get_width())/2, (HEIGHT - textf.get_height()-PADDING)), change = 2, colour=BLACK, repeat=True)
  
  import shelve
  #load saves
  stored_data = shelve.open(os.path.join("Saves", "data"))
  #stored_data.clear()
  try:
    _ = stored_data["do_tutorial"]
    levels_completed = stored_data["levels_completed"]
    toasted_marshmellows = stored_data["toasted_marshmellows"]
  except KeyError:
    stored_data["do_tutorial"] = "yes"
    levels_completed = 0
    toasted_marshmellows = 0
    
  stored_data.close()
  
  # remove unnecessary events from event list
  pygame.event.set_blocked(None)
  pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP])
  pygame.event.set_allowed(USEREVENTS)
  
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
        if state.get_state() == "game":############################ creation of marshmellows and projectiles are placeholders
          marshmellows.create(random.randrange(0, 5), "normal")
          projectiles.create("fireball")
      
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
        
      elif event.type == STARTLEVEL:
        levels.passed_level()
        levels.load_current(pygame.time.get_ticks())
        
    if fade.start == True:
      if fade.fade == "out":
        if state.get_state() == "start":
          state.set_state("game") ######### this should set it to menu state not game state
          time.sleep(0.25) # load stuff here
          levels.initialise()
          
    update_game(marshmellows, projectiles)
    #print(turret.current)
    
    draw(state, marshmellows, projectiles, fade, start, turret)

main()