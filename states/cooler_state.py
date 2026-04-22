import pygame

from states.base_state import GameState


class CoolerState(GameState):
    # This state lets the player inspect the cooler, click fish, and manage each catch.
    # It behaves like a modal popup over the game world.
    def __init__(self, game):
        # Store the shared game reference so the cooler can access save data,
        # update player stats, and return to the previous state when done.
        super().__init__(game)

        # The cooler can show two screens:
        # "grid" = all caught fish in a 4-column layout
        # "detail" = one fish with Eat / Release / Return buttons
        self.mode = "grid"

        # This holds the index of the selected cooler entry when the player clicks a fish.
        self.selected_index = None

        # These are loaded from save data when the state starts.
        self.location = None
        self.background = None

        # Fonts are created once and reused.
        self.title_font = None
        self.body_font = None
        self.small_font = None
        self.button_font = None

        # Layout settings for the grid.
        self.grid_cols = 4
        self.slot_size = 120
        self.slot_gap = 18
        self.grid_rects = []

        # Buttons shown on the detail screen.
        self.eat_button_rect = pygame.Rect(260, 600, 180, 54)
        self.release_button_rect = pygame.Rect(540, 600, 180, 54)
        self.return_button_rect = pygame.Rect(820, 600, 220, 54)

        # Button shown on the grid screen.
        self.return_to_free_button_rect = pygame.Rect(980, 30, 220, 54)

        # Cache the current location background so the cooler can use a dimmed
        # version of the player's current area as the backdrop.
        self.background_cache = None

    # This runs once when the cooler opens.
    # It loads the current location and prepares fonts and background assets.
    def enter(self):
        self.location = self.game.save_data.current_location
        self.background_cache = self._load_background()

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.body_font = pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 24)
            self.button_font = pygame.font.SysFont(None, 30)

    # This is just the cleanup hook for consistency with the rest of the states.
    def exit(self):
        return super().exit()

    # This loads the current location background if one exists.
    # The cooler uses the current area as a visual backdrop, but darkened.
    def _load_background(self):
        if self.location is None or not getattr(self.location, "image", None):
            return None

        try:
            return self.game.load_image(self.location.image)
        except Exception:
            return None

    # This returns the cooler entry at a given index.
    # It supports both the new dictionary format and the older raw Catchable format.
    def _get_entry_data(self, index):
        if index < 0 or index >= len(self.game.save_data.cooler):
            return None, 0

        entry = self.game.save_data.cooler[index]

        # Preferred format:
        # {"catchable": <Catchable>, "mutation": <int>}
        if isinstance(entry, dict):
            catchable = entry.get("catchable")
            mutation = entry.get("mutation", 0)
            return catchable, mutation

        # Backward-compatible fallback:
        # raw Catchable objects are treated as mutation level 0
        return entry, 0

    # This safely gets the correct stat value for the stored mutation level.
    # It prevents index errors when the mutation value is higher than the list length.
    def _safe_stat_value(self, values, mutation):
        if not values:
            return 0

        index = max(0, min(int(mutation), len(values) - 1))
        return values[index]

    # This gets the correct image path for a stored catch.
    # Fish can have mutation-based image sets, while trash usually has one image.
    def _get_image_path(self, catchable, mutation):
        if catchable is None:
            return None

        if hasattr(catchable, "image_for_mutation"):
            path = catchable.image_for_mutation(mutation)
            if path:
                return path

        images = getattr(catchable, "images", None)

        if isinstance(images, (list, tuple)):
            if not images:
                return None
            index = max(0, min(int(mutation), len(images) - 1))
            return images[index]

        return images

    # This loads the image for a cooler entry and caches it only for this screen.
    def _load_entry_image(self, catchable, mutation):
        path = self._get_image_path(catchable, mutation)
        if not path:
            return None

        try:
            return self.game.load_image(path)
        except Exception:
            return None

    # This checks whether the cooler has anything in it.
    def _has_items(self):
        return len(self.game.save_data.cooler) > 0

    # This returns the currently selected item, if any.
    def _selected_entry(self):
        if self.selected_index is None:
            return None, 0

        return self._get_entry_data(self.selected_index)

    # This handles the rewards from eating a fish.
    # It adds energy and mutation to the player's save data.
    # It also sets progression flags when the mutation total crosses key thresholds.
    def _apply_eat_rewards(self, catchable, mutation):
        if catchable is None:
            return

        energy_gain = self._safe_stat_value(getattr(catchable, "energy", []), mutation)
        mutation_gain = self._safe_stat_value(getattr(catchable, "mutation_score", []), mutation)

        # Add stats to the player.
        self.game.save_data.energy += energy_gain
        self.game.save_data.mutation_level += mutation_gain

        # Add progression flags when thresholds are reached.
        # These are only added once because flags are stored in a set.
        if self.game.save_data.mutation_level >= 25:
            self.game.save_data.flags.add("25_mutation")

        if self.game.save_data.mutation_level >= 100:
            self.game.save_data.flags.add("100_mutation")

    # This removes a catch from the cooler by index.
    # It is used by both Eat and Release.
    def _remove_entry(self, index):
        if index < 0 or index >= len(self.game.save_data.cooler):
            return

        self.game.save_data.cooler.pop(index)

    # This starts a detail view for the clicked fish.
    # The player can then choose to Eat, Release, or Return to cooler.
    def _open_entry(self, index):
        self.selected_index = index
        self.mode = "detail"

    # This returns the player to the grid view without changing the cooler contents.
    def _return_to_grid(self):
        self.selected_index = None
        self.mode = "grid"

    # This eats the selected fish, gives rewards, removes it from the cooler,
    # and then returns the player to FreeState.
    def _eat_selected(self):
        catchable, mutation = self._selected_entry()
        if catchable is None:
            return

        self._apply_eat_rewards(catchable, mutation)
        self._remove_entry(self.selected_index)
        self.game.pop_state()

    # This releases the selected fish, removes it from the cooler,
    # and then returns the player to FreeState.
    def _release_selected(self):
        if self.selected_index is None:
            return

        self._remove_entry(self.selected_index)
        self.game.pop_state()

    # This handles all mouse and quit input for the cooler screen.
    # The grid screen uses fish-image buttons, and the detail screen uses action buttons.
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        if self.mode == "grid":
            # Return button from the grid screen.
            if self.return_to_free_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return

            # Fish image buttons.
            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    self._open_entry(idx)
                    return

        elif self.mode == "detail":
            # Eat button.
            if self.eat_button_rect.collidepoint(event.pos):
                self._eat_selected()
                return

            # Release button.
            if self.release_button_rect.collidepoint(event.pos):
                self._release_selected()
                return

            # Return to cooler button.
            if self.return_button_rect.collidepoint(event.pos):
                self._return_to_grid()
                return

    # The cooler has no time-based logic right now.
    def update(self, dt):
        return

    # This draws the cooler screen.
    # It uses a dimmed version of the current location as the backdrop,
    # then draws either the grid or the detail panel on top.
    def draw(self, screen):
        self._draw_background(screen)

        if self.mode == "grid":
            self._draw_grid_screen(screen)
        else:
            self._draw_detail_screen(screen)

    # This draws the backdrop using the current location background,
    # then adds a dark transparent layer to make the cooler pop out.
    def _draw_background(self, screen):
        w, h = screen.get_size()

        if self.background_cache is not None:
            bg = pygame.transform.smoothscale(self.background_cache, (w, h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((20, 20, 30))

        # Dark overlay to make the cooler feel like a modal screen.
        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

    # This draws the main cooler grid.
    # Each fish image acts like a button.
    def _draw_grid_screen(self, screen):
        screen_w, screen_h = screen.get_size()

        panel = pygame.Rect(60, 80, screen_w - 120, screen_h - 160)
        pygame.draw.rect(screen, (18, 18, 24), panel, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), panel, width=2, border_radius=18)

        title = self.title_font.render("Cooler", True, (255, 255, 255))
        screen.blit(title, (panel.x + 24, panel.y + 18))

        # Return to FreeState button.
        self._draw_button(screen, self.return_to_free_button_rect, "Return to free state")

        cooler = self.game.save_data.cooler

        if not cooler:
            empty = self.body_font.render("Your cooler is empty.", True, (230, 230, 230))
            screen.blit(empty, (panel.x + 24, panel.y + 80))
            self.grid_rects = []
            return

        # Layout math for the 4-column grid.
        cols = self.grid_cols
        slot_size = self.slot_size
        gap = self.slot_gap

        start_x = panel.x + 24
        start_y = panel.y + 80

        self.grid_rects = []

        for index, entry in enumerate(cooler):
            catchable, mutation = self._get_entry_data(index)

            col = index % cols
            row = index // cols

            x = start_x + col * (slot_size + gap)
            y = start_y + row * (slot_size + 44 + gap)

            rect = pygame.Rect(x, y, slot_size, slot_size)
            self.grid_rects.append(rect)

            # Draw the slot frame.
            pygame.draw.rect(screen, (45, 45, 60), rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

            # Load and draw the fish image if possible.
            image = self._load_entry_image(catchable, mutation)
            if image is not None:
                scaled = pygame.transform.smoothscale(image, (slot_size - 10, slot_size - 10))
                screen.blit(scaled, (rect.x + 5, rect.y + 5))

            # Show the fish name below the image.
            name_text = getattr(catchable, "name", "Unknown")
            name_surf = self.small_font.render(name_text, True, (255, 255, 255))
            name_rect = name_surf.get_rect(midtop=(rect.centerx, rect.bottom + 8))
            screen.blit(name_surf, name_rect)

        # Helpful hint text.
        hint = self.small_font.render("Click a fish to inspect it.", True, (220, 220, 220))
        screen.blit(hint, (panel.x + 24, panel.bottom - 34))

    # This draws the detail screen for a single selected fish.
    # The player can eat it, release it, or return to the grid.
    def _draw_detail_screen(self, screen):
        screen_w, screen_h = screen.get_size()
        panel = pygame.Rect(120, 70, screen_w - 240, screen_h - 140)

        pygame.draw.rect(screen, (18, 18, 24), panel, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), panel, width=2, border_radius=18)

        catchable, mutation = self._selected_entry()
        if catchable is None:
            msg = self.body_font.render("That item is no longer available.", True, (255, 255, 255))
            screen.blit(msg, (panel.x + 24, panel.y + 24))
            return

        title = self.title_font.render(getattr(catchable, "name", "Unknown"), True, (255, 255, 255))
        screen.blit(title, (panel.x + 24, panel.y + 20))

        # Draw the large image in the middle.
        image = self._load_entry_image(catchable, mutation)
        if image is not None:
            img_size = 220
            img_rect = pygame.Rect(panel.centerx - img_size // 2, panel.y + 90, img_size, img_size)
            pygame.draw.rect(screen, (45, 45, 60), img_rect, border_radius=14)
            pygame.draw.rect(screen, (255, 255, 255), img_rect, width=2, border_radius=14)
            scaled = pygame.transform.smoothscale(image, (img_size - 10, img_size - 10))
            screen.blit(scaled, (img_rect.x + 5, img_rect.y + 5))

        # Show the stat values that would be gained by eating this fish.
        energy_gain = self._safe_stat_value(getattr(catchable, "energy", []), mutation)
        mutation_gain = self._safe_stat_value(getattr(catchable, "mutation_score", []), mutation)

        energy_text = self.body_font.render(f"Energy: +{energy_gain}", True, (230, 230, 230))
        screen.blit(energy_text, (panel.x + 24, panel.y + 340))

        # Buttons.
        self._draw_button(screen, self.eat_button_rect, "Eat")
        self._draw_button(screen, self.release_button_rect, "Release")
        self._draw_button(screen, self.return_button_rect, "Return to cooler")

    # This draws one rounded button with centered text.
    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        surf = self.button_font.render(label, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=rect.center))