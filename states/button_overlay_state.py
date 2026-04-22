import pygame
from states.base_state import GameState


class ButtonOverlayState(GameState):
    # This state sits on top of another state (usually FreeState)
    # and draws a clickable button without stopping the underlying state.
    def __init__(self, game, underlying_state):
        # Store reference to the main game (from GameState)
        super().__init__(game)

        # This is the state underneath (e.g., FreeState).
        # We forward updates, drawing, and most input to it.
        self.underlying_state = underlying_state

        # Rectangle that defines the button's position and size on screen.
        self.button_rect = pygame.Rect(40, 40, 300, 60)

        # Font will be created once when the state starts.
        self.font = None

    def enter(self):
        # Called once when the state is pushed onto the stack.
        # We initialize the font here so it's not recreated every frame.
        if self.font is None:
            self.font = pygame.font.SysFont(None, 30)

    def handle_event(self, event):
        # This handles input events (mouse, keyboard, etc.)

        # Allow the window to close properly
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        # Handle mouse clicks
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # If the click is inside the button, toggle the setting
            if self.button_rect.collidepoint(event.pos):
                self.game.npc_interactions_enabled = not self.game.npc_interactions_enabled
            else:
                # If the click is NOT on the button,
                # pass the event to the underlying state so it still works normally
                self.underlying_state.handle_event(event)
        else:
            # For all other events (keyboard, movement, etc.),
            # forward them directly to the underlying state
            self.underlying_state.handle_event(event)

    def update(self, dt):
        # This updates the underlying state every frame.
        # This is what allows FreeState to keep running while the overlay exists.
        self.underlying_state.update(dt)

    def draw(self, screen):
        # First draw the underlying state (the game world, etc.)
        self.underlying_state.draw(screen)

        # Decide what text to show based on the toggle state
        if self.game.npc_interactions_enabled:
            text = "NPC Conversations: On"
        else:
            text = "NPC Conversations: Off"

        # Draw the button background
        pygame.draw.rect(screen, (35, 35, 50), self.button_rect, border_radius=10)

        # Draw the button border
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, width=2, border_radius=10)

        # Render the button text
        text_surf = self.font.render(text, True, (255, 255, 255))

        # Center the text inside the button
        text_rect = text_surf.get_rect(center=self.button_rect.center)

        # Draw the text onto the screen
        screen.blit(text_surf, text_rect)