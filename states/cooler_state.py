import pygame
from states.base_state import GameState
from states.dialogue_state import DialogueState

class CoolerState(GameState):
    def __init__(self, game, mode="grid", trade_request=None):
        super().__init__(game)

        # Modes:
        # "grid"   → normal cooler browsing
        # "detail" → inspect one fish
        # "trade"  → select fish for trading
        self.mode = mode

        # Trade data (only used in trade mode)
        self.trade_request = trade_request

        # Tracks selected fish indices during trading
        self.selected_indices = set()

        # Used for detail mode
        self.selected_index = None

        self.location = None
        self.background = None

        # Fonts
        self.title_font = None
        self.body_font = None
        self.small_font = None
        self.button_font = None

        # Grid layout
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

        # Back button
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

    def _load_background(self):
        if self.location and getattr(self.location, "image", None):
            try:
                return self.game.load_image(self.location.image)
            except:
                pass
        return None

    # ---------- DATA ----------

    def _get_entry_data(self, index):
        entry = self.game.save_data.cooler[index]

        if isinstance(entry, dict):
            return entry.get("catchable"), entry.get("mutation", 0)

        return entry, 0

    def _safe_stat_value(self, values, mutation):
        if not values:
            return 0
        return values[max(0, min(mutation, len(values) - 1))]

    # ---------- TRADE ----------

    def _confirm_trade(self):
        required = self.trade_request.get("required_fish", 0)

        if len(self.selected_indices) < required:
            # Not enough fish → go to failure dialogue
            self.game.pop_state()
            self.game.push_state(
                DialogueState(
                    self.game,
                    self.trade_request["conversation"],
                    self.trade_request["fail_node"]
                )
            )
            return

        # Remove selected fish
        for idx in sorted(self.selected_indices, reverse=True):
            self.game.save_data.cooler.pop(idx)

        # Set purchase flag
        self.game.save_data.flags.add(self.trade_request["purchase_flag"])

        # Return to dialogue
        self.game.pop_state()
        self.game.push_state(
            DialogueState(
                self.game,
                self.trade_request["conversation"],
                self.trade_request["resume_node"]
            )
        )

    # ---------- INPUT ----------

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if event.type != pygame.MOUSEBUTTONDOWN or event.button != 1:
            return

        # TRADE MODE
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

        # NORMAL GRID
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
        self.game.save_data.cooler.pop(self.selected_index)
        self.game.pop_state()

    # ---------- DRAW ----------

    def draw(self, screen):
        self._draw_background(screen)

        if self.mode in ("grid", "trade"):
            self._draw_grid(screen)
        else:
            self._draw_detail(screen)

    def _draw_background(self, screen):
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

        # Capacity display
        cap = self.game.save_data._cooler_capacity()
        count = len(self.game.save_data.cooler)

        text = self.small_font.render(f"{count} / {cap}", True, (255,255,255))
        screen.blit(text, (panel.right - 100, panel.y + 20))

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

        # Trade UI
        if self.mode == "trade":
            required = self.trade_request["required_fish"]
            selected = len(self.selected_indices)

            count_text = self.small_font.render(f"{selected} / {required}", True, (255,255,255))
            screen.blit(count_text, (panel.centerx - 30, panel.y + 20))

            self._draw_button(screen, self.confirm_button_rect, "Confirm")
            self._draw_button(screen, self.cancel_button_rect, "Cancel")

    def _draw_detail(self, screen):
        panel = pygame.Rect(120, 70, 1040, 580)

        pygame.draw.rect(screen, (18,18,24), panel, border_radius=18)
        pygame.draw.rect(screen, (255,255,255), panel, 2, border_radius=18)

        catchable, mutation = self._get_entry_data(self.selected_index)

        title = self.title_font.render(catchable.name, True, (255,255,255))
        screen.blit(title, (panel.x + 24, panel.y + 20))

        self._draw_button(screen, self.eat_button_rect, "Eat")
        self._draw_button(screen, self.release_button_rect, "Release")
        self._draw_button(screen, self.return_button_rect, "Back")

    def _draw_button(self, screen, rect, label):
        pygame.draw.rect(screen, (40,40,60), rect, border_radius=12)
        pygame.draw.rect(screen, (255,255,255), rect, 2, border_radius=12)

        text = self.button_font.render(label, True, (255,255,255))
        screen.blit(text, text.get_rect(center=rect.center))