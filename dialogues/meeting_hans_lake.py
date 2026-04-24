from npc_interactions import Dialogue, hans, player

meeting_hans_lake = {
    "intro": [
        Dialogue(
            player,
            "As you began to approach the man moving around the shackle packing up stuff together, you came to notice his height. His head was close to reaching the lowest part of the roof. His forelock of messy chestnut hair slightly closer to reaching it.",
            kind="thought"
        ),
        Dialogue(
            player,
            "On top he wore a heavy coat that one would wear in noir detectives of the 50s.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Rest was still out of sight, except his extreme weight, with his belly sticking at least 15 centimetres in front of him.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Once you became close the man paid attention to you.",
            kind="thought"
        ),
        Dialogue(
            hans,
            "...",
            kind="npc"
        ),
        Dialogue(
            hans,
            "The fuck you want?",
            kind="npc"
        ),
        Dialogue(
            player,
            "You didn’t expect to hear that at first, however, now by hearing him you were sure he was Austrian, with a posh accent.",
            kind="thought"
        ),
        Dialogue(
            player,
            "He stared at you and puffed a bit as if tired, and returned to packing the stuff without paying attention to you.",
            kind="thought",
            next_node="questions"
        )
    ],

    "questions": [
        Dialogue(
            player,
            "What is your name?",
            kind="choice",
            associated_flag="ask_hans_name_lake",
            next_node="ask_name"
        ),
        Dialogue(
            player,
            "And what the fuck do you want?",
            kind="choice",
            associated_flag="ask_hans_what_lake",
            next_node="ask_what"
        ),
        Dialogue(
            player,
            "Do you know what this place is?",
            kind="choice",
            associated_flag="ask_hans_where_lake",
            next_node="ask_where"
        ),
        Dialogue(
            player,
            "...",
            kind="choice",
            associated_flag="ask_hans_nothing_lake",
            next_node="ask_nothing"
        )
    ],

    "ask_where": [
        Dialogue(
            hans,
            "No clue.",
            kind="npc",
            next_node="questions"
        )
    ],

    "ask_name": [
        Dialogue(
            hans,
            "Hans.",
            kind="npc",
            associated_flag="introduced_hans",
            next_node="questions"
        )
    ],

    "ask_what": [
        Dialogue(
            hans,
            "None of your fucking business.",
            kind="npc",
            next_node="questions"
        ),
        Dialogue(
            player,
            "He seemed pissed off. Although it was hard to tell whether he was pissed off at you or just like that.",
            kind="thought",
            next_node="questions"
        ),
    ],

    "ask_nothing": [
        Dialogue(
            player,
            "He was going around picking up different stuff and getting it together. Some of it for fishing. Some of it was pots and knives, and some just socks.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You got the point. He was a rocky mountain of stubbornness more annoying than that which was hovering over the whole village, and so you left him to do his business.",
            kind="thought",
            associated_flag="meeting_hans_complete",
            next_node="end"
        ),
        
    ],

    "end": []
}