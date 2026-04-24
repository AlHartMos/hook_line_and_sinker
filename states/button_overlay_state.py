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
        from states.free_state import FreeState
        # --- ALWAYS draw FreeState if it exists ---
        base_drawn = False

        for state in self.game.state_stack:
            if isinstance(state, FreeState):
                state.draw(screen)
                base_drawn = True
                break

        # fallback if somehow FreeState isn't present
        if not base_drawn:
            screen.fill((20, 20, 30))

        # --- DRAW THE OVERLAY BUTTON ---
        pygame.draw.rect(screen, (40, 40, 60), self.button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, 2, border_radius=12)

        text = self.font.render("Explore", True, (255, 255, 255))
        screen.blit(text, text.get_rect(center=self.button_rect.center))