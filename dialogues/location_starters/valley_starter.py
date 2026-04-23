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