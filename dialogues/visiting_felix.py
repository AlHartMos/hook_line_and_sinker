from npc_interactions import Dialogue, felix, player

felix_visit = {

    # ---------- NO FISH ----------
    "no_fish": [
        Dialogue(
            player,
            "As you approached Felix’s shack, you realized you had no fish with you.",
            kind="thought"
        ),
        Dialogue(
            player,
            "It would be rude to visit him empty-handed.",
            kind="thought",
            next_node="end"
        )
    ],

    # ---------- HAS FISH ----------
    "intro": [
        Dialogue(
            felix,
            "Do you have some… fish?",
            kind="npc",
            next_node="options"
        )
    ],

    "options": [
        Dialogue(
            player,
            "Give fish",
            kind="choice",
            next_node="trade_felix"
        ),
        Dialogue(
            player,
            "Return to map",
            kind="choice",
            next_node="end"
        )
    ],

    # ---------- NOT ENOUGH TOTAL ----------
    "not_enough_total": [
        Dialogue(
            player,
            "Felix’s gloved hands reached out for the fish.",
            kind="thought"
        ),
        Dialogue(
            felix,
            "Can you give a bit more?",
            kind="npc",
            next_node="options"
        )
    ],

    # ---------- ENOUGH TOTAL ----------
    "enough_total": [
        Dialogue(player, "Felix’s hands reached for the fish.", kind="thought"),

        Dialogue(
            felix,
            "You… you brought me so much delicious… fish…",
            kind="npc"
        ),

        Dialogue(
            player,
            "For the first time, Felix sounded healthy.",
            kind="thought"
        ),

        Dialogue(
            felix,
            "I remember what I promised to you. Listen carefully now.",
            kind="npc"
        ),

        Dialogue(felix, "Outside this village, far from the rapids, there is a great treasure.", kind="npc"),
        Dialogue(felix, "Whoever finds it will live in ease for generations.", kind="npc"),

        Dialogue(felix, "Hans and Selim searched here already. It is not here.", kind="npc"),

        Dialogue(felix, "The rapids are safe. The last one leads back to civilization.", kind="npc"),

        Dialogue(felix, "You have two choices.", kind="npc"),
        Dialogue(felix, "Stay here… or go forward and find the treasure.", kind="npc"),

        Dialogue(
            player,
            "Now you knew what you had to do.",
            kind="thought"
        ),

        Dialogue(
            player,
            "You waved goodbye. The door shut behind him.",
            kind="thought",
            associated_flag=["felix_done", "felix_revealed_treasure"],
            next_node="end"
        )
    ],

    "end": []
}

felix_visit["_trade"] = {
    "trade_felix": {
        "required_fish": 1,          # must give at least 1 per visit
        "total_required": 10,        # total goal
        "purchase_flag": None,       # Felix doesn’t use item flags
        "fail_node": "not_enough_total",
        "success_node": "enough_total"
    }
}