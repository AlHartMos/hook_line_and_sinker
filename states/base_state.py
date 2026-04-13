# Basic template for all game states
    # Child classes will inherit these methods
    # This means we don't need to know the specific state to use any of these methods in the main loop
    # All methods pass since the basecase does not need them, the child classes will

class GameState:
    # Connect state to main Game object, so it can share methods and data
    def __init__(self, game):
        self.game = game

    def enter(self):
        # Called when the state first becomes active (used to trigger NPC interactions)
        pass

    def exit(self):
        # Called when the state is about to become inactive
        pass

    def handle_event(self, event):
        # Handles input events like key presses, mouse clicks, and quitting the game
        # Sets which inputs are allowed
        pass

    def update(self, dt):
        # Update state as time progresses
        # Sets how if/how time progresses in this state
        pass

    def draw(self, screen):
        # Draws the current state of the screen
        # Place backgrounds, NPC portraits, UI, dialogue...
        pass