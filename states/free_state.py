import pygame

from states.base_state import GameState
from states.dialogue_state import DialogueState
from states.fishing_state import FishingState


class FreeState(GameState):
    # This is the main exploration state.
    # It shows the current location, permanent world buttons, and any one-time
    # arrival conversation for that location.
    def __init__(self, game):
        # Store the shared game reference so this state can access save data,
        # the state stack, and helper methods like load_image().
        super().__init__(game)

        # These are filled in every time the state enters so the state always
        # reflects the player's current location.
        self.location = None
        self.background = None

        # This flag makes sure the arrival conversation only gets checked once
        # per time this state becomes active.
        self.arrival_checked = False

        # Button rectangles for the permanent actions in free mode.
        # Fishing stays available all the time.
        # Moving on only appears when the location's unlock flag is present.
        self.fishing_button_rect = pygame.Rect(40, 620, 220, 56)
        self.next_location_button_rect = pygame.Rect(1020, 620, 220, 56)

        # Fonts are created once and reused.
        self.title_font = None
        self.button_font = None
        self.small_font = None

    # This runs when FreeState becomes the active state.
    # It reloads the current location and background so the screen matches
    # whatever location the player is currently in.
    def enter(self):
        self.location = self.game.save_data.current_location
        self.background = self._load_background()

        self.arrival_checked = False

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.button_font = pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 24)

    # This is a cleanup hook.
    # FreeState does not need special cleanup right now, but the method stays
    # here so it fits the same state interface as the other states.
    def exit(self):
        return super().exit()

    # This helper loads the current location background safely.
    # If the location has no image, or the image fails to load, the state
    # can still draw by falling back to a plain background fill.
    def _load_background(self):
        if self.location is None or not self.location.image:
            return None

        try:
            return self.game.load_image(self.location.image)
        except Exception:
            return None

    # This helper decides whether the "move on" button should appear.
    # The button only shows when the location has a next location, and the
    # required unlock flag has already been added to save data.
    def can_move_on(self):
        if self.location is None:
            return False

        if self.location.next_location is None:
            return False

        if self.location.next_location_flag is None:
            return False

        return self.location.next_location_flag in self.game.save_data.flags

    # This helper starts the arrival conversation once per location entry.
    # It uses a flag so the same intro does not replay every time the player
    # returns to FreeState after a conversation ends.
    def _maybe_start_arrival_conversation(self):
        if self.location is None:
            return

        if self.location.arrival_conversation is None:
            return

        # If NPC conversations are disabled, skip the full arrival conversation.
        # This keeps the toggle you wanted meaningful for full cutscenes too.
        if not getattr(self.game, "npc_interactions_enabled", True):
            return

        arrival_flag = self.location.arrival_flag or f"visited_location_{self.location.id}"

        if arrival_flag in self.game.save_data.flags:
            return

        # Mark the conversation as seen before pushing the dialogue state.
        # That way it cannot accidentally trigger again when the player returns.
        self.game.save_data.flags.add(arrival_flag)

        # Push the arrival conversation on top of FreeState.
        # FreeState will stay underneath and continue once dialogue ends.
        self.game.push_state(
            DialogueState(
                self.game,
                conversation=self.location.arrival_conversation,
                start_node=self.location.arrival_start_node
            )
        )

    # This moves the player to the next location.
    # It updates the save data and then replaces the current FreeState so the
    # new location can load its own background and arrival logic.
    def _go_to_next_location(self):
        if not self.can_move_on():
            return

        self.game.save_data.current_location = self.location.next_location

        # Replace this FreeState with a fresh one so the new location gets loaded.
        self.game.change_state(FreeState(self.game))

    # This handles input while the player is in the free-roam world view.
    # It listens for the fishing button, the next-location button, and quitting.
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.fishing_button_rect.collidepoint(event.pos):
                # Fishing is a temporary overlay, so it gets pushed on top.
                self.game.push_state(FishingState(self.game))
                return

            if self.next_location_button_rect.collidepoint(event.pos):
                self._go_to_next_location()
                return

        # Any other input can be used later for player movement, NPC clicking,
        # or other free-state mechanics.
        return

    # This handles any time-based logic in the free state.
    # Right now the only automatic behavior is the one-time arrival conversation.
    def update(self, dt):
        if not self.arrival_checked:
            self.arrival_checked = True
            self._maybe_start_arrival_conversation()

    # This draws the location, then draws the permanent world buttons on top.
    # The upper-left corner is intentionally left open so an overlay button
    # can sit there later without colliding with these controls.
    def draw(self, screen):
        screen_w, screen_h = screen.get_size()

        # Draw the background first.
        if self.background is not None:
            bg = pygame.transform.smoothscale(self.background, (screen_w, screen_h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((30, 35, 45))

        # Draw a small title plate so the player knows where they are.
        title_box = pygame.Rect(20, 20, 320, 54)
        pygame.draw.rect(screen, (15, 15, 20), title_box, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), title_box, width=2, border_radius=12)

        title_text = self.location.name if self.location else "Unknown Location"
        title_surf = self.title_font.render(title_text, True, (255, 255, 255))
        screen.blit(title_surf, (title_box.x + 16, title_box.y + 10))

        # Draw the permanent fishing button.
        self._draw_button(
            screen,
            self.fishing_button_rect,
            "Fish"
        )

        # Draw the next-location button only when the unlock flag is present.
        if self.can_move_on():
            self._draw_button(
                screen,
                self.next_location_button_rect,
                "Move on"
            )

        # Helpful hint text at the bottom center.
        hint_text = self.small_font.render("Use the buttons to fish or continue.", True, (235, 235, 235))
        hint_rect = hint_text.get_rect(center=(screen_w // 2, screen_h - 24))
        screen.blit(hint_text, hint_rect)

    # This draws one of the rounded UI buttons used by FreeState.
    # Keeping it in a helper method avoids repeating the same draw code twice.
    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        label_surf = self.button_font.render(label, True, (255, 255, 255))
        label_rect = label_surf.get_rect(center=rect.center)
        screen.blit(label_surf, label_rect)