import pygame
import numpy as np

from states.base_state import GameState #Base class
from fishes import minnow, perch, pike, catfish, weeds


class FishingState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.location = None
        self.catch = None #
        self.catch_mutation = 0

        # Defining constants for the reveal of the catch (mini cutscene to be played when the player 'fishes')
        self.phase = "reveal"
        self.phase_started_at = 0
        self.reveal_duration_ms = 5000

        self.background = None

        self.title_font = None
        self.body_font = None
        self.button_font = None

        self.release_button = pygame.Rect(340, 560, 180, 54) #Create button for releasing the catch
        self.cooler_button = pygame.Rect(760, 560, 180, 54) #Create button for adding the catch to cooler

        # Get image of catch
        self.catch_image = None
        self.catch_image_size = 180
        self.catch_image_rect = pygame.Rect(0, 0, self.catch_image_size, self.catch_image_size)

    def enter(self):
        self.location = self.game.save_data.current_location #Get current location

        if self.location.image:
            self.background = self.game.load_image(self.location.image)
        else:
            self.background = None

        self.catch = self._roll_catch()
        self.catch_mutation = (
            self.location.mutation_level() if self.catch.isFish else 0 # Set fish mutation level
        )
        self.catch_image = self._load_catch_image()

        self.phase = "reveal"
        self.phase_started_at = pygame.time.get_ticks() #Get current time to run 'reveal' phase for just 5 seconds

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 54)
            self.body_font = pygame.font.SysFont(None, 34)
            self.button_font = pygame.font.SysFont(None, 30)

    def exit(self):
        return super().exit()

    def update(self, dt):
        if self.phase == "reveal":
            now = pygame.time.get_ticks() # Get current time
            if now - self.phase_started_at >= self.reveal_duration_ms:
                # If 'reveal' phase has run for more that 5 seconds, move on to choice
                self.phase = "choice"

    def handle_event(self, event):
        # If the game is quit during the event
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        # During reveal phase, the player cannot take actions
        if self.phase != "choice":
            return

        # Clicking buttons to decide what to do with Catch
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.release_button.collidepoint(event.pos):
                self._release_catch()
            elif self.cooler_button.collidepoint(event.pos):
                self._add_to_cooler()

    def draw(self, screen):
        self._draw_background(screen)

        if self.phase == "reveal": 
            self._draw_message_box(
                screen,
                "You cast your line...",
                image= None #assets/cast.png
            )
        else: # Show catch
            self._draw_message_box(
                screen,
                f"You caught a {self.catch.name}.",
                image=self.catch_image
            )
            self._draw_button(screen, self.release_button, "Release") #Create a button to release the catch
            self._draw_button(screen, self.cooler_button, "Add to cooler") #Create a button to add the catch to cooler

    # Get random catch (based on location data)
    def _roll_catch(self):
        # 0 = fish, 1 = trash
        result = self.location.trash_or_fish()

        # If the item is trash
        if result == 1:
            return weeds

        # Set fishing pool based on location
        pool = self._fish_pool_for_location()

        # Choose a fish object
        return np.random.choice(pool)

    def _fish_pool_for_location(self):
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
        return [minnow] #Base case

    # Go back to previous game state if catch is released
    def _release_catch(self):
        self.game.pop_state()

    # Add fish to cooler and go back to previous game state
    def _add_to_cooler(self):
        self.game.save_data.cooler.append(self.catch)
        self.game.pop_state()

    # Have current location be in the background
    def _draw_background(self, screen):
        if self.background is not None:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill((25, 35, 50))

    # Draw message box along with image
    def _draw_message_box(self, screen, title_text, body_text, image=None):
        box = pygame.Rect(120, 420, 1040, 230)
        pygame.draw.rect(screen, (20, 20, 20), box, border_radius=16)
        pygame.draw.rect(screen, (240, 240, 240), box, width=3, border_radius=16)

        # Image box (always centered at top of message box)
        image_size = 120 if image is not None else 0
        image_box = pygame.Rect(
            box.centerx - image_size // 2,
            box.y + 16,
            image_size,
            image_size
       )

        if image is not None:
            scaled = pygame.transform.smoothscale(image, (image_size, image_size))
            pygame.draw.rect(screen, (245, 245, 245), image_box, width=3, border_radius=8)
            screen.blit(scaled, image_box.topleft)

            text_y_offset = image_box.bottom + 10
        else:
            text_y_offset = box.y + 30

        title = self.title_font.render(title_text, True, (255, 255, 255))
        body = self.body_font.render(body_text, True, (230, 230, 230))

        screen.blit(title, (box.x + 28, text_y_offset))
        screen.blit(body, (box.x + 28, text_y_offset + 40))
    
    # Create buttons
    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (60, 60, 80), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        text = self.button_font.render(label, True, (255, 255, 255))
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

    # Get image for catch
    def _load_catch_image(self):
        image_path = None

        if self.catch.isFish:
            image_path = self.catch.image_for_mutation(self.catch_mutation)
        else:
            image_path = self.catch.images

        if image_path is None:
            return None

        image = self.game.load_image(image_path)
        return pygame.transform.smoothscale(image, (self.catch_image_size, self.catch_image_size))