# NPC data
class Npc:
    def __init__(self, name, image):
        self.name = name
        self.hidden_name = "Stranger"
        self.image = image


# Class for dialogue
class Dialogue:
    def __init__(self, character, text, kind="npc", associated_flag=None, next_node=None):
        self.character = character
        self.speaker = character.name if character and character.name else None
        self.image = character.image if character else None
        self.text = text
        self.kind = kind  # "npc", "thought", or "choice"
        self.flag = associated_flag
        self.next_node = next_node


# Create NPCs
bertha = Npc("Bertha", "assets/bertha.png")
selim = Npc("Selim", "assets/selim.png")
hans = Npc("Hans", "assets/hans.png")
unknown = Npc("Stranger", None)
player = Npc(None, None)