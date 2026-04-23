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

        self.options = []

    def enter(self):
        flags = self.game.save_data.flags

        self.options = []

        # --- Hans ---
        if "meeting_hans_complete" not in flags:
            self.options.append(("Go to shack", "meeting_hans"))

        # --- Bertha ---
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
                    self.game.push_state(
                        DialogueState(self.game, self._get_conversation(node), "intro")
                    )
                    return

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
        screen.fill((20, 20, 30))

        self.rects = []

        for i, (label, _) in enumerate(self.options):
            rect = pygame.Rect(300, 200 + i * 80, 600, 50)
            self.rects.append(rect)

            pygame.draw.rect(screen, (40, 40, 60), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

            font = pygame.font.SysFont(None, 30)
            text = font.render(label, True, (255, 255, 255))
            screen.blit(text, text.get_rect(center=rect.center))