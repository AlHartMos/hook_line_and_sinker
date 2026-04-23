import pygame
from states.base_state import GameState
from states.valley_menu_state import ValleyMenuState


class ButtonOverlayState(GameState):
    # This state draws a UI button on top of whatever state is underneath it.
    # It is designed to behave like an overlay:
    # - It does NOT replace gameplay
    # - It only intercepts specific input (button clicks)
    # - Everything else continues as normal

    def __init__(self, game):
        super().__init__(game)

        # Button position and size
        self.button_rect = pygame.Rect(400, 20, 300, 60)

        # Font will be created once when the state starts
        self.font = None

        # Whether input should pass through to underlying states
        # (useful for letting FreeState still receive input)
        self.pass_through = True

    def enter(self):
        # Called once when the overlay is added to the stack
        if self.font is None:
            self.font = pygame.font.SysFont(None, 30)

    def exit(self):
        return super().exit()

    def handle_event(self, event):
        # Handle quit normally
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        # Handle button click
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                # Only active after valley unlock
                if "valley_paths_unlocked" in self.game.save_data.flags:
                    self.game.push_state(ValleyMenuState(self.game))
                return
        # If pass-through is enabled, forward the event to the state below
        if self.pass_through:
            self._forward_event(event)

    def _forward_event(self, event):
        # This sends the event to the next state down in the stack.
        # It allows FreeState to still receive input even though this overlay is on top.

        if len(self.game.state_stack) < 2:
            return

        underlying_state = self.game.state_stack[-2]
        underlying_state.handle_event(event)

    def update(self, dt):
        # Forward update so underlying gameplay continues running
        if self.pass_through and len(self.game.state_stack) >= 2:
            self.game.state_stack[-2].update(dt)

    def draw(self, screen):
        # First draw the underlying state
        if len(self.game.state_stack) >= 2:
            self.game.state_stack[-2].draw(screen)

        # Decide button text based on toggle state
        if self.game.npc_interactions_enabled:
            text = "NPC Conversations: On"
        else:
            text = "NPC Conversations: Off"

        # Draw button background
        pygame.draw.rect(screen, (35, 35, 50), self.button_rect, border_radius=10)

        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, width=2, border_radius=10)

        # Render text
        text_surf = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=self.button_rect.center)

        # Draw text
        screen.blit(text_surf, text_rect)