from npc_interactions import Dialogue, player

lake_start = {
    "intro": [
        Dialogue(
                player,
                "Tall trees, peaks of some lost in the white fog that came around as if from nowhere surrounding you with it.",
                kind="thought"
            ),
        Dialogue(
                player,
                "Ground too busy with all the trees and bushes to reach it. Close shot of the boat itself, fishing.",
                kind="thought"
            ),
        Dialogue(
                player,
                "The water is more dim, with the depth no longer seen below.",
                kind="thought"
            ),
        Dialogue(
                player,
                "The quiet infinitely spread through all of it, with no sounds of waves, birds, or even wind.",
                kind="thought"
            ),
        Dialogue(
                player,
                "Maybe in here you will find your luck.",
                kind="thought",
                next_node="end"
        )
    ],

    "end": []
}