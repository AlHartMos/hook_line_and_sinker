import numpy as np
from fishes import fish

class Location:
    def __init__(
        self,
        id,
        name,
        trash_fish_ratio,
        mutation_rates,
        image_path,
        arrival_conversation=None,
        arrival_start_node="intro",
        arrival_flag=None,
        next_location=None,
        next_location_flag=None
    ):
        self.id = id # Location id (matches order that the player visits)
        self.name = name # Location name
        self.trash_fish_ratio = trash_fish_ratio # Ratio of trash to fish that can be caught (trash:fish)
        self.mutation_rates = mutation_rates # List of the mutation chance when the player catches a fish
        self.image = image_path # Path to the image that will serve as the background for this location

        # Short conversation that can play the first time the player arrives here.
        # This should usually be a conversation dictionary passed into DialogueState.
        self.arrival_conversation = arrival_conversation

        # Which node to begin at when the arrival conversation starts.
        self.arrival_start_node = arrival_start_node

        # Flag that marks the arrival conversation as already seen.
        # If this is None, FreeState can still auto-generate one from the location id.
        self.arrival_flag = arrival_flag

        # The next location object the player can move to from here.
        self.next_location = next_location

        # Flag that must exist before the "move on" button appears.
        self.next_location_flag = next_location_flag

    def mutation_level(self):
        # Returns the mutation level based on the current location
        return np.random.choice([0, 1, 2, 3, 4], p=self.mutation_rates)

    def trash_or_fish(self):
        # Returns one if Fish and zero if Trash
        return np.random.choice([0, 1], self.trash_fish_ratio)
    
# Defining the locations
cave = Location(
    5, 
    "Cave", 
    [0.0, 1.0], 
    [0.0, 0.05, 0.05, 0.1, 0.8], 
    None, 
    "dialogues/location_starters/cave_starter.py",
    )

lighthouse = Location(
    4, 
    "Lighthouse", 
    [0.01, 0.99], 
    [0.2, 0.2, 0.3, 0.3, 0.0], 
    None, 
    "dialogues/location_starters/lighthouse_starter.py",
    next_location=cave
    )

forest = Location(
    3, 
    "Forest", 
    [0.1, 0.9], 
    [0.4, 0.3, 0.2, 0.1, 0.0], 
    None, 
    "dialogues/location_starters/forest_starter.py",
    next_location=lighthouse
    )

valley = Location(
    2, 
    "Valley", 
    [0.1, 0.9], 
    [0.6, 0.3, 0.1, 0.0, 0.0], 
    None, 
    "dialogues/location_starters/valley_starter.py",
    next_location=forest
    )

lake = Location(
    1, 
    "Lake", 
    [0.3, 0.7], 
    [0.8, 0.2, 0.0, 0.0, 0.0], 
    None, 
    "dialogues/location_starters/lake_starter.py",
    next_location=valley,
    )

tutorial = Location(
    0, 
    "Tutorial", 
    [0.7, 0.3], 
    [1.0, 0.0, 0.0, 0.0, 0.0], 
    "assets/Tutorial_Area.png", 
    "dialogues/location_starters/tutorial_starter.py",
    next_location=lake,
    next_location_flag="tutorial_fish_caught"
    )
