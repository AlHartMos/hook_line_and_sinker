import pygame

# Game is the central controller for the whole game
    # Creates: window, clock
    # Keeps track of if the game is running
    # Storing states
    # Running the main loop
    # Switching between states
    # Storing data shared between states

from states.free_state import FreeState

class Game:
    # Initialize the game
    def __init__(self):
        self.screen = pygame.display.set_mode((1280, 720)) # Initalize screen
        pygame.display.set_caption("Hook, Line, and Sinker") # Sets title window

        self.clock = pygame.time.Clock() # Create clock to control frame rate/when things appear
        self.running = True # Ensures the game keeps running until it's stopped

        self.save_data = SaveData() # Get data for user

        self.state_stack = [] # Allows for different states to be used simultaneously (good for popups)
        # ********** TODO: Add introductory popup to FreeState **************
        self.push_state(FreeState(self)) # Starts the game in FreeState

    # Recieve top state to work with the current state easily
    @property
    def state(self):
        return self.state_stack[-1]

    # Add state to the top of the stack
    def push_state(self, state):
        self.state_stack.append(state)
        state.enter() # Run new state

    # Remove the top state from the stack
        # Ends game if no states remain in the stack
    def pop_state(self):
        if self.state_stack:
            self.state_stack[-1].exit()
            self.state_stack.pop()

        if not self.state_stack:
            self.running = False

    # Replace current state
    def change_state(self, state):
        if self.state_stack:
            self.state_stack[-1].exit()
            self.state_stack.pop()

        self.state_stack.append(state)
        state.enter()

    # Main loop that keeps the game going
    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0 # 60FPS (/1000 to get into seconds)

            for event in pygame.event.get(): # Get all input/window events
                if event.type == pygame.QUIT: # If the game is quit, stop the game
                    self.running = False # Turn off the game
                else:
                    self.state.handle_event(event) # Send input to the current event

            self.state.update(dt) # Update logic
            self.state.draw(self.screen) # Draw the current frame
            pygame.display.flip() # Show the frame onscreen

    # Load an image (takes path as argument)
    def load_image(self, path):
        return pygame.image.load(path).convert_alpha()

# Save data about the player as they progress through the game
class SaveData:
    def __init__(self):
        self.location = "tutorial" # Set current location
        self.flags = set() # list of things that have happened for story logic later on
        self.cooler = [] # List of fish in the cooler
        self.mutation_level = 0 # Mutation level of the players
        self.energy = 100 # Current energy level
