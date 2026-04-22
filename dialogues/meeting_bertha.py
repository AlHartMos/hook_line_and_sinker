from npc_interactions import Dialogue, bertha, player, unknown

meeting_bertha = {
    "intro": [
        Dialogue(
            player,
            "After reaching the house entrance door, the sound tells you that there must be a fireplace. Not too surprising in a place like this.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You decide to knock on the door and see what will happen.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Next few seconds pass in quiet of the wood chirping away, until you hear the creak of something being moved against the floor.",
            kind="thought"
        ),
        Dialogue(
            unknown,
            "Coming.",
            kind="npc"
        ),
        Dialogue(
            player,
            "The female voice came from behind the door. Not having too much of any accent.",
            kind="thought"
        ),
        Dialogue(
            player,
            "After a few more sounds of footsteps the door was opened.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Behind the entrance door stood a woman barely above 5 feet with a darker crimson red hood over her head. Short blond hair. Face of age with curvy nose, narrow barely pink lips, darker green eyes, oval ears and brows like two wings of falco. Yet an expression of a grandma famous for overfeeding her descendants.",
            kind="thought"
        ),
        Dialogue(
            player,
            "On her neck were many little skin tags that were darker than her pale skin. slightly below a darker blue bodice, with little to no pressure on the sides. Below, something that one will call a dark skirt.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Hello. You must have just arrived. Glad you managed to make it here.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Her voice was simple and on the lower pitch. Simple smile on the face.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "I won’t lie to you, but you look just like a wet cat after the rain. Please, come in.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Despite not being used to such kindness, you decided to follow inside the house due to truly being drenched from top to bottom.",
            kind="thought"
        ),
        Dialogue(
            player,
            "It was comfortable inside. Around were a few shelves made of red wood, some photos sealed inside a golden looking frame. A pack of cards above the fireplace, with still crackling away wood below. Two armchairs one next to the fireplace in which you were settled under the plaid in red and black pattern, another close to the little round table by the counters acting as a kitchen. In the corner neatly made up bed.",
            kind="thought"
        ),
        Dialogue(
            player,
            "The whole house which was simply a very large room",
            kind="thought"
        ),
        Dialogue(
            player,
            "Above the fire was a kettle. The woman started to move the second armchair closer to the one you are in, and after a few huffs she was in it next to you.",
            kind="thought"
        ),
        Dialogue(
            player,
            "She looked at you, and settled into her armchair as comfortably as possible for her.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Let’s start once again. I am Bertha. You are far from the only one that got here, although I have to admit, the visitors are rare and don’t stay here for too long.",
            kind="npc",
            associated_flag="bertha_introduces_herself"
        ),
        Dialogue(
            player,
            "She then rubbed her neck slightly, going with cut nails over skin tags.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "You know, it is very nice to see new faces from time to time. So don’t mind me if I may appear a bit weird.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Strangely enough, those were the words that relaxed you a bit more. The clothes on you seemed to slowly drain, without needing to spin it.",
            kind="thought"
        ),
        Dialogue(
            player,
            "As you began to look at Bertha, a few questions arose in your mind.",
            kind="thought",
            next_node="questions"
        )
    ],

    "questions": [
        Dialogue(
            player,
            "What is this place?",
            kind="choice",
            associated_flag="ask_bertha_where",
            next_node="bertha_where"
        ),
        Dialogue(
            player,
            "Is there any electricity in here?",
            kind="choice",
            associated_flag="ask_bertha_electricity",
            next_node="bertha_electricity"
        ),
        Dialogue(
            player,
            "Who else lives here?",
            kind="choice",
            associated_flag="ask_bertha_companions",
            next_node="bertha_companions"
        ),
        Dialogue(
            player,
            "Where does the flow lead?",
            kind="choice",
            associated_flag="ask_bertha_flow",
            next_node="bertha_flow"
        ),
        Dialogue(
            player,
            "...",
            kind="choice",
            associated_flag="ask_bertha_nothing",
            next_node="bertha_end"
        )
    ],

    "bertha_where": [
        Dialogue(
            bertha,
            "You are in Anchuria now. It was in the past a little town with quite a few people living here, but lately only passersby, who go through the flow of the river, get in here.",
            kind="npc"
        ),
        Dialogue(
            player,
            "You could swear that you were in the lake all this time, however, you don’t question her answer.",
            kind="thought",
        ),
        Dialogue(
            player,
            "Besides that you tried to remember whether you ever heard of the place, but to no avail.",
            kind="thought",
        ),
        Dialogue(
            bertha,
            "I have lived here ever since birth, and I have to tell you it is a beautiful place.",
            kind="npc"
        ),
        Dialogue(
            bertha,
            "Sure, the high mountains block off the sun most of the time, and yet the breath in here is simply incomparable, not that I have been to too many places to compare.",
            kind="npc"
        ),
        Dialogue(
            player,
            "She shrugged her nails along the line of her neck.",
            kind="thought",
        ),
        Dialogue(
            bertha,
            "I hope you love fish though. Except for some rare plants that can survive in this dark, there are no other options for the food.",
            kind="npc"
        ),
        Dialogue(
            player,
            "You sighed, carefully not to bring attention to it, yet the idea of eating only fish was hitting harder than one would wish.",
            kind="thought",
            next_node="questions"
        )
    ],

    "bertha_electricity": [
        Dialogue(
            player,
            "Bertha looked at you with childish interest, and confusion.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Not that I know of.",
            kind="npc",
        ),
        Dialogue(
            player,
            "By her sight it felt as if she heard the word electricity for the very first time. Although maybe no technology of the world has managed to reach this place.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Despite the head hurting you still thought of how long the electricity was used.",
            kind="thought"
        ),
        Dialogue(
            player,
            "200 years maybe? And she has no clue of it?",
            kind="thought"
        ),
        Dialogue(
            player,
            "You decided not to push on the question, after all being next to the fireplace was better than being thrown out due to an argument.",
            kind="thought",
            next_node="questions"
        )
    ],

    "bertha_companions": [
        Dialogue(
            bertha,
            "Only Felix and Hans. There was a man called Selim, but he went along the flow…",
            kind="npc"
        ),
        Dialogue(
            player,
            "She paused looking down with slight sorrow. You understood what going down the flow meant, and gave her a moment.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Felix is native, been here for at least 20 years. He is a nice fellow, only very shy. I haven’t seen much of him in weeks, always closing the door and saying not to bother. But if you get to talk to him, he could appear to be quite nice.",
            kind="npc"
        ),
        Dialogue(
            player,
            "She then changed her expression slightly to a more upset look.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "I can’t say that about Hans though. He lives in a shackle by the water. You will see his belly and aggressive temper before anything else.",
            kind="npc"
        ),
        Dialogue(
            bertha,
            "Better stay further from him. He is no good.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Bertha rose slightly to check the kettle and probably got a pause to not talk about Hans.",
            kind="thought"
        ),
        Dialogue(
            player,
            "When she settled back there were no more mentions of either Felix or Hans.",
            kind="thought",
            next_node="questions"
        ),
    ],

    "bertha_flow": [
        Dialogue(
            player,
            "At that question Bertha became more concentrated on your face, as if trying to read what you were asking it for.",
            kind="thought"
        ),
        Dialogue(
            player,
            "However, a few seconds later she responded simply.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Nowhere. Only a giant fall to your doom.",
            kind="npc"
        ),
        Dialogue(
            player,
            "She then showed with hand a boat going and then falling down with sounds that added to the feeling that she was showing it as if for the kid, after cackling.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Great. Now you were certainly stuck. Just as one would want to be a little dark scoop of land with only scenery being great black mountain peaks.",
            kind="thought",
            next_node="questions"
        ),
    ],

    # TO BE COMPLETED
    "bertha_end": [
        Dialogue(
            bertha,
            "That is fine. You do not have to ask everything at once.",
            kind="npc"
        )
    ]
}


def bertha_response(flags):
    # Returns the next branch based on which player choice was made.
    if "ask_bertha_where" in flags:
        return "bertha_where"
    if "ask_bertha_electricity" in flags:
        return "bertha_electricity"
    if "ask_bertha_companions" in flags:
        return "bertha_companions"
    if "ask_bertha_flow" in flags:
        return "bertha_flow"
    if "ask_bertha_nothing" in flags:
        return "bertha_end"
    return "questions"