from npc_interactions import Dialogue, bertha, player

bertha_post_shop = {

    # ---------- DEFAULT ENTRY ----------
    "intro": [
        Dialogue(
            bertha,
            "So you’ve come to meet me. It is lovely to see you. I’m afraid I don’t have anything to offer you but tea. Would you like to come in?",
            kind="npc",
            next_node="bertha_choices"
        )
    ],

    # ---------- MAIN OPTIONS ----------
    "bertha_choices": [
        # Treasure (conditional)
        Dialogue(
            player,
            "Ask about the treasure",
            kind="choice",
            next_node="treasure_confrontation"
        ),

        Dialogue(
            player,
            "Say you just stopped by to say hi",
            kind="choice",
            next_node="just_visiting"
        ),

        Dialogue(
            player,
            "Enter for tea",
            kind="choice",
            next_node="tea"
        ),

        Dialogue(
            player,
            "Return to map",
            kind="choice",
            next_node="end"
        ),
    ],

    # ---------- TREASURE PATH ----------
    "treasure_confrontation": [
        Dialogue(player, "Bertha’s face strained at once.", kind="thought"),
        Dialogue(player, "She must’ve known about it… yet hasn’t told anyone. Why?", kind="thought"),

        Dialogue(
            bertha,
            "Listen, I know it might not be the best here, but once you settle it is a great place.",
            kind="npc"
        ),

        Dialogue(player, "You don’t let her avoid the question.", kind="thought"),
        Dialogue(player, "Her reaction is uneasy. Afraid.", kind="thought"),

        Dialogue(
            bertha,
            "All these treasure adventures never work out well. Just stay, and I promise you will feel at home.",
            kind="npc"
        ),

        Dialogue(player, "You hate that she hid it from you.", kind="thought"),
        Dialogue(player, "Your only way out is through the rapids.", kind="thought"),
        Dialogue(player, "Now it makes sense why the others went.", kind="thought"),

        Dialogue(bertha, "It might be hard for you to understand but…", kind="npc"),

        Dialogue(player, "You don’t want to hear any more.", kind="thought"),
        Dialogue(player, "You close the door and leave.", kind="thought"),
        Dialogue(
            player,
            "You won’t return to Bertha again.",
            kind="thought",
            associated_flag="bertha_locked_out",
            next_node="end"
        )
    ],

    # ---------- SAY HI ----------
    "just_visiting": [
        Dialogue(
            bertha,
            "Oh, alright. Thank you for coming to visit.",
            kind="npc"
        ),
        Dialogue(
            player,
            "She gives a warm, if slightly sad smile and closes the door.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You return to your boat.",
            kind="thought",
            next_node="end"
        )
    ],

    # ---------- TEA ----------
    "tea": [
        Dialogue(player, "She gives a beaming smile and gestures for you to come inside.", kind="thought"),
        Dialogue(player, "You both settle by the fireplace, tea in hand.", kind="thought"),
        Dialogue(player, "You don’t speak, but you don’t need to.", kind="thought"),
        Dialogue(player, "It’s comfortable here.", kind="thought"),
        Dialogue(
            player,
            "Eventually, you return to your boat.",
            kind="thought",
            associated_flag="tea_with_bertha",
            next_node="end"
        )
    ],

    "end": []
}