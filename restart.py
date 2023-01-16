import shelve
import os

stored_data = shelve.open(os.path.join("Saves", "data"))
stored_data.clear()