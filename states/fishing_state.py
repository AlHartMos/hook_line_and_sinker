import pygame
import numpy as np

from states.base_state import GameState
from fishes import fish, trash, minnow, perch, pike, catfish


class FishingState(GameState):
    # This state handles the full fishing interaction.
    # It temporarily replaces FreeState until the player finishes the fishing action.
    def __init__(self, game):
        super().__init__(game)

        self.location = None
        self.background = None

        self.catch = None
        self.catch_mutation = 0
        self.catch_image = None

        # Two-phase system:
        # "reveal" → short delay before result
        # "choice" → player decides what to do with catch
        self.phase = "reveal"
        self.phase_started_at = 0
        self.reveal_duration_ms = 5000

        self.title_font = None
        self.body_font = None
        self.button_font = None
        self.small_font = None

        self.release_button = pygame.Rect(340, 560, 180, 54)
        self.cooler_button = pygame.Rect(760, 560, 180, 54)

    def enter(self):
        # Called once when fishing starts
        self.location = self.game.save_data.current_location
        self.background = self._load_background()

        self.catch = self._roll_catch()
        self.catch_mutation = self._roll_mutation_if_needed()
        self.catch_image = self._load_catch_image()

        self._handle_progression_unlock()

        self.phase = "reveal"
        self.phase_started_at = pygame.time.get_ticks()

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 54)
            self.body_font = pygame.font.SysFont(None, 34)
            self.button_font = pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 24)

    def exit(self):
        return super().exit()

    # ---------- CORE LOGIC ----------

    def _roll_catch(self):
        # Decide whether player catches fish or trash
        result = self.location.trash_or_fish()

        if result == 1:
            # Trash
            return np.random.choice(trash)

        # Fish → use location-based pool
        pool = self._fish_pool_for_location()
        return np.random.choice(pool)

    def _fish_pool_for_location(self):
        # Defines which fish are available in each location

        if self.location.id == 0:      # Tutorial
            return [minnow]

        elif self.location.id == 1:    # Lake
            return [minnow, perch]

        elif self.location.id == 2:    # Valley
            return [minnow, perch, pike]

        elif self.location.id == 3:    # Forest
            return [minnow, perch, pike]

        elif self.location.id == 4:    # Lighthouse
            return [minnow, perch, pike, catfish]

        elif self.location.id == 5:    # Cave
            return [minnow, perch, pike, catfish]

        # Base case fallback
        return [minnow]

    def _roll_mutation_if_needed(self):
        # Only fish have mutation levels
        if not getattr(self.catch, "isFish", False):
            return 0
        return self.location.mutation_level()

    # ---------- IMAGE HANDLING ----------

    def _get_catch_image_path(self):
        if self.catch is None:
            return None

        if getattr(self.catch, "isFish", False):
            if hasattr(self.catch, "image_for_mutation"):
                return self.catch.image_for_mutation(self.catch_mutation)

            images = getattr(self.catch, "images", None)
            if isinstance(images, (list, tuple)) and images:
                index = max(0, min(self.catch_mutation, len(images) - 1))
                return images[index]

            return images

        return getattr(self.catch, "images", None)

    def _load_catch_image(self):
        path = self._get_catch_image_path()
        if not path:
            return None

        try:
            return self.game.load_image(path)
        except Exception:
            return None

    def _load_background(self):
        if not self.location or not self.location.image:
            return None

        try:
            return self.game.load_image(self.location.image)
        except Exception:
            return None

    # ---------- UPDATE ----------

    def update(self, dt):
        # After delay → move to choice phase
        if self.phase == "reveal":
            now = pygame.time.get_ticks()
            if now - self.phase_started_at >= self.reveal_duration_ms:
                self.phase = "choice"

    # ---------- INPUT ----------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        # Ignore input during reveal phase
        if self.phase != "choice":
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.release_button.collidepoint(event.pos):
                self.game.pop_state()

            elif self.cooler_button.collidepoint(event.pos):
                self.game.save_data.cooler.append({
                    "catchable": self.catch,
                    "mutation": self.catch_mutation
                })
                self.game.pop_state()

    # ---------- DRAW ----------

    def draw(self, screen):
        self._draw_background(screen)

        if self.phase == "reveal":
            self._draw_message_box(
                screen,
                "You cast your line...",
                image=None
            )
        else:
            self._draw_message_box(
                screen,
                f"You caught a {self.catch.name}.",
                image=self.catch_image
            )

            self._draw_button(screen, self.release_button, "Release")
            self._draw_button(screen, self.cooler_button, "Add to cooler")

    def _draw_background(self, screen):
        w, h = screen.get_size()

        if self.background:
            bg = pygame.transform.smoothscale(self.background, (w, h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((25, 35, 50))

    def _draw_message_box(self, screen, title, body, image=None):
        box = pygame.Rect(120, 420, 1040, 230)

        pygame.draw.rect(screen, (20, 20, 20), box, border_radius=16)
        pygame.draw.rect(screen, (240, 240, 240), box, width=3, border_radius=16)

        image_size = 120 if image else 0

        if image:
            image_box = pygame.Rect(
                box.centerx - image_size // 2,
                box.y + 16,
                image_size,
                image_size
            )

            scaled = pygame.transform.smoothscale(image, (image_size, image_size))
            pygame.draw.rect(screen, (245, 245, 245), image_box, width=3, border_radius=8)
            screen.blit(scaled, image_box.topleft)

            text_y = image_box.bottom + 10
        else:
            text_y = box.y + 30

        title_surf = self.title_font.render(title, True, (255, 255, 255))
        body_surf = self.body_font.render(body, True, (230, 230, 230))

        screen.blit(title_surf, (box.x + 28, text_y))
        screen.blit(body_surf, (box.x + 28, text_y + 44))

    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        surf = self.button_font.render(label, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=rect.center))
    
    def _handle_progression_unlock(self):
    # This method is responsible for setting progression flags
    # based on what the player just did in fishing.

        location = self.location

        if location is None:
            return

        # Example: Tutorial progression
        if location.id == 0:
            # First successful catch unlocks next area
            self.game.save_data.flags.add("tutorial_fish_caught")

# If this game is ever iterated upon stuff to add would be:
    # Catch minigame
    # Fish rarities