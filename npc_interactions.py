# NPC data
class Npc:
    def __init__(self, name, image, hidden_name=None, reveal_flag=None):
        self.name = name
        self.hidden_name = hidden_name
        self.reveal_flag = reveal_flag
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
bertha = Npc("Bertha", "assets/bertha.png", hidden_name="???", reveal_flag="introduced_bertha")
selim = Npc("Selim", "assets/selim.png", hidden_name="???", reveal_flag="introduced_selim")
hans = Npc("Hans", "assets/hans.png", hidden_name="???", reveal_flag="introduced_hans")
felix = Npc("Felix", None, hidden_name="???", reveal_flag="introduced_felix")
unknown = Npc("Stranger", None)
player = Npc(None, None)

