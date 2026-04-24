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

        # Grid layout settings
        self.grid_cols = 4
        self.slot_size = 120
        self.slot_gap = 18
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

        # Cached background image
        self.background_cache = None

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
        from states.dialogue_state import DialogueState
        """
        Handles trade confirmation for BOTH:
        - Standard trades (Bertha)
        - Cumulative trades (Felix)

        Behavior:
        - Removes selected fish
        - Applies either:
            • single purchase (flag)
            • cumulative progress (Felix)
            - Returns to appropriate dialogue node
            """
        
        trade = self.trade_request

        required = trade.get("required_fish", 0)
        total_required = trade.get("total_required", None)  # Felix-only

        selected_count = len(self.selected_indices)

        # --- NOTHING SELECTED ---
        if selected_count == 0:
            self.game.pop_state()
            return

        # --- STANDARD TRADE CHECK (Bertha) ---
        # Only enforce required_fish if NOT a cumulative trade
        if total_required is None and selected_count < required:
            self.game.pop_state()
            self.game.push_state(
                DialogueState(
                    self.game,
                    trade["conversation"],
                    trade["fail_node"]
                )
            )
            return

        # --- REMOVE SELECTED FISH ---
        for idx in sorted(self.selected_indices, reverse=True):
            self.game.save_data.cooler.pop(idx)

        # =========================================================
        # =============== FELIX CUMULATIVE LOGIC ==================
        # =========================================================
        if total_required is not None:
            # Initialize if not present
            if not hasattr(self.game.save_data, "felix_fish_given"):
                self.game.save_data.felix_fish_given = 0

            # Add to total
            self.game.save_data.felix_fish_given += selected_count

            # Check if enough TOTAL fish has been given
            if self.game.save_data.felix_fish_given >= total_required:
                next_node = trade["success_node"]
            else:
                next_node = trade["fail_node"]

            self.game.pop_state()

            self.game.push_state(
                DialogueState(
                    self.game,
                    trade["conversation"],
                    next_node
                )
            )
            return

        # =========================================================
        # =============== STANDARD TRADE LOGIC ====================
        # =========================================================

        # Grant purchase flag (Bertha-style)
        self.game.save_data.flags.add(trade["purchase_flag"])

        self.game.pop_state()

        self.game.push_state(
            DialogueState(
                self.game,
                trade["conversation"],
                trade["resume_node"]
            )
        )

    # ---------- INPUT HANDLING ----------

    def handle_event(self, event):
        """
        Handles all mouse input for:
        - grid navigation
        - trade selection
        - detail actions
        """
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        # TRADE MODE
        if self.mode == "trade":
            required = self.trade_request.get("required_fish", 0)

            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    # Toggle selection, but cap at required amount
                    if idx in self.selected_indices:
                        self.selected_indices.remove(idx)
                    else:
                        if len(self.selected_indices) < required:
                            self.selected_indices.add(idx)
                    return

            # Confirm trade
            if self.confirm_button_rect.collidepoint(event.pos):
                self._confirm_trade()
                return

            # Cancel trade
            if self.cancel_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return

        # NORMAL GRID MODE
        elif self.mode == "grid":
            if self.return_to_free_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return

            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = idx
                    self.mode = "detail"
                    return

        # DETAIL MODE
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
        panel = pygame.Rect(60, 80, 1160, 560)

        pygame.draw.rect(screen, (18, 18, 24), panel, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), panel, 2, border_radius=18)

        cap = self.game.save_data._cooler_capacity()
        count = len(self.game.save_data.cooler)

        # --- Slightly repositioned capacity text (less cramped) ---
        text = self.small_font.render(f"{count} / {cap}", True, (255,255,255))
        screen.blit(text, (panel.right - 120, panel.y + 10))

        self.grid_rects = []

        for i, entry in enumerate(self.game.save_data.cooler):
            x = panel.x + 24 + (i % 4) * (self.slot_size + self.slot_gap)
            y = panel.y + 80 + (i // 4) * (self.slot_size + 60)

            rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
            self.grid_rects.append(rect)

            pygame.draw.rect(screen, (45,45,60), rect, border_radius=12)

            catchable, mutation = self._get_entry_data(i)

            image = catchable.image_for_mutation(mutation)
            if image:
                img = self.game.load_image(image)
                screen.blit(pygame.transform.scale(img, (110,110)), (x+5,y+5))

            name = self.small_font.render(catchable.name, True, (255,255,255))
            screen.blit(name, (x, y+125))

            if self.mode == "trade" and i in self.selected_indices:
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

    def _draw_detail(self, screen):
        """
        Draws the detailed view of a selected fish.
        """
        panel = pygame.Rect(120, 70, 1040, 580)

        pygame.draw.rect(screen, (18,18,24), panel, border_radius=18)
        pygame.draw.rect(screen, (255,255,255), panel, 2, border_radius=18)

        catchable, mutation = self._get_entry_data(self.selected_index)

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

