import pygame

from states.base_state import GameState
from states.dialogue_state import DialogueState
from states.fishing_state import FishingState
from states.button_overlay_state import ButtonOverlayState
from states.cooler_state import CoolerState
from states.popup_state import PopupState


class FreeState(GameState):
    # This is the main exploration state.
    # It shows the current location, the permanent fishing button,
    # the optional "move on" button, and it can trigger an arrival conversation.
    def __init__(self, game):
        # Store the shared game reference so this state can access save data,
        # the stack, and image loading.
        super().__init__(game)

        # These are refreshed whenever the state starts or the location changes.
        self.location = None
        self.background = None

        # This helps make sure the arrival conversation only triggers once
        # for the current location entry.
        self.arrival_checked = False

        # Button positions for the always-available world actions.
        # The overlay button is intended to live in the top-left corner,
        # so these controls stay in the bottom corners.
        self.fishing_button_rect = pygame.Rect(40, 620, 220, 56)
        self.cooler_button_rect = pygame.Rect(500, 620, 220, 56)
        self.next_location_button_rect = pygame.Rect(1020, 620, 220, 56)

        # Fonts are created once and reused.
        self.title_font = None
        self.button_font = None
        self.small_font = None

    # This runs when FreeState becomes active.
    # It loads the player's current location and adds the overlay button
    # if it is not already present.
    def enter(self):
        self.location = self.game.save_data.current_location
        self.background = self._load_background()

        self.arrival_checked = False

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.button_font = pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 24)

    # This is a cleanup hook.
    def exit(self):
        # Remove overlay if it exists
        self.game.state_stack = [
            s for s in self.game.state_stack
            if not isinstance(s, ButtonOverlayState)
        ]
        return super().exit()
    
    # This checks whether the overlay is already in the stack.
    # It prevents FreeState from adding duplicate overlay states.
    def _overlay_exists(self):
        for state in self.game.state_stack:
            if isinstance(state, ButtonOverlayState):
                return True
            
        return False

    # This safely loads the background image for the current location.
    # If the image is missing or fails to load, the state can still draw
    # with a fallback background color.
    def _load_background(self):
        if self.location is None or not self.location.image:
            return None

        try:
            return self.game.load_image(self.location.image)
        except Exception:
            return None

    # This returns True when the move-on button should appear.
    # The button only shows if:
    # - there is a next location
    # - a flag says the player has unlocked it
    def can_move_on(self):
        if self.location is None:
            return False

        if self.location.next_location is None:
            return False

        if self.location.next_location_flag is None:
            return False

        return self.location.next_location_flag in self.game.save_data.flags

    # This starts the arrival conversation if the location has one
    # and the player has not seen it yet.
    def _maybe_start_arrival_conversation(self):
        if self.location is None:
            return

        if self.location.arrival_conversation is None:
            return

        # If full NPC conversations are disabled, skip the cutscene-style intro.
        if not getattr(self.game, "npc_interactions_enabled", True):
            return

        arrival_flag = self.location.arrival_flag or f"visited_location_{self.location.id}"

        if arrival_flag in self.game.save_data.flags:
            return

        # Mark it immediately so it does not re-trigger.
        self.game.save_data.flags.add(arrival_flag)

        # Push the conversation on top of FreeState.
        # FreeState remains underneath and continues afterward.
        self.game.push_state(
            DialogueState(
                self.game,
                conversation=self.location.arrival_conversation,
                start_node=self.location.arrival_start_node
            )
        )

    # This refreshes the current location in place.
    # It is used when the player moves on to the next area.
    # We do NOT replace FreeState with a new FreeState, because the overlay
    # is sitting on top of it and should stay in place.
    def _set_location(self, new_location):
        old_location = self.location

        self.game.save_data.current_location = new_location
        self.location = new_location
        self.background = self._load_background()
        self.arrival_checked = False

        # --- APPLY TRAVEL COST ---
        if old_location and new_location:

            # Only apply between Lake (1) and Valley (2)
            if (
                (old_location.id == 1 and new_location.id == 2)
            ):
                travel_cost = getattr(self, "_pending_travel_cost", 0)
                self.game.save_data.cooler = [] # Lose everything in the cooler

                self.game.save_data.energy = max(
                    0,
                    self.game.save_data.energy - travel_cost
                )

                # --- ARRIVAL BUFFER ---
                # Ensure player has at least 10 energy to fish
                if self.game.save_data.energy < 10:
                    self.game.save_data.energy = 10

                # Feedback popup
                self.game.save_data.pending_popup_after_dialogue = {
                    "title": "Exhaustion",
                    "message": "The journey drained your energy."
                }

        # Clear stored cost after use
        self._pending_travel_cost = 0

    # This handles the move-on button.
    # It updates the current location directly, then waits for the next update
    # tick to trigger the new arrival conversation if there is one.
    def _go_to_next_location(self):
        if not self.can_move_on():
            return

        # --- TRAVEL COST SETUP ---
        TRAVEL_PERCENT = 0.2  # 20% energy cost
        MIN_ENERGY_AFTER_TRAVEL = 10

        current_energy = self.game.save_data.energy
        travel_cost = int(current_energy * TRAVEL_PERCENT)

        remaining_energy = current_energy - travel_cost

        # --- TOO TIRED CHECK ---
        # Player must still have enough energy left AFTER travel
        if remaining_energy < MIN_ENERGY_AFTER_TRAVEL:
            self.game.save_data.pending_popup_after_dialogue = {
                "title": "Too Tired",
                "message": "You are too exhausted to make the journey."
            }
            return

        # Store the computed cost so we don't recalculate inconsistently
        self._pending_travel_cost = travel_cost

        self._set_location(self.location.next_location)

    # This handles input while the player is exploring.
    # Fishing and moving on are always available here.
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.fishing_button_rect.collidepoint(event.pos):
                # Fishing is a temporary state, so it gets pushed on top.
                self.game.push_state(FishingState(self.game))
                return

            if self.next_location_button_rect.collidepoint(event.pos):
                self._go_to_next_location()
                return
            
            if self.cooler_button_rect.collidepoint(event.pos):
                self.game.push_state(CoolerState(self.game))
                return

        return

    # This updates the free-roam world logic.
    # The first time this runs after entering a location, it checks for any
    # arrival conversation that should be shown.
    def update(self, dt):
        # Handle the one-time arrival conversation for the location.
        if not self.arrival_checked:
            self.arrival_checked = True
            self._maybe_start_arrival_conversation()

        from dialogues.location_starters.valley_starter import valley_intro_after_fish
        if (
            self.location is not None
            and self.location.id == 2
            and self.game.save_data.energy >= 78
            and "valley_paths_unlocked" not in self.game.save_data.flags
        ):
            self.game.save_data.flags.add("valley_paths_unlocked")

            self.game.save_data.pending_dialogue = {
                "conversation": valley_intro_after_fish,
                "start_node": "intro"
            }

            return  # IMPORTANT: stop further updates this frame
        
        if getattr(self.game.save_data, "pending_dialogue", None):
            data = self.game.save_data.pending_dialogue
            self.game.save_data.pending_dialogue = None

            self.game.push_state(
                DialogueState(
                    self.game,
                    data["conversation"],
                    data["start_node"]
                )
            )
            return
        
        sd = self.game.save_data

        # --- ENERGY 0 → GAME OVER ---
        if sd.energy <= 0 and "game_over_energy" not in sd.flags:
            sd.flags.add("game_over_energy")

            sd.pending_popup = {
                "title": "Exhaustion",
                "message": "You have no energy left.",
                "end_game": True
            }
            return


        # --- MUTATION 25 ---
        if sd.mutation_level >= 25 and "mutation_25_popup" not in sd.flags:
            sd.flags.add("mutation_25_popup")

            sd.pending_popup = {
                "title": "Something's happening...",
                "message": "You feel something changing inside you.",
                "end_game": False
            }
            return


        # --- MUTATION 100 → GAME OVER ---
        if sd.mutation_level >= 100 and "mutation_100_popup" not in sd.flags:
            sd.flags.add("mutation_100_popup")

            sd.pending_popup = {
                "title": "Transformation",
                "message": "You are no longer human.",
                "end_game": True
            }
            return
        
        # --- overlay add ---
        valley_done = (
            "asked_bertha_treasure" in self.game.save_data.flags and
            "meeting_hans_complete" in self.game.save_data.flags and
            "felix_done" in self.game.save_data.flags
        )
        
        if (
            "valley_paths_unlocked" in self.game.save_data.flags
            and not valley_done
            and not isinstance(self.game.state, DialogueState)
        ):
            if not any(isinstance(s, ButtonOverlayState) for s in self.game.state_stack):
                self.game.push_state(ButtonOverlayState(self.game))

        # --- overlay remove ---
        if valley_done and any(isinstance(s, ButtonOverlayState) for s in self.game.state_stack):
            self.game.state_stack = [
                s for s in self.game.state_stack
                if not isinstance(s, ButtonOverlayState)
            ]
        
        # If dialogue just finished and we have a delayed popup
        if (
            not any(isinstance(s, DialogueState) for s in self.game.state_stack)
            and getattr(self.game.save_data, "pending_popup_after_dialogue", None)
        ):
            popup = self.game.save_data.pending_popup_after_dialogue
            self.game.save_data.pending_popup_after_dialogue = None
        
            self.game.push_state(
                PopupState(
                    self.game,
                    title=popup["title"],
                    message=popup["message"]
                )
            )
            return
                
        # If another state requested a system popup, show it now.
        if self.game.save_data.pending_popup is not None:
            popup = self.game.save_data.pending_popup
            self.game.save_data.pending_popup = None

            self.game.push_state(
                PopupState(
                    self.game,
                    title=popup["title"],
                    message=popup["message"]
                )
            )
            return
        

    # This draws the current location and the permanent world buttons.
    # The upper-left corner is left open so the overlay button can live there.
    def draw(self, screen):
        screen_w, screen_h = screen.get_size()

        # Draw the background first.
        if self.background is not None:
            bg = pygame.transform.smoothscale(self.background, (screen_w, screen_h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((30, 35, 45))

        # Draw a small title panel with the current location name.
        title_box = pygame.Rect(20, 20, 320, 54)
        pygame.draw.rect(screen, (15, 15, 20), title_box, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), title_box, width=2, border_radius=12)

        title_text = self.location.name if self.location else "Unknown Location"
        title_surf = self.title_font.render(title_text, True, (255, 255, 255))
        screen.blit(title_surf, (title_box.x + 16, title_box.y + 10))

        # Draw a small energy box in the top-right corner.
        # This keeps it visible in free state without overlapping the title,
        # fishing button, move-on button, or the overlay button.
        energy_box = pygame.Rect(screen_w - 180, 20, 160, 44)
        pygame.draw.rect(screen, (15, 15, 20), energy_box, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), energy_box, width=2, border_radius=12)

        energy_text = self.small_font.render(
            f"Energy: {self.game.save_data.energy}",
            True,
            (255, 255, 255)
            )           
        screen.blit(energy_text, (energy_box.x + 16, energy_box.y + 16))

        # Draw the permanent fishing and cooler buttons.
        self._draw_button(screen, self.fishing_button_rect, "Fish")
        self._draw_button(screen, self.cooler_button_rect, "Cooler")

        # Only draw the move-on button if the unlock flag is present.
        if self.can_move_on():
            self._draw_button(screen, self.next_location_button_rect, "Move on")

    # This draws a rounded button with centered text.
    # It keeps the free-state UI consistent and avoids repeating draw code.
    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        label_surf = self.button_font.render(label, True, (255, 255, 255))
        label_rect = label_surf.get_rect(center=rect.center)
        screen.blit(label_surf, label_rect)