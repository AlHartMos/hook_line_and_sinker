import numpy as np
from states.base_state import GameState
from game import Game, SaveData
from fishes import fish, trash

# State for when the player is currently fishing

class FishingState(GameState):
    
    def __init__(self, game):
        super().__init__(game)
        self.location = game.save_data.current_location

    def enter(self):
        # Defining the catch
        is_fish = self.location.trash_or_fish()
        if is_fish:
            self.catch = np.random.choice(fish)
        else:
            self.catch = np.random.choice(trash)
        
        return super().enter()
    
    def exit(self):
        return super().exit()
        