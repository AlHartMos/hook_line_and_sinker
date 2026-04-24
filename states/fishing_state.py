import pygame
import numpy as np

from states.base_state import GameState
from fishes import trash, minnow, perch, pike, catfish
from dialogues.location_starters.valley_starter import valley_intro_after_fish


class FishingState(GameState):
    # This state handles the full fishing interaction.
    # It temporarily replaces FreeState until the player finishes the fishing action.
    def __init__(self, game):
        super().__init__(game)

        # Current location is loaded when the state starts.
        self.location = None
        self.background = None

        # These store the result of the fishing attempt.
        self.catch = None
        self.catch_mutation = 0
        self.catch_image = None

        # Two-phase system:
        # "reveal" → short delay before the player sees the result
        # "choice" → the player chooses Release or Add to cooler
        self.phase = "reveal"
        self.phase_started_at = 0
        self.reveal_duration_ms = 5000

        # Fonts are created once and reused.
        self.title_font = None
        self.body_font = None
        self.button_font = None
        self.small_font = None

        # Choice buttons shown after the catch reveal.
        # Eat is only shown if the catch is a fish or weeds.
        self.eat_button     = pygame.Rect(0, 0, 200, 60)
        self.release_button = pygame.Rect(0, 0, 200, 60)
        self.cooler_button  = pygame.Rect(0, 0, 220, 60)

    def enter(self):
        # Called once when fishing starts.
        # We load the location first, because all fishing logic depends on it.
        self.location = self.game.save_data.current_location
        self.background = self._load_background()

        # Roll the catch before any progression logic runs.
        self.catch = self._roll_catch()
        self.catch_mutation = self._roll_mutation_if_needed()
        self.catch_image = self._load_catch_image()

        # Fishing costs energy immediately when the action begins.
        self.game.save_data.energy = max(0, self.game.save_data.energy - 5)

        # Progression rules run after the catch exists.
        # This keeps the tutorial logic tied to the actual result of fishing.
        self._handle_progression()

        self.phase = "reveal"
        self.phase_started_at = pygame.time.get_ticks()

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 54)
            self.body_font = pygame.font.SysFont(None, 34)
            self.button_font = pygame.font.SysFont(None, 30)
        self.small_font = pygame.font.SysFont(None, 24)

    def exit(self):
        return super().exit()

    # ---------- CORE CATCH LOGIC ----------

    def _roll_catch(self):
        # Use the location's boolean fish/trash roll.
        # True means fish, False means trash.
        if self.location.is_fish():
            pool = self._fish_pool_for_location()
            return np.random.choice(pool)

        return np.random.choice(trash)

    def _fish_pool_for_location(self):
        # Defines which fish are available in each location.
        # This can be expanded later into a per-location data system.

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

        # Base case fallback.
        return [minnow]

    def _roll_mutation_if_needed(self):
        # Only fish have mutation levels.
        if not getattr(self.catch, "isFish", False):
            return 0

        return self.location.mutation_level()

    # ---------- PROGRESSION LOGIC ----------

    def _queue_popup(self, title, message):
        # Store a popup request so FreeState can show it once fishing ends.
        # This keeps popup display separate from fishing logic.
        self.game.save_data.pending_popup = {
            "title": title,
            "message": message
        }

    def _handle_progression(self):
        # Location-specific progression dispatcher.
        if self.location is None:
            return

        if self.location.id == 0:
            self._handle_tutorial_progression()
        elif self.location.id == 1:
             self._handle_lake_progression()
        elif self.location.id == 2:
            self._handle_valley_progression()

    def _handle_tutorial_progression(self):
        # Tutorial progression only happens when the player catches trash.
        # This teaches the player the fishing loop and unlocks the next area.
        if self.catch.isFish:
            return

        self.game.save_data.tutorial_trash_caught += 1

        if (
            self.game.save_data.tutorial_trash_caught == 1
            and not self.game.save_data.tutorial_first_trash_popup_shown
        ):
            self._queue_popup(
                "Tutorial",
                "No problems, not everything works the first time you do it. Just try again, and maybe you will catch a fish."
            )
            self.game.save_data.tutorial_first_trash_popup_shown = True

        elif (
            self.game.save_data.tutorial_trash_caught == 2
            and not self.game.save_data.tutorial_second_trash_popup_shown
        ):
            self._queue_popup(
                "Tutorial",
                "Sorry, you haven’t caught anything interesting. Whenever you fish your energy bar is reduced slightly; in order to restore it you need to eat fish, and to do that you need to catch one first. So let’s just try it once more."
            )
            self.game.save_data.tutorial_second_trash_popup_shown = True

        elif (
            self.game.save_data.tutorial_trash_caught == 3
            and not self.game.save_data.tutorial_third_trash_popup_shown
        ):
            self._queue_popup(
                "Tutorial",
                "With your luck being on its lowest you decide to move along the lake further. Maybe in some other place you’ll be in luck"
            )
            self.game.save_data.tutorial_third_trash_popup_shown = True

            # This is the progression flag FreeState checks to show the next-location button.
            self.game.save_data.flags.add("three_trash_caught")

    def _handle_lake_progression(self):
    # Lake progression only happens when the player catches fish.
    # This teaches the player the fishing loop, hints at mutation, and unlocks the next area.
        if self.catch.isTrash:
            return
        
        self.game.save_data.lake_fish_caught += 1
        if (
            self.game.save_data.lake_fish_caught == 1
            and not self.game.save_data.lake_first_fish_popup_shown
        ):
            # Change fish to a level 0 mutant
            self.catch_mutation = 0
            self.catch_image = self._load_catch_image()

            self._queue_popup(
                "Lake",
                "Great! As you saw, you need to pick what you want to do with the fish you catch. Let's store them all in the cooler for now, but usually you could also eat it to restore energy or release it."
            )
            self.game.save_data.lake_first_fish_popup_shown = True
        elif (
            self.game.save_data.lake_fish_caught == 2
            and not self.game.save_data.lake_second_fish_popup_shown
        ):
            self._queue_popup(
                "Lake",
                "Well done, you began to get the gist of it! Now that we have a few fish, let’s check our cooler. To look into your cooler press Cooler"
            )
            # Change fish to a level 0 mutant
            self.catch_mutation = 0
            self.catch_image = self._load_catch_image()

            self.game.save_data.lake_second_fish_popup_shown = True
        elif (
            self.game.save_data.lake_fish_caught == 3
            and not self.game.save_data.lake_third_fish_popup_shown
        ):
            
            self._queue_popup(
                "Lake",
                "As you look at it you are both proud of yourself, and with a bit of a question as to the fish's appearance"
            )
            # Change fish to a level 1 mutant
            self.catch_mutation = 1
            self.catch_image = self._load_catch_image()

            # Making it harder to catch fish so the player wants to move on
            self.location.trash_fish_ratio = [0.9, 0.1]

            self.game.save_data.lake_third_fish_popup_shown = True
            # This is the progression flag FreeState checks to show the next-location button.
            self.game.save_data.flags.add("three_fish_caught_lake")

    def _handle_valley_progression(self):
        # Only trigger on first fish caught
        if self.catch.isTrash:
           return

        if "valley_first_fish" not in self.game.save_data.flags:
            self.game.save_data.flags.add("valley_first_fish")

            # Queue dialogue
            self.game.save_data.pending_dialogue = {
                "conversation": valley_intro_after_fish,
                "start_node": "intro"
            }

            # Enable overlay button functionality
            self.game.save_data.flags.add("valley_paths_unlocked")


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
        # After the reveal delay, switch to the choice phase.
        if self.phase == "reveal":
            now = pygame.time.get_ticks()
            if now - self.phase_started_at >= self.reveal_duration_ms:
                self.phase = "choice"

    # ---------- INPUT ----------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return
        
        # Get positions of buttons
        if self.phase == "choice":
            self._update_button_positions()

        # Ignore input during the reveal phase
        if self.phase != "choice":
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Eat is only available for fish catches.
            if self.catch is not None and self.catch.isFish:
                if self.eat_button.collidepoint(event.pos):
                    self._eat_catch()
                    return

            if self.release_button.collidepoint(event.pos):
                self.game.pop_state()
                return

            if self.cooler_button.collidepoint(event.pos):
                capacity = self.game.save_data._cooler_capacity()

                if len(self.game.save_data.cooler) < capacity:
                    self.game.save_data.cooler.append({
                    "catchable": self.catch,
                    "mutation": self.catch_mutation
                    })
                    self.game.pop_state()

                else:
                    self.game.save_data.pending_popup = {
                        "title": "Cooler Full",
                        "message": "Your cooler is full. You cannot store more fish."
                    }
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

    def _draw_background(self, screen):
        w, h = screen.get_size()

        if self.background:
            bg = pygame.transform.smoothscale(self.background, (w, h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((25, 35, 50))

    def _draw_message_box(self, screen, title, body="", image=None):
        screen_w, screen_h = screen.get_size()

        # --- MAIN PANEL ---
        panel = pygame.Rect(160, 120, screen_w - 320, screen_h - 240)

        pygame.draw.rect(screen, (18, 18, 24), panel, border_radius=20)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2, border_radius=20)

        center_x = panel.centerx

        # --- IMAGE (large + centered) ---
        image_size = 180
        image_y = panel.y + 40

        if image:
            img_rect = pygame.Rect(
                center_x - image_size // 2,
                image_y,
                image_size,
                image_size
            )

            scaled = pygame.transform.smoothscale(image, (image_size, image_size))
            pygame.draw.rect(screen, (240, 240, 240), img_rect, 2, border_radius=10)
            screen.blit(scaled, img_rect.topleft)

            text_y = img_rect.bottom + 30
        else:
            text_y = panel.y + 40

        # --- TITLE (centered) ---
        title_surf = self.title_font.render(title, True, (255, 255, 255))
        title_rect = title_surf.get_rect(center=(center_x, text_y))
        screen.blit(title_surf, title_rect)

        # --- BUTTONS (horizontal, centered) ---
        button_y = panel.bottom - 100
        spacing = 220

        buttons = []

        # Release (always)
        buttons.append(("Release", self.release_button))

        # Eat (only if fish or weeds)
        if self.catch is not None and (self.catch.isFish or self.catch.name == "Lake Weed Cluster"):
            buttons.append(("Eat", self.eat_button))

        # Add to cooler
        buttons.append(("Add to cooler", self.cooler_button))

        # Center buttons
        total_width = spacing * (len(buttons) - 1)
        start_x = center_x - total_width // 2

        if self.phase == "choice":
            for i, (label, rect) in enumerate(buttons):
                rect.center = (start_x + i * spacing, button_y)
                self._draw_button(screen, rect, label)

    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        text = self.button_font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    def _safe_stat_value(self, values, mutation):
        # Returns the stat value for the current mutation level,
        # while safely clamping the index into the valid range.
        if not values:
            return 0

        index = max(0, min(int(mutation), len(values) - 1))
        return values[index]
    

    def _apply_eat_rewards(self):
        # Eating a fish gives the player energy and mutation progress.
        # The exact reward depends on the fish and its mutation level.
        if self.catch is None or not getattr(self.catch, "isFish", False):
            return
    
        energy_gain = self._safe_stat_value(getattr(self.catch, "energy", []), self.catch_mutation)
        mutation_gain = self._safe_stat_value(getattr(self.catch, "mutation_score", []), self.catch_mutation)
    
        self.game.save_data.energy += energy_gain
        self.game.save_data.mutation_level += mutation_gain
    
        # Set mutation milestone flags once the player reaches the threshold.
        # These flags can be checked elsewhere for story or progression logic.
        if self.game.save_data.mutation_level >= 25:
            self.game.save_data.flags.add("25_mutation")
    
        if self.game.save_data.mutation_level >= 100:
            self.game.save_data.flags.add("100_mutation")
    
    def _eat_catch(self):
        # Eat the caught fish immediately and return to FreeState.
        self._apply_eat_rewards()
        self.game.pop_state()

    def _update_button_positions(self):
        screen_w, screen_h = self.game.screen.get_size()

        panel = pygame.Rect(160, 120, screen_w - 320, screen_h - 240)
        center_x = panel.centerx

        button_y = panel.bottom - 100
        spacing = 220

        buttons = []

        # Release
        buttons.append(self.release_button)

        # Eat
        if self.catch is not None and (self.catch.isFish or self.catch.name == "Lake Weed Cluster"):
            buttons.append(self.eat_button)

        # Cooler
        buttons.append(self.cooler_button)

        total_width = spacing * (len(buttons) - 1)
        start_x = center_x - total_width // 2

        for i, rect in enumerate(buttons):
            rect.center = (start_x + i * spacing, button_y)