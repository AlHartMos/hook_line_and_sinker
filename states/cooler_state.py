import pygame
from states.base_state import GameState

class CoolerState(GameState):
    def __init__(self, game, mode="grid", trade_request=None):
        super().__init__(game)

        # Mode determines how the cooler behaves:
        # "grid"   → normal inventory view
        # "detail" → viewing one specific fish
        # "trade"  → selecting fish for a trade
        self.mode = mode

        # Trade configuration passed from DialogueState (only used in trade mode)
        self.trade_request = trade_request

        # Stores indices of fish selected during trading
        self.selected_indices = set()

        # Index of currently selected fish (used in detail mode)
        self.selected_index = None

        # Current location and background for visual consistency
        self.location = None
        self.background = None

        # Fonts (initialized once in enter())
        self.title_font = None
        self.body_font = None
        self.small_font = None
        self.button_font = None

        # Panel size
        self.panel_rect = pygame.Rect(60, 160, 1160, 320)

        # Grid layout settings
        self.grid_cols = 4
        self.slot_size = 240
        self.slot_gap = 30
        self.grid_rects = []

        # Buttons for detail mode
        self.eat_button_rect = pygame.Rect(260, 600, 180, 54)
        self.release_button_rect = pygame.Rect(540, 600, 180, 54)
        self.return_button_rect = pygame.Rect(820, 600, 220, 54)

        # Buttons for trade mode
        self.confirm_button_rect = pygame.Rect(500, 600, 180, 54)
        self.cancel_button_rect = pygame.Rect(720, 600, 180, 54)

        # Button to exit cooler
        self.return_to_free_button_rect = pygame.Rect(980, 30, 220, 54)

        # Buttons to move between pages
        self.prev_button = pygame.Rect(120, 520, 80, 50)
        self.next_button = pygame.Rect(1120, 520, 80, 50)

        # Cached background image
        self.background_cache = None

        # Page mechanic
        self.page = 0
        self.items_per_page = self.grid_cols  # 4 items per page (1 row)

    def enter(self):
        """
        Called when the cooler state is opened.
        Loads background and initializes fonts.
        """
        self.location = self.game.save_data.current_location
        self.background_cache = self._load_background()

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.body_font = pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 24)
            self.button_font = pygame.font.SysFont(None, 30)

    def _load_background(self):
        """
        Attempts to load the current location background.
        Falls back to None if unavailable.
        """
        if self.location and getattr(self.location, "image", None):
            try:
                return self.game.load_image(self.location.image)
            except:
                pass
        return None

    # ---------- DATA HELPERS ----------

    def _get_entry_data(self, index):
        """
        Returns (catchable, mutation_level) for a cooler entry.
        Supports both dict format and legacy format.
        """
        entry = self.game.save_data.cooler[index]

        if isinstance(entry, dict):
            return entry.get("catchable"), entry.get("mutation", 0)

        return entry, 0

    def _safe_stat_value(self, values, mutation):
        """
        Safely retrieves a stat value from a list using mutation level.
        Prevents out-of-range errors.
        """
        if not values:
            return 0
        return values[max(0, min(mutation, len(values) - 1))]

    # ---------- TRADE LOGIC ----------

    def _confirm_trade(self):
        trade = self.trade_request
        required = trade.get("required_fish", 0)
        total_required = trade.get("total_required", None)

        selected = list(self.selected_indices)

        # --- NOT ENOUGH (per-visit) ---
        if len(selected) < required:
            self.game.pop_state()
            dialogue = self.game.state
            dialogue.node = trade["fail_node"]
            dialogue.line_index = 0
            return

        # --- REMOVE FISH ---
        for idx in sorted(selected, reverse=True):
            self.game.save_data.cooler.pop(idx)

        # --- FELIX CUMULATIVE LOGIC ---
        if total_required is not None:
            if not hasattr(self.game.save_data, "felix_fish_given"):
                self.game.save_data.felix_fish_given = 0

            self.game.save_data.felix_fish_given += len(selected)

            if self.game.save_data.felix_fish_given >= total_required:
                next_node = trade["success_node"]
            else:
                next_node = trade["fail_node"]

            self.game.pop_state()

            dialogue = self.game.state
            dialogue.node = next_node
            dialogue.line_index = 0
            return

        # --- STANDARD PURCHASE (Bertha) ---
        self.game.save_data.flags.add(trade["purchase_flag"])

        self.game.pop_state()

        dialogue = self.game.state
        dialogue.node = trade["resume_node"]
        dialogue.line_index = 0

        # Clear selection
        self.selected_indices.clear()

    # ---------- INPUT HANDLING ----------
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return
        # --- PAGES ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                max_page = (len(self.game.save_data.cooler) - 1) // self.items_per_page
                self.page = min(max_page, self.page + 1)
            elif event.key == pygame.K_LEFT:
                self.page = max(0, self.page - 1)
        # --- ONLY handle left click from here on ---
        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return
        # --- CLICK OUTSIDE PANEL ---
        if not self.panel_rect.collidepoint(event.pos):
            self.game.pop_state()
            return
        # ---------- TRADE MODE ----------
        if self.confirm_button_rect.collidepoint(event.pos):
            self._confirm_trade()
            return
        if self.cancel_button_rect.collidepoint(event.pos):
            self.game.pop_state()
            return
        
        if self.mode == "trade":
            required = self.trade_request.get("required_fish", 0)
            start = self.page * self.items_per_page
            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    real_index = start + idx
                    if real_index in self.selected_indices:
                        self.selected_indices.remove(real_index)
                    else:
                        if len(self.selected_indices) < required:
                            self.selected_indices.add(real_index)
                    return
            if self.confirm_button_rect.collidepoint(event.pos):
                self._confirm_trade()
                return
            if self.cancel_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return
        # ---------- GRID MODE ----------
        elif self.mode == "grid":
            if self.return_to_free_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return
            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    start = self.page * self.items_per_page
                    self.selected_index = start + idx
                    self.mode = "detail"
                    return
        # ---------- DETAIL MODE ----------
        elif self.mode == "detail":
            if self.eat_button_rect.collidepoint(event.pos):
                self._eat_selected()
                return
            if self.release_button_rect.collidepoint(event.pos):
                self._release_selected()
                return
            if self.return_button_rect.collidepoint(event.pos):
                self.mode = "grid"
                return
            
        # Arrows
        if self.prev_button.collidepoint(event.pos):
            self.page = max(0, self.page - 1)
            return

        if self.next_button.collidepoint(event.pos):
            max_page = (len(self.game.save_data.cooler) - 1) // self.items_per_page
            self.page = min(max_page, self.page + 1)
            return
            
    # ---------- ACTIONS ----------
    def _eat_selected(self):
        """
        Eats the selected fish:
        - Adds energy and mutation
        - Applies milestone flags
        - Removes fish
        """
        catchable, mutation = self._get_entry_data(self.selected_index)

        energy = self._safe_stat_value(catchable.energy, mutation)
        mutation_gain = self._safe_stat_value(catchable.mutation_score, mutation)

        self.game.save_data.energy += energy
        self.game.save_data.mutation_level += mutation_gain

        if self.game.save_data.mutation_level >= 25:
            self.game.save_data.flags.add("25_mutation")
        if self.game.save_data.mutation_level >= 100:
            self.game.save_data.flags.add("100_mutation")

        self.game.save_data.cooler.pop(self.selected_index)
        self.game.pop_state()

    def _release_selected(self):
        """
        Removes the selected fish without reward.
        """
        self.game.save_data.cooler.pop(self.selected_index)
        self.game.pop_state()

    # ---------- DRAW ----------

    def draw(self, screen):
        """
        Main draw dispatcher.
        Chooses between grid and detail rendering.
        """
        self._draw_background(screen)

        if self.mode in ("grid", "trade"):
            self._draw_grid(screen)
        else:
            self._draw_detail(screen)

    def _draw_background(self, screen):
        """
        Draws the dimmed background behind the cooler UI.
        """
        if self.background_cache:
            screen.blit(pygame.transform.scale(self.background_cache, screen.get_size()), (0, 0))
        else:
            screen.fill((20, 20, 30))

        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

    def _draw_grid(self, screen):
        panel = self.panel_rect

        pygame.draw.rect(screen, (18, 18, 24), panel, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2, border_radius=18)

        cap = self.game.save_data._cooler_capacity()
        count = len(self.game.save_data.cooler)

        # --- Slightly repositioned capacity text (less cramped) ---
        text = self.small_font.render(f"{count} / {cap}", True, (255,255,255))
        screen.blit(text, (panel.right - 120, panel.y + 10))

        self.grid_rects = []

        # Visible items on the page
        start = self.page * self.items_per_page
        end = start + self.items_per_page
        visible_items = self.game.save_data.cooler[start:end]

        for i, entry in enumerate(visible_items):
            x = panel.x + 24 + (i % 4) * (self.slot_size + self.slot_gap)
            y = panel.y + 80 + (i // 4) * (self.slot_size + 100)

            rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
            self.grid_rects.append(rect)

            pygame.draw.rect(screen, (45,45,60), rect, border_radius=12)

            real_index = start + i
            catchable, mutation = self._get_entry_data(real_index)

            image = catchable.image_for_mutation(mutation)
            if image:
                img = self.game.load_image(image)
                img_size = 220
                img_x = x + (self.slot_size - img_size) // 2
                img_y = y + (self.slot_size - img_size) // 2

                screen.blit(pygame.transform.scale(img, (img_size, img_size)), (img_x, img_y))
            name = self.small_font.render(catchable.name, True, (255,255,255))
            screen.blit(name, (x, y + self.slot_size + 10))

            if self.mode == "trade" and (start + i) in self.selected_indices:
                pygame.draw.rect(screen, (255,215,0), rect, 3)

        # ---------- TRADE UI (SPACING FIXED) ----------
        if self.mode == "trade":
            required = self.trade_request.get("required_fish", 0)
            selected = len(self.selected_indices)

            header_y = panel.y + 20

            # Main counter (larger + centered)
            main_text = self.body_font.render(
                f"{selected} / {required}",
                True,
                (255, 255, 255)
            )
            main_rect = main_text.get_rect(center=(panel.centerx, header_y + 10))
            screen.blit(main_text, main_rect)

            # Felix cumulative progress (smaller + below)
            if "total_required" in self.trade_request:
                total_required = self.trade_request["total_required"]
                given = self.game.save_data.felix_fish_given

                progress_text = self.small_font.render(
                    f"Total given: {given} / {total_required}",
                    True,
                    (200, 200, 200)
                )
                progress_rect = progress_text.get_rect(center=(panel.centerx, header_y + 40))
                screen.blit(progress_text, progress_rect)

            # Slightly lowered buttons for breathing room
            button_offset = 20

            color = (80,80,80) if selected < required else (40,40,60)

            confirm_rect = self.confirm_button_rect.move(0, button_offset)
            cancel_rect = self.cancel_button_rect.move(0, button_offset)

            self._draw_button(screen, confirm_rect, "Confirm", color)
            self._draw_button(screen, cancel_rect, "Cancel")

        # Page text
        page_text = self.small_font.render(
            f"{self.page + 1} / {max(1, (len(self.game.save_data.cooler)-1)//self.items_per_page + 1)}",
            True,
            (255,255,255)
        )
        screen.blit(page_text, (self.panel_rect.centerx - 20, self.panel_rect.bottom + 20))
        
        # Buttons
        self._draw_button(screen, self.prev_button, "<")
        self._draw_button(screen, self.next_button, ">")

    def _draw_detail(self, screen):
        """
        Draws the detailed view of a selected fish.
        """
        panel = pygame.Rect(120, 70, 1040, 580)

        pygame.draw.rect(screen, (18,18,24), panel, border_radius=18)
        pygame.draw.rect(screen, (255,255,255), panel, 2, border_radius=18)

        catchable, mutation = self._get_entry_data(self.selected_index)

        # --- DRAW FISH IMAGE ---
        image = catchable.image_for_mutation(mutation)

        if image:
            try:
                img = self.game.load_image(image)

                img_size = 400
                img_rect = pygame.Rect(
                    panel.centerx - img_size // 2,
                    panel.y + 80,
                    img_size,
                    img_size
                )

                scaled = pygame.transform.smoothscale(img, (img_size, img_size))
                pygame.draw.rect(screen, (240, 240, 240), img_rect, 2, border_radius=10)
                screen.blit(scaled, img_rect.topleft)

            except:
                pass

        title = self.title_font.render(catchable.name, True, (255,255,255))
        screen.blit(title, (panel.x + 24, panel.y + 20))

        self._draw_button(screen, self.eat_button_rect, "Eat")
        self._draw_button(screen, self.release_button_rect, "Release")
        self._draw_button(screen, self.return_button_rect, "Back")

    def _draw_button(self, screen, rect, label, fill_color=(40,40,60)):
        """
        Draws a standard UI button with text.
        """
        pygame.draw.rect(screen, fill_color, rect, border_radius=12)
        pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=12)

        text = self.button_font.render(label, True, (255,255,255))
        screen.blit(text, text.get_rect(center=rect.center))

