from pygame import event
#levels: a, b, c, d -> a = marshmellow type, b = delay before spawning (ms), c = row (0 to 4, 9 = random), d = repeats (default 1)
LEVELS = (
  [{"type":"normal","delay":0,"row":0}],
  
  [("normal", 0, 4, 1)],
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
      pass # when all levels have been passed do something
  def get_current_level_int(self):
    return self.current_level_int
  
  def process(self, time: int, end_wave_event: event.Event):
    if self.last_enemy_spawn_time + self.current_level_data["delay"] <= time:
      event.post(end_wave_event)