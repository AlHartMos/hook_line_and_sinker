from npc_interactions import Dialogue, player

valley_start = {
    "intro": [
        Dialogue(
            player,
            "As the boat began to move, despite the silence there appeared a strong current pushing it forward. The sound was loud.",
            kind="thought"
        ),
        Dialogue(
            player,
            "The boat hit against the waves. Fog was inevitable.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You tried to go back, yet the force of water fought you, forcing you forward.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Constant hits of water. Waves. Noise. Shaking.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Suddenly, your head struck something.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Silence once more.",
            kind="thought"
        ),

        # --- WAKE UP ---
        Dialogue(
            player,
            "Once you wake up, the darkness is so deep it is hard to tell whether your eyes are open or still closed.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You are surrounded by tall mountains. Far away, the sound of flowing water echoes constantly.",
            kind="thought"
        ),
        Dialogue(
            player,
            "The waters are barely visible. The lack of light makes everything uncertain.",
            kind="thought"
        ),
        Dialogue(
            player,
            "The boat is intact. All of your caught fish are gone. Your head aches.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Some fish would be good to restore your strength. Not just your head needs attention now.",
            kind="thought",
            next_node="end"
        )
    ],

    "end": []
}

valley_intro_after_fish = {

    "intro": [
        Dialogue(
            player,
            "With your belly once again full, you begin to truly look around.",
            kind="thought"
        ),

        Dialogue(
            player,
            "Not far from you, there is a small isle near the base of the mountain.",
            kind="thought"
        ),

        Dialogue(
            player,
            "On it, you can make out a village.",
            kind="thought"
        ),

        Dialogue(
            player,
            "It lacks light, the only source coming from the narrow opening between the rocky mountain tops.",
            kind="thought"
        ),

        Dialogue(
            player,
            "The village seems empty…",
            kind="thought"
        ),

        Dialogue(
            player,
            "But two things stand out.",
            kind="thought"
        ),

        Dialogue(
            player,
            "A shack with light coming from inside…",
            kind="thought"
        ),

        Dialogue(
            player,
            "And someone moving inside another crooked structure.",
            kind="thought"
        ),

        Dialogue(
            player,
            "You have no idea what this place is doing here.",
            kind="thought"
        ),

        Dialogue(
            player,
            "But that is not your concern right now.",
            kind="thought"
        ),

        Dialogue(
            player,
            "What matters is that you are no longer stranded with nothing but a splitting headache.",
            kind="thought"
        ),

        # --- IMPORTANT FLAG UNLOCK ---
        Dialogue(
            player,
            "You can now explore the village.",
            kind="thought",
            associated_flag="valley_paths_unlocked",
            next_node="end"
        )
    ],

    "end": []
}