import numpy as np

fish = []
trash = []

class Catchable():
    def __init__(self, name, isFish: bool, fish_images, energy: list, mutation_score: list, isConsumable = True):
        self.name = name # Name of the fish caught

        self.isFish = isFish
        self.isTrash = not isFish
        if self.isTrash:
            trash.append(self)
        else:
            fish.append(self)
        self.consumable = isConsumable
        self.images = fish_images # List of the names of the fish assets for their base and mutated forms
        self.energy = energy # List of the amount of energy they give the player when eaten based on their mutation level
        self.mutation_score = mutation_score # List of how much each fish contributes to the player's mutation score based on their mutation level

    def image_for_mutation(self, mutation_level=0):
        # Returns the image path for the current mutation level
        if self.images is None:
            return None

        if isinstance(self.images, (list, tuple)):
            index = max(0, min(mutation_level, len(self.images) - 1))
            return self.images[index]

        return self.images


# Defining the different catchable items
minnow = Catchable(
    "Minnow", #name of the fish
    True, #is a fish
    [ #Images for different mutation levels
        "assets/minnow_0.png", 
        "assets/minnow_1.png", 
        "assets/minnow_2.png", 
        "assets/minnow_3.png", 
        "assets/minnow_4.png"
    ], 
    [1, 1.5, 2, 3, 5], #energy provided to player if eaten
    [0, 1, 2, 3, 4] #mutation level provided to player if eaten
 )

perch = Catchable(
    "Perch", 
    True, 
    [
        "assets/perch_0.png", 
        "assets/perch_1.png", 
        "assets/perch_2.png", 
        "assets/perch_3.png", 
        "assets/perch_4.png"
    ], 
    [3, 3.5, 5, 6, 8], 
    [0, 1, 3, 5, 8]
)

pike = Catchable(
    "Pike", 
    True, 
    [
        "assets/pike_0.png", 
        "assets/pike_1.png", 
        None, 
        None, 
        None
    ], 
    [3, 3.5, 5, 6, 8], 
    [0, 1, 3, 5, 8]
)

catfish = Catchable(
    "Catfish", 
    True, 
    [
        None, 
        None, 
        None, 
        None, 
        None
    ], 
    [7, 8, 10, 12, 15], 
    [0, 2, 6, 10, 15]
)

weeds = Catchable(
    "Lake Weed Cluster", 
    False, 
    "assets/Weed.png", 
    [0.5], 
    [0]
)

