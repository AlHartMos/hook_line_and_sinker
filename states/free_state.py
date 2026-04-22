# State in which the player can choose to fish, move to the next location, or eat

import pygame
from states.base_state import GameState

class FreeState(GameState):
    # Initialize state with data from the game
    def __init__(self, game):
        super().__init__(game)

    # Handling user inputs
    def handle_event(self, event):
        pass