import pygame

from states.base_state import GameState


class DialogueState(GameState):
    # This class handles every conversation in the game.
    # It can show NPC dialogue, player thoughts, and player choice buttons
    # as long as the conversation data follows the same node-based format.
    def __init__(self, game, conversation, start_node="intro"):
        # We store the game reference through the parent class so this state
        # can access save data, the state stack, image loading, and other shared systems.
        super().__init__(game)

        # This is the conversation data passed in from outside.
        # It should be a dictionary of nodes, where each node maps to a list of Dialogue objects.
        self.conversation = conversation

        # This is the current node name in the conversation.
        # Example: "intro", "questions", or a branch name like "bertha_where".
        self.node = start_node

        # This is the index of the current line inside the active node.
        self.line_index = 0

        # These caches and UI lists help the state render portraits and buttons efficiently.
        self.portrait_cache = {}
        self.choice_buttons = []

        # Fonts are created once and reused so we do not recreate them every frame.
        self.title_font = None
        self.body_font = None
        self.choice_font = None
        self.small_font = None

    # This runs once when the dialogue state becomes active.
    # It is a good place to set up any UI resources that the state needs.
    def enter(self):
        if self.title_font is None:
            self.title_font = pygame.font.SysFont(None, 42)
            self.body_font = pygame.font.SysFont(None, 30)
            self.choice_font = pygame.font.SysFont(None, 28)
            self.small_font = pygame.font.SysFont(None, 24)

    # This runs when the dialogue state is being removed.
    # It exists mainly as a cleanup hook and keeps the state interface consistent.
    def exit(self):
        return super().exit()

    # This returns the list of Dialogue objects for the current node.
    # It keeps the rest of the code simple because we only have to ask for the active node in one place.
    def current_entries(self):
        return self.conversation.get(self.node, [])

    # This returns the current Dialogue object in the active node.
    # It is used by the drawing and advancing code so they always know what line is active.
    def current_entry(self):
        entries = self.current_entries()
        if not entries:
            return None
        if self.line_index < 0 or self.line_index >= len(entries):
            return None
        return entries[self.line_index]

    # This checks whether the current node is a choice node.
    # Choice nodes are displayed as buttons instead of advancing line by line.
    def is_choice_node(self):
        entries = self.current_entries()
        return bool(entries) and getattr(entries[0], "kind", "npc") == "choice"

    # This decides what name should be shown above the dialogue.
    # It lets you hide identities such as "Bertha" and show "???" until the reveal flag exists.
    def get_display_name(self, dialogue):
    # If no character, nothing to show
        if dialogue is None or dialogue.character is None:
            return None

        npc = dialogue.character

        # If NPC has a hidden name AND reveal flag not triggered → show hidden name
        if npc.hidden_name and dialogue.flag:
            if dialogue.flag not in self.game.save_data.flags:
                return npc.hidden_name

        # Otherwise show real name
        return npc.name

    # This filters out questions that have already been asked.
    # Any choice whose flag is already in save data will no longer appear.
    def get_available_choices(self):
        choices = self.conversation.get("questions", [])
        available = []

        for choice in choices:
            if choice.flag is None:
                available.append(choice)
            elif choice.flag not in self.game.save_data.flags:
                available.append(choice)

        return available

    # This loads and caches portrait images so they do not need to be reloaded every frame.
    # It also safely handles missing images by returning None.
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

    # This wraps long text into multiple lines so it fits inside the dialogue box.
    # It prevents long dialogue from running off the edge of the UI.
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

    # This advances the conversation when the player clicks or presses a key.
    # It also stores any flag attached to the current dialogue line before moving on.
    def advance(self):
        entries = self.current_entries()
        if not entries:
            self.game.pop_state()
            return

        current = self.current_entry()
        if current is None:
            self.game.pop_state()
            return

        # If this line has a flag, remember that it happened.
        if current.flag:
            self.game.save_data.flags.add(current.flag)

        next_node = getattr(current, "next_node", None)

        self.line_index += 1

        # If there are more lines in the current node, stay here.
        if self.line_index < len(entries):
            return

        # If the node has a next_node, jump there after the final line.
        if next_node:
            self.node = next_node
            self.line_index = 0

            # If we land back on questions, and there are no choices left, end the conversation.
            if self.node == "questions" and not self.get_available_choices():
                self.node = "end"
                self.line_index = 0

            return

        # If there is no next node, end the conversation.
        self.game.pop_state()

    # This handles the player selecting one of the visible choice buttons.
    # It stores the choice's flag, then jumps to the branch assigned to that choice.
    def choose_choice(self, choice_index):
        choices = self.get_available_choices()
        if not choices:
            self.node = "end"
            self.line_index = 0
            return

        if choice_index < 0 or choice_index >= len(choices):
            return

        choice = choices[choice_index]

        if choice.flag:
            self.game.save_data.flags.add(choice.flag)

        self.node = choice.next_node or "questions"
        self.line_index = 0

        # If the branch returns to questions and nothing is left to ask, end the conversation.
        if self.node == "questions" and not self.get_available_choices():
            self.node = "end"
            self.line_index = 0

    # This receives keyboard and mouse input while the conversation is active.
    # It routes clicks to choices or advances normal dialogue with space, enter, or click.
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

    # This is where per-frame logic would go if the dialogue ever needed timers or animations.
    # For now it exists so the state still follows the same update pattern as the rest of the game.
    def update(self, dt):
        return

    # This draws the active conversation frame.
    # It chooses between normal dialogue rendering and the question-button screen.
    def draw(self, screen):
        screen.fill((20, 24, 34))

        if self.is_choice_node():
            self.draw_choice_screen(screen)
        else:
            self.draw_dialogue_screen(screen)

        pygame.display.flip()

    # This draws NPC dialogue or player thoughts.
    # It shows portraits for NPC lines and leaves thoughts text-only.
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

    # This draws the player-choice screen.
    # It shows every unanswered question as a button and lets the player pick one.
    def draw_choice_screen(self, screen):
        screen_w, screen_h = screen.get_size()
        box = pygame.Rect(70, screen_h - 260, screen_w - 140, 200)

        pygame.draw.rect(screen, (15, 15, 20), box, border_radius=18)
        pygame.draw.rect(screen, (240, 240, 240), box, width=3, border_radius=18)

        prompt = self.title_font.render("Choose a question:", True, (255, 255, 255))
        screen.blit(prompt, (box.x + 24, box.y + 18))

        choices = self.get_available_choices()
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