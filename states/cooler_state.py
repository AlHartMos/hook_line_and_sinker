import pygame
from states.base_state import GameState
from states.dialogue_state import DialogueState


class CoolerState(GameState):
    def __init__(self, game, mode="grid", trade_request=None):
        super().__init__(game)

        # Modes:
        # "grid"   → normal cooler browsing
        # "detail" → single fish view
        # "trade"  → selecting fish for a trade
        self.mode = mode

        # Trade data passed in from DialogueState
        self.trade_request = trade_request

        # Track selected fish indices during trade
        self.selected_indices = set()

        self.selected_index = None

        self.location = None
        self.background = None

        self.title_font = None
        self.body_font = None
        self.small_font = None
        self.button_font = None

        self.grid_cols = 4
        self.slot_size = 120
        self.slot_gap = 18
        self.grid_rects = []

        # Detail buttons
        self.eat_button_rect = pygame.Rect(260, 600, 180, 54)
        self.release_button_rect = pygame.Rect(540, 600, 180, 54)
        self.return_button_rect = pygame.Rect(820, 600, 220, 54)

        # Trade buttons
        self.confirm_button_rect = pygame.Rect(500, 600, 180, 54)
        self.cancel_button_rect = pygame.Rect(720, 600, 180, 54)

        self.return_to_free_button_rect = pygame.Rect(980, 30, 220, 54)

        self.background_cache = None

    def enter(self):
        self.location = self.game.save_data.current_location
        self.background_cache = self._load_background()

        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.body_font = pygame.font.SysFont(None, 30)
            self.small_font = pygame.font.SysFont(None, 24)
            self.button_font = pygame.font.SysFont(None, 30)

    def exit(self):
        return super().exit()

    def _load_background(self):
        if self.location is None or not getattr(self.location, "image", None):
            return None

        try:
            return self.game.load_image(self.location.image)
        except Exception:
            return None

    # ---------- DATA HELPERS ----------

    def _get_entry_data(self, index):
        if index < 0 or index >= len(self.game.save_data.cooler):
            return None, 0

        entry = self.game.save_data.cooler[index]

        if isinstance(entry, dict):
            return entry.get("catchable"), entry.get("mutation", 0)

        return entry, 0

    def _safe_stat_value(self, values, mutation):
        if not values:
            return 0
        index = max(0, min(int(mutation), len(values) - 1))
        return values[index]

    # ---------- TRADE LOGIC ----------

    def _confirm_trade(self):
        required = self.trade_request["required_fish"]

        # Not enough fish → go to failure dialogue
        if len(self.selected_indices) < required:
            self.game.pop_state()
            self.game.push_state(
                DialogueState(
                    self.game,
                    conversation=self.trade_request["conversation"],
                    start_node=self.trade_request["fail_node"]
                )
            )
            return

        # Remove selected fish
        for idx in sorted(self.selected_indices, reverse=True):
            self.game.save_data.cooler.pop(idx)

        # Set purchase flag
        self.game.save_data.flags.add(self.trade_request["purchase_flag"])

        # Return to shop dialogue
        self.game.pop_state()
        self.game.push_state(
            DialogueState(
                self.game,
                conversation=self.trade_request["conversation"],
                start_node=self.trade_request["resume_node"]
            )
        )

    # ---------- INPUT ----------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        # TRADE MODE INPUT
        if self.mode == "trade":
            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    # Toggle selection
                    if idx in self.selected_indices:
                        self.selected_indices.remove(idx)
                    else:
                        self.selected_indices.add(idx)
                    return

            if self.confirm_button_rect.collidepoint(event.pos):
                self._confirm_trade()
                return

            if self.cancel_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return

        # NORMAL GRID INPUT
        elif self.mode == "grid":
            if self.return_to_free_button_rect.collidepoint(event.pos):
                self.game.pop_state()
                return

            for idx, rect in enumerate(self.grid_rects):
                if rect.collidepoint(event.pos):
                    self.selected_index = idx
                    self.mode = "detail"
                    return

        # DETAIL INPUT
        elif self.mode == "detail":
            if self.eat_button_rect.collidepoint(event.pos):
                self._eat_selected()
                return

            if self.release_button_rect.collidepoint(event.pos):
                self._release_selected()
                return

            if self.return_button_rect.collidepoint(event.pos):
                self.selected_index = None
                self.mode = "grid"
                return

    # ---------- UPDATE ----------

    def update(self, dt):
        return

    # ---------- DRAW ----------

    def draw(self, screen):
        self._draw_background(screen)

        if self.mode in ("grid", "trade"):
            self._draw_grid_screen(screen)
        else:
            self._draw_detail_screen(screen)

    def _draw_background(self, screen):
        w, h = screen.get_size()

        if self.background_cache:
            bg = pygame.transform.smoothscale(self.background_cache, (w, h))
            screen.blit(bg, (0, 0))
        else:
            screen.fill((20, 20, 30))

        overlay = pygame.Surface((w, h), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

    def _draw_grid_screen(self, screen):
        screen_w, screen_h = screen.get_size()

        panel = pygame.Rect(60, 80, screen_w - 120, screen_h - 160)

        pygame.draw.rect(screen, (18, 18, 24), panel, border_radius=18)
        pygame.draw.rect(screen, (255, 255, 255), panel, width=2, border_radius=18)

        # TRADE MODE HEADER
        if self.mode == "trade":
            required = self.trade_request["required_fish"]
            selected = len(self.selected_indices)

            text = self.small_font.render(f"{selected} / {required}", True, (255, 255, 255))
            screen.blit(text, (panel.centerx - 30, panel.y + 18))

        cooler = self.game.save_data.cooler

        self.grid_rects = []

        for i, entry in enumerate(cooler):
            col = i % self.grid_cols
            row = i // self.grid_cols

            x = panel.x + 24 + col * (self.slot_size + self.slot_gap)
            y = panel.y + 80 + row * (self.slot_size + 60)

            rect = pygame.Rect(x, y, self.slot_size, self.slot_size)
            self.grid_rects.append(rect)

            pygame.draw.rect(screen, (45, 45, 60), rect, border_radius=12)

            # Highlight selected fish in trade mode
            if self.mode == "trade" and i in self.selected_indices:
                pygame.draw.rect(screen, (255, 215, 0), rect, width=3)

        # Draw trade buttons
        if self.mode == "trade":
            self._draw_button(screen, self.confirm_button_rect, "Confirm")
            self._draw_button(screen, self.cancel_button_rect, "Cancel")

    def _draw_detail_screen(self, screen):
        # (unchanged from your version)
        pass

    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
        pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=12)

        surf = self.button_font.render(label, True, (255, 255, 255))
        screen.blit(surf, surf.get_rect(center=rect.center))