from npc_interactions import Dialogue, bertha, player, unknown

meeting_bertha = {
    "intro": [
        Dialogue(
            player,
            "After reaching the house entrance door, the sound of a fireplace crackling. Not too surprising in a place like this.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You decide to knock on the door and see what will happen.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Next few seconds pass in quiet of a bird chirping in the distance, until you hear the creak of something being moved against the floor.",
            kind="thought"
        ),
        Dialogue(
            unknown,
            "Coming.",
            kind="npc"
        ),
        Dialogue(
            player,
            "A feminine voice came from behind the door. She didn't seem to have any discernable accent.",
            kind="thought"
        ),
        Dialogue(
            player,
            "After a few more sounds of footsteps the door was opened.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Behind the entrance door stood a woman barely above 5 feet with a dark crimson red hood over her head. Short blond hair. Wrinkled face with curvy nose, narrow barely pink lips, dark green eyes, oval ears and brows like two wings of falcon. She looked like a grandma famous for overfeeding her descendants.",
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
            bertha,
            "I don't mean to offend, dear, but you look just like a wet cat after the rain. Please, come in.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Despite not being used to such kindness, you decided to follow inside the house. You were truly being drenched from top to bottom.",
            kind="thought"
        ),
        Dialogue(
            player,
            "It was comfortable inside. Around were a few shelves made of red wood, some photos sealed inside a golden frames. A pack of cards above the fireplace, with still crackling away wood below. Two armchairs, one next to the fireplace in a plaid red and black pattern, another close to the little round table by the counters acting as a kitchen. In the corner, a neatly made bed.",
            kind="thought"
        ),
        Dialogue(
            player,
            "The whole house which was simply a very large room. You continue to observe as you settle into the armchair by the fireplace",
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
            "Oh, where are my manners? Allow me to intoduce myself. I am Bertha. You are far from my first vistor, although I have to admit, they typically don’t stay here for too long.",
            kind="npc",
            associated_flag="introduced_bertha"
        ),
        Dialogue(
            player,
            "She then rubbed her neck slightly, going with cut nails over skin tags.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "I apologize if my mannarisms are a bit odd, it's been a long time since my last visitor. You know, it is very nice to see a new face.",
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
            "Do you have any electricity here?",
            kind="choice",
            associated_flag="ask_bertha_electricity",
            next_node="bertha_electricity"
        ),
        Dialogue(
            player,
            "Does anyone else live here?",
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
            "You are in Anchuria now. In the past, it was a little town with quite a few people. Lately, there's only passersby, who go through the flow of the river.",
            kind="npc"
        ),
        Dialogue(
            player,
            "You could have sworn that you were still in the lake. However, you don’t question her answer.",
            kind="thought",
        ),
        Dialogue(
            player,
            "You tried to remember whether you ever heard of Anchuria before, but to no avail.",
            kind="thought",
        ),
        Dialogue(
            bertha,
            "I have lived here my whole life, and I have to tell you, it is a beautiful place.",
            kind="npc"
        ),
        Dialogue(
            bertha,
            "Sure, the mountains block off the sun most of the time, but the air in here is simply incomparable, not that I have been to many places to compare.",
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
            "You sighed, carefully not to bring attention to it, yet the idea of eating only fish was not very appealing.",
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
            "It seemed like she had just heard the word electricity for the first time. Maybe no modern technology has managed to reach this place?",
            kind="thought"
        ),
        Dialogue(
            player,
            "Still, it has been a long time since electricity was introduced into human society.",
            kind="thought"
        ),
        Dialogue(
            player,
            "200 years maybe? And she has never heard of it?",
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
            "Only Felix and Hans. There was another man, Selim, but... he went along the flow…",
            kind="npc",
            associated_flag=["introduced_hans", "introduced_felix", "introduced_selim"]
        ),
        Dialogue(
            player,
            "She paused looking down, brows furrowing togther. You gave her a moment to greive.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Felix is practically native, been here for at least 20 years. He is very shy. I haven’t seen much of him in weeks, always closing the door and saying not to bother. But if you get to talk to him, you'll find he's a kind fellow",
            kind="npc"
        ),
        Dialogue(
            player,
            "She then changed her expression slightly, radiating frustration and sadness.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "I can’t say that about Hans though. He lives in a shack by the water. You'll see his belly and aggressive temper before his shack though.",
            kind="npc"
        ),
        Dialogue(
            bertha,
            "Best to stay away from him. He is no good.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Bertha rose slightly out of her armchair to check the kettle, and probably to show she was done talking about Hans.",
            kind="thought"
        ),
        Dialogue(
            player,
            "When she settled back down, she didn't mention anyone else.",
            kind="thought",
            next_node="questions"
        ),
    ],

    "bertha_flow": [
        Dialogue(
            player,
            "At that question Bertha concentrated on your face, as if trying to read why you were asking.",
            kind="thought"
        ),
        Dialogue(
            player,
            "However, a few seconds later she responded.",
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
            "Great. Now you were certainly stuck here. In the dark valley. Just perfect.",
            kind="thought",
            next_node="questions"
        ),
    ],

    "bertha_end": [
        Dialogue(
            player,
            "About thirty minutes later you are feeling less like a wet puppy.",
            kind="thought"
        ),
        Dialogue(
            player,
            "The tea that Bertha made for you out of strange herbs that were growing around here reminded you of white tea, only with a slight aftertaste of raspberry.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Truly unexpected combination.",
            kind="thought"
        ),
        Dialogue(
            player,
            "Bertha wasn’t paying too much attention to you anymore, doing something with playing cards on the main table.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You appreciated her kindness a lot, and felt as if you were overstaying welcome. Of, course she would never admit that, yet you were gentleman enough to know it was time to leave.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You got out of an armchair carefully, smoothing down the plaid fabric.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You said your thanks to her and went to the exit door.",
            kind="thought"
        ),
        Dialogue(
            player,
            "She responded with the same kind smile as usual and once you opened the door let out.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Listen… Would you like to make some trades?",
            kind="npc"
        ),
        Dialogue(
            player,
            "You paused in one place and turned to look at her.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "I see you are a very nice person, much more, let’s say, accessible than others here, and I’m already a bit old for all the grappling through the water and catching the fish for food. So…",
            kind="npc"
        ),
        Dialogue(
            bertha,
            "If you would be so kind, when you have time, get me some fish, and I promise I’ll find something good for you too. Afterall, we have to get used to each other.",
            kind="npc"
        ),
        Dialogue(
            player,
            "Your head nodded to her request before you fully processed it.",
            kind="thought"
        ),
        Dialogue(
            player,
            "With that you got back outside, into the pitch black surroundings with soft light hitting from far above.",
            kind="thought"
        ),
        Dialogue(
            player,
            "You can visit her later, once you have some fish to trade.",
            kind="thought",
            associated_flag="meeting_bertha_complete",
            next_node="end"
        )
    ],

    "end": []
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