from npc_interactions import Dialogue, player

tutorial_start = {
    "intro": [
        Dialogue(
                player,
                "Patient waves reach the sandy shores of the lake with small pebbles all across.",
                kind="thought"
            ),
        Dialogue(
                player,
                "The wide area of the lake was so large that one might believe to have come to the black sea.",
                kind="thought"
            ),
        Dialogue(
                player,
                "Sunny sky, barely filled with the clouds. Some broken branches reaching up near the wooden fence surrounding the water. Some simple trees afar. Lack of bushes, only one place with grass growing from far below.",
                kind="thought"
            ),
        Dialogue(
                player,
                "The best time and place for fishing, you believed.",
                kind="thought"
            ),
        Dialogue(
                player,
                "Only some patience and one will catch anything that they wished.",
                kind="thought"
            ),
        Dialogue(
                player,
                "Press the 'Fish' button to begin fishing",
                kind="thought",
                next_node="end"
            )
    ],

    "end": []
}