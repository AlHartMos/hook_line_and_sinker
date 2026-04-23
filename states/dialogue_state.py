import pygame

from states.base_state import GameState
from states.cooler_state import CoolerState


class DialogueState(GameState):
    # This state handles any conversation in the game.
    # A conversation is a dictionary of nodes, and each node is a list of Dialogue objects.
    # A node can be:
    # - normal dialogue lines (npc / thought)
    # - or a choice node where every entry has kind="choice"
    def __init__(self, game, conversation, start_node="intro"):
        # Store the shared game reference so the state can access save data,
        # the state stack, and image loading.
        super().__init__(game)

        # The conversation dictionary passed in by the location or event.
        self.conversation = conversation

        # The node we are currently reading from.
        self.node = start_node

        # Which line inside the current node is active.
        self.line_index = 0

        # Cache portraits so we do not reload the same image every frame.
        self.portrait_cache = {}

        # Stores button rectangles for the current choice screen.
        self.choice_buttons = []

        # Fonts are created once and reused.
        self.title_font = None
        self.body_font = None
        self.choice_font = None
        self.small_font = None

    # This runs once when the dialogue becomes active.
    # It prepares the fonts used by the dialogue UI.
    def enter(self):
        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.body_font = pygame.font.SysFont(None, 30)
            self.choice_font = pygame.font.SysFont(None, 28)
            self.small_font = pygame.font.SysFont(None, 24)

    # Cleanup hook for consistency with the rest of the state system.
    def exit(self):
        return super().exit()

    # Returns the list of Dialogue entries for the active node.
    def current_entries(self):
        return self.conversation.get(self.node, [])

    # Returns the current Dialogue object inside the active node.
    def current_entry(self):
        entries = self.current_entries()
        if not entries:
            return None
        if self.line_index < 0 or self.line_index >= len(entries):
            return None
        return entries[self.line_index]

    # A node is a choice node if every entry in it is marked as kind="choice".
    # This lets you place choices in any node, not just a special "questions" node.
    def is_choice_node(self):
        entries = self.current_entries()
        return bool(entries) and all(getattr(entry, "kind", "npc") == "choice" for entry in entries)

    # Returns the list of available choice entries for the current node.
    # If the current node is not a choice node, this returns an empty list.
    def current_choices(self):
        if not self.is_choice_node():
            return []

        choices = self.current_entries()

        filtered = []
        for c in choices:
            # Hide treasure option unless flag is present
            if c.text == "Ask about the treasure":
                if "felix_revealed_treasure" not in self.game.save_data.flags:
                    continue
            if c.flag and c.flag in self.game.save_data.flags:
                continue  # hide already purchased item
            filtered.append(c)


        return filtered

    # Decides what name should be shown above the dialogue.
    def get_display_name(self, dialogue):
        if dialogue is None or dialogue.character is None:
            return None

        npc = dialogue.character

        if npc.hidden_name and npc.reveal_flag:
            if npc.reveal_flag not in self.game.save_data.flags:
                return npc.hidden_name

        return npc.name

    # Loads and caches portraits so they do not need to be reloaded constantly.
    def get_portrait(self, dialogue):
        if dialogue is None:
            return None

        image_path = getattr(dialogue, "image", None)
        if not image_path:
            return None

        if image_path not in self.portrait_cache:
            try:
                self.portrait_cache[image_path] = self.game.load_image(image_path)
            except Exception:
                self.portrait_cache[image_path] = None

        return self.portrait_cache[image_path]

    # Wraps text so it fits inside the dialogue box.
    def wrap_text(self, text, font, max_width):
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = word if not current_line else current_line + " " + word
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line)
                current_line = word

        if current_line:
            lines.append(current_line)

        return lines

    # Advances normal dialogue one line at a time.
    # If the current line has a next_node, it jumps there when the node finishes.
    def advance(self):
        entries = self.current_entries()
        if not entries:
            self.game.pop_state()
            return

        current = self.current_entry()
        if current is None:
            self.game.pop_state()
            return

        # If the current line has a flag, store it now.
        if current.flag:
            if isinstance(current.flag, list):
                # Add multiple flags
                for f in current.flag:
                    self.game.save_data.flags.add(f)
            else:
                # Add single flag
                self.game.save_data.flags.add(current.flag)

        next_node = getattr(current, "next_node", None)

        self.line_index += 1

        # Stay in the same node if there are more lines left.
        if self.line_index < len(entries):
            return

        # If this node points somewhere else, jump there.
        if next_node:
            self.node = next_node
            self.line_index = 0
            return

        # If there is no next node, the conversation is over.
        self.game.pop_state()

    # Handles the player clicking a choice button.
    def choose_choice(self, choice_index):
        choices = self.current_choices()
        if not choices:
            self.game.pop_state()
            return

        if choice_index < 0 or choice_index >= len(choices):
            return

        choice = choices[choice_index]

        if choice.flag:
            self.game.save_data.flags.add(choice.flag)

        # Check if this choice triggers a trade
        if "_trade" in self.conversation and choice.next_node in self.conversation["_trade"]:
            trade_request = self.conversation["_trade"][choice.next_node]

            # Attach conversation reference for return
            trade_request["conversation"] = self.conversation

            self.game.push_state(
                CoolerState(
                    self.game,
                    mode="trade",
                    trade_request=trade_request,
                )
            )
            return
        
        self.node = choice.next_node or "end"
        self.line_index = 0

        # If the chosen branch lands on an empty node, the conversation ends naturally.
        if not self.current_entries():
            self.game.pop_state()

    # Handles keyboard and mouse input.
    # Choice nodes use buttons, normal dialogue uses click / space / enter to advance.
    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.game.running = False
            return

        if self.is_choice_node():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for index, rect in enumerate(self.choice_buttons):
                    if rect.collidepoint(event.pos):
                        self.choose_choice(index)
                        return
            return

        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_RETURN):
                self.advance()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.advance()

    def update(self, dt):
        # Auto-redirect to "all_sold_out" if all shop items are purchased

        # Only run this if the conversation has trading data
        if "_trade" in self.conversation:

            # Get all purchase flags from trade config
            trade_flags = [
                trade["purchase_flag"]
                for trade in self.conversation["_trade"].values()
        ]

            # If ALL flags are present → everything is bought
            if all(flag in self.game.save_data.flags for flag in trade_flags):

                # Prevent infinite loop: only redirect if not already there
                if self.node != "all_sold_out":
                    self.node = "all_sold_out"
                    self.line_index = 0

    # Draws either normal dialogue or the current choice screen.
    def draw(self, screen):
        screen.fill((20, 24, 34))

        if self.is_choice_node():
            self.draw_choice_screen(screen)
        else:
            self.draw_dialogue_screen(screen)

        pygame.display.flip()

    # Draws NPC dialogue or player thoughts.
    def draw_dialogue_screen(self, screen):
        entry = self.current_entry()
        if entry is None:
            return

        screen_w, screen_h = screen.get_size()
        box = pygame.Rect(70, screen_h - 220, screen_w - 140, 160)

        pygame.draw.rect(screen, (15, 15, 20), box, border_radius=18)
        pygame.draw.rect(screen, (240, 240, 240), box, width=3, border_radius=18)

        portrait = self.get_portrait(entry)
        show_name = self.get_display_name(entry)

        text_x = box.x + 24
        text_top = box.y + 22

        if getattr(entry, "kind", "npc") == "npc" and portrait is not None:
            portrait_size = 120
            portrait_rect = pygame.Rect(box.x + 20, box.y - 140, portrait_size, portrait_size)

            scaled = pygame.transform.smoothscale(portrait, (portrait_size, portrait_size))
            pygame.draw.rect(screen, (245, 245, 245), portrait_rect, width=3, border_radius=10)
            screen.blit(scaled, portrait_rect.topleft)

            text_x = portrait_rect.right + 20
            text_top = box.y + 22

        if getattr(entry, "kind", "npc") == "npc" and show_name:
            name_surf = self.title_font.render(show_name, True, (255, 255, 255))
            screen.blit(name_surf, (text_x, text_top))
            text_top += 44

        elif getattr(entry, "kind", "npc") == "thought":
            tag = self.small_font.render("Inner thoughts", True, (180, 180, 180))
            screen.blit(tag, (text_x, text_top))
            text_top += 28

        lines = self.wrap_text(entry.text, self.body_font, box.width - (text_x - box.x) - 30)
        for i, line in enumerate(lines):
            surf = self.body_font.render(line, True, (230, 230, 230))
            screen.blit(surf, (text_x, text_top + i * 30))

        hint = self.small_font.render("Space / click to continue", True, (180, 180, 180))
        screen.blit(hint, (box.right - hint.get_width() - 18, box.bottom - 30))

    # Draws a choice screen for the current node.
    def draw_choice_screen(self, screen):
        screen_w, screen_h = screen.get_size()
        box = pygame.Rect(70, screen_h - 260, screen_w - 140, 200)

        pygame.draw.rect(screen, (15, 15, 20), box, border_radius=18)
        pygame.draw.rect(screen, (240, 240, 240), box, width=3, border_radius=18)

        prompt = self.title_font.render("Choose:", True, (255, 255, 255))
        screen.blit(prompt, (box.x + 24, box.y + 18))

        choices = self.current_choices()
        self.choice_buttons = []

        button_x = box.x + 24
        button_y = box.y + 70
        button_w = box.width - 48
        button_h = 38
        gap = 10

        mouse_pos = pygame.mouse.get_pos()

        for i, choice in enumerate(choices):
            rect = pygame.Rect(button_x, button_y + i * (button_h + gap), button_w, button_h)
            self.choice_buttons.append(rect)

            hovered = rect.collidepoint(mouse_pos)
            fill = (70, 70, 95) if hovered else (45, 45, 60)

            pygame.draw.rect(screen, fill, rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, width=2, border_radius=10)

            text = self.choice_font.render(choice.text, True, (255, 255, 255))
            screen.blit(text, (rect.x + 14, rect.y + 8))