import numpy as np
from fishes import fish

class Location ():

    def __init__(self, id, name, trash_fish_ratio, mutation_rates, image_path):
        self.id = id # Location id (matches order that the player visits)
        self.name = name # Location name
        self.trash_fish_ratio = trash_fish_ratio # Ratio of trash to fish that can be caught (trash:fish)
        self.mutation_rates = mutation_rates # List of the mutation chance when the player catches a fish
        self.image = image_path # Path to the image that will serve as the background for this location

    def mutation_level(self):
        # Returns the mutation level based on the current location
        return np.random.choice([0, 1, 2, 3, 4], p = self.mutation_rates)
    
    def trash_or_fish(self):
        # Returns zero if Fish and one if Trash
        return np.random.choice([0, 1], self.trash_fish_ratio)
    
# Defining the locations in a dictionary for easy access to data when designing the game
tutorial = Location(0, "Tutorial", [0.7, 0.3], [1.0, 0.0, 0.0, 0.0, 0.0], "assets/Tutorial_Area.png")
lake = Location(1, "Lake", [0.3, 0.7], [0.8, 0.2, 0.0, 0.0, 0.0], None)
valley = Location(2, "Valley", [0.1, 0.9], [0.6, 0.3, 0.1, 0.0, 0.0], None)
forest = Location(3, "Forest", [0.1, 0.9], [0.4, 0.3, 0.2, 0.1, 0.0], None)
lighthouse = Location(4, "Lighthouse", [0.01, 0.99], [0.2, 0.2, 0.3, 0.3, 0.0], None)
cave = Location(5, "Cave", [0.0, 1.0], [0.0, 0.05, 0.05, 0.1, 0.8], None)
