from npc_interactions import Dialogue, bertha, player

trading_with_bertha = {
    "intro": [
        Dialogue(
            player,
            "Bertha met you with a kind smile.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Hello again, dear. Please, come in.",
            kind="npc",
            next_node="trading"
        ),
    ],

    "trading": [

    ],

    "end": [],
}