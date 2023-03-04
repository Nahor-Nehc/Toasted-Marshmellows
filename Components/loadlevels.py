from pygame import event
#levels: a, b, c, d -> a = marshmellow type, b = delay before spawning (ms), c = row (0 to 4, 9 = random), d = repeats (default 1)

norm = lambda delay, row: {"type":"normal","delay": delay,"row": row}
normR = lambda delay: norm(delay, 9)

LEVELS = (
  [normR(1200), normR(2000), normR(1500)],
  [normR(3000), normR(500), normR(500), normR(500), normR(500)],
  [],
  
)

class Levels:
  def initialise(self):
    self.levels = tuple(LEVELS)
    self.current_level_int = 0
  def load_current(self, time: int):
    self.current_level_data = self.levels[self.current_level_int]
    self.level_start_time = time
    self.last_enemy_spawn_time = time
    self.current_enemy = 0
  def passed_level(self):
    self.current_level_int += 1
    if self.current_level_int >= len(self.levels):
      print("ran out of levels") # when all levels have been passed do something
      self.current_level_int = 0 # replays the last wav
    self.current_level_data = self.levels[self.current_level_int]
    self.current_enemy = 0
      
      
  def get_current_level_int(self):
    return self.current_level_int
  
  def process(self, time: int, spawn: event.Event):
    enemy = self.current_level_data[self.current_enemy]
    if self.last_enemy_spawn_time + enemy["delay"] <= time:
      print(self.current_enemy)
      event.post(event.Event(spawn))
      self.last_enemy_spawn_time = time
      self.current_enemy += 1
      if self.current_enemy >= len(self.current_level_data):
        self.passed_level()
        print("next level")
      