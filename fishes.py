import numpy as np

fish = []
trash = []

class Catch:

    def __init__(self, name, item_type, fish_images, energy, mutation_score):
        self.name = name # Name of the fish caught
        self.item_type = item_type
        self.images = fish_images # List of the names of the fish assets for their base and mutated forms
        self.energy = energy # List of the amount of energy they give the player when eaten based on their mutation level
        self.mutation_score = mutation_score # List of how much each fish contributes to the player's mutation score based on their mutation level
        if self.item_type == "trash":
            trash.append(self.name)
        elif self.item_type == "fish":
            fish.append(self.name)
    
    def eaten(self, level):
        # How much energy they give the player when eaten based on the level of mutation
        if level in range(len(self.energy)):
            return self.energy[level]
        else:
            raise ValueError("Mutation level too high")

    def mutate(self, level):
        # How mutation points to give the player based on the level of mutation
        if level in range(len(self.mutation_score)):
            return self.mutation_score[level]
        else:
            raise ValueError("Mutation level too high")

class Location ():

    def __init__(self, id, name, trash_fish_ratio, mutation_rates):
        self.id = id # Location id (matches order that the player visits)
        self.name = name # Location name
        self.trash_fish_ratio = trash_fish_ratio # Ratio of trash to fish that can be caught (trash:fish)
        self.mutation_rates = mutation_rates # List of the mutation chance when the player catches a fish

    def mutation_level(self):
        # Returns the mutation level based on the current location
        return np.random.choice(5, p = self.mutation_rates)


# Defining the locations in a dictionary for easy access to data when designing the game
locations = {
    0: Location(0, "Tutorial", [0.7, 0.3], [1.0, 0.0, 0.0, 0.0, 0.0]),
    1: Location(1, "Lake", [0.3, 0.7], [0.8, 0.2, 0.0, 0.0, 0.0]),
    2: Location(2, "Valley", [0.1, 0.9], [0.6, 0.3, 0.1, 0.0, 0.0]),
    3: Location(3, "Forest", [0.1, 0.9], [0.4, 0.3, 0.2, 0.1, 0.0]),
    4: Location(4, "Lighthouse", [0.01, 0.99], [0.2, 0.2, 0.3, 0.3, 0.0]),
    5: Location(5, "Cave", [0.0, 1.0], [0.0, 0.05, 0.05, 0.1, 0.8])
}
# Defining the different catchable items
minnow = Catch("Minnow", "fish", None, [1, 1.5, 2, 3, 5], [0, 1, 2, 3, 4])
perch = Catch("Perch", "fish", None, [3, 3.5, 5, 6, 8], [0, 1, 3, 5, 8])
pike = Catch("Pike", "fish", None, [3, 3.5, 5, 6, 8], [0, 1, 3, 5, 8])
catfish = Catch("Catfish", "fish", None, [7, 8, 10, 12, 15], [0, 2, 6, 10, 15])
weeds = Catch("Lake Weed Cluster", "trash", None, [0.5], [0])

