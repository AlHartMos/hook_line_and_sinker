import pygame
from states.base_state import GameState
from states.dialogue_state import DialogueState
from dialogues.meeting_bertha import meeting_bertha
from dialogues.meeting_felix import meeting_felix
from dialogues.meeting_hans_lake import meeting_hans_lake
from dialogues.visting_bertha import bertha_post_shop
from dialogues.visiting_felix import felix_visit
from dialogues.trading_bertha import bertha_trading

class ValleyMenuState(GameState):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.SysFont(None, 32)

        self.options = []

    def enter(self):
        flags = self.game.save_data.flags

        self.options = []

        # --- Hans ---
        if "meeting_hans_complete" not in flags:
            self.options.append(("Go to shack", "meeting_hans"))

        # --- Bertha ---
        if "bertha_locked_out" not in flags:
            if "meeting_bertha_complete" not in flags:
                self.options.append(("Go to house", "meeting_bertha"))
            elif "trading_with_bertha_complete" not in flags:
                self.options.append(("Trade with Bertha", "bertha_trading"))
            else:
                self.options.append(("Visit Bertha", "bertha_post_shop"))

        # --- Felix ---
        if "met_felix" not in flags:
            self.options.append(("Explore the village", "meeting_felix"))
        elif "felix_done" not in flags:
            self.options.append(("Visit Felix", "felix_visit"))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i, rect in enumerate(self.rects):
                if rect.collidepoint(event.pos):
                    label, node = self.options[i]
                    self.game.pop_state()
                    conversation = self._get_conversation(node)

                    # Special case for Felix
                    if node == "felix_visit":
                        if len(self.game.save_data.cooler) == 0:
                            start_node = "no_fish"
                        else:
                            start_node = "intro"
                    else:
                        start_node = "intro"

                    self.game.push_state(
                        DialogueState(self.game, conversation, start_node)
                    )
                    return
            self.game.pop_state()
        

    def _get_conversation(self, key):
        # Map keys to actual dialogue dictionaries
        return {
            "meeting_hans": meeting_hans_lake,
            "meeting_bertha": meeting_bertha,
            "bertha_post_shop": bertha_post_shop,
            "meeting_felix": meeting_felix,
            "felix_visit": felix_visit,
            "bertha_trading": bertha_trading
        }[key]

    def draw(self, screen):
        from states.free_state import FreeState

        # Draw FreeState in background
        for state in self.game.state_stack:
            if isinstance(state, FreeState):
                state.draw(screen)
                break
            
        # Dark overlay (so UI stands out)
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        self.rects = []

        screen_w, screen_h = screen.get_size()

        button_width = 500
        button_height = 60
        spacing = 30

        total_height = len(self.options) * button_height + (len(self.options) - 1) * spacing
        start_y = (screen_h - total_height) // 2

        for i, (label, _) in enumerate(self.options):
            rect = pygame.Rect(
                (screen_w - button_width) // 2,
                start_y + i * (button_height + spacing),
                button_width,
                button_height
            )
            self.rects.append(rect)

            pygame.draw.rect(screen, (40, 40, 60), rect, border_radius=12)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=12)

            text = self.font.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))