import pygame
from states.base_state import GameState

class PopupState(GameState):
    # This state is a reusable system popup.
    # It can show a short message with an OK button on top of the game world.
    # Use it for tutorial messages, system notifications, unlock notices, and similar dialogue.
    def __init__(self, game, title, message, image=None, button_text="OK", on_close=None):
        # Store the shared game reference so the popup can access the state stack
        # and return to the previous screen when it is dismissed.
        super().__init__(game)

        # Popup text content.
        self.title = title
        self.message = message

        # Optional image to show above the text.
        # This can be a loaded pygame Surface or None.
        self.image = image

        # Text shown on the confirm button.
        self.button_text = button_text

        # Optional callback to run after the popup closes.
        # This is useful if you want to chain logic after the player dismisses it.
        self.on_close = on_close

        # Button layout.
        self.button_rect = pygame.Rect(0, 0, 180, 54)

        # Fonts are created once when the state starts.
        self.title_font = None
        self.body_font = None
        self.button_font = None

    # This runs once when the popup becomes active.
    # It sets up fonts and centers the button.
    def enter(self):
        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.body_font = pygame.font.SysFont(None, 30)
            self.button_font = pygame.font.SysFont(None, 30)

    # This is the cleanup hook for consistency with the rest of the states.
    def exit(self):
        return super().exit()

    # This wraps text so long messages fit inside the popup box.
    def _wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = word if not current_line else current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    # This closes the popup and returns to the previous state.
    # If an on_close callback was provided, it runs after the popup closes.
    def _close(self):
        self.game.pop_state()

        if self.on_close is not None:
            self.on_close()

    # This handles input for the popup.
    # Clicking the button, pressing Space, Enter, or Escape all close it.
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self._close()
                return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN, pygame.K_ESCAPE):
                self._close()

    # The popup does not need time-based updates right now.
    def update(self, dt):
        return

    # This draws the popup.
    # It draws the state underneath first, then a dark overlay, then the popup box.
    def draw(self, screen):
        screen_w, screen_h = screen.get_size()

        # Draw the state underneath if there is one.
        # This makes the popup feel like an overlay instead of a full screen swap.
        if len(self.game.state_stack) >= 2:
            underlying_state = self.game.state_stack[-2]
            underlying_state.draw(screen)
        else:
            screen.fill((20, 20, 30))

        # Dark transparent overlay so the popup stands out.
        overlay = pygame.Surface((screen_w, screen_h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        # Main popup panel.
        box = pygame.Rect(120, 160, screen_w - 240, 400)
        pygame.draw.rect(screen, (18, 18, 24), box, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), box, width=2, border_radius=18)

        # Draw title.
        title_surf = self.title_font.render(self.title, True, (255, 255, 255))
        screen.blit(title_surf, (box.x + 24, box.y + 20))

        # Optional image at the top center.
        text_top = box.y + 80
        if self.image is not None:
            image_size = 120
            image_rect = pygame.Rect(
                box.centerx - image_size // 2,
                box.y + 60,
                image_size,
                image_size
            )
            scaled = pygame.transform.smoothscale(self.image, (image_size, image_size))
            pygame.draw.rect(screen, (245, 245, 245), image_rect, width=2, border_radius=10)
            screen.blit(scaled, image_rect.topleft)
            text_top = image_rect.bottom + 20

        # Wrap and draw message text.
        lines = self._wrap_text(self.message, self.body_font, box.width - 48)
        for i, line in enumerate(lines):
            line_surf = self.body_font.render(line, True, (230, 230, 230))
            screen.blit(line_surf, (box.x + 24, text_top + i * 32))

        # Center the button near the bottom of the popup.
        self.button_rect.centerx = box.centerx
        self.button_rect.bottom = box.bottom - 24

        pygame.draw.rect(screen, (40, 40, 60), self.button_rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), self.button_rect, width=2, border_radius=12)

        button_surf = self.button_font.render(self.button_text, True, (255, 255, 255))
        button_rect = button_surf.get_rect(center=self.button_rect.center)
        screen.blit(button_surf, button_rect)