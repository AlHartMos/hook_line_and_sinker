from npc_interactions import Dialogue, felix, player

meeting_felix = {

    # ---------- INTRO ----------
    "intro": [
        Dialogue(player, "The village, despite its emptiness, felt very alive.", kind="thought"),
        Dialogue(player, "The shacks looked as if someone had left just yesterday… as if they would return soon.", kind="thought"),
        Dialogue(player, "Though that felt very unlikely.", kind="thought"),

        Dialogue(player, "The plants were scarce. Barely any grass. Mostly sticks and stones.", kind="thought"),

        Dialogue(player, "In the silent streets, you felt strangely relaxed.", kind="thought"),
        Dialogue(player, "As if this was what you had been missing.", kind="thought"),
        Dialogue(player, "A place where no one could hear you.", kind="thought"),

        Dialogue(player, "Then— a creak.", kind="thought"),
        Dialogue(player, "Not far away.", kind="thought"),

        Dialogue(player, "Then a few heavy coughs.", kind="thought"),
        Dialogue(player, "Wet. Strange. As if water filled the mouth.", kind="thought"),

        Dialogue(player, "You couldn’t ignore it.", kind="thought"),

        Dialogue(player, "It came from a shack near the mountains.", kind="thought"),
        Dialogue(player, "It looked unstable. Roof sagging low. Door crooked. Wood barely holding together.", kind="thought"),

        Dialogue(player, "You stepped carefully onto the threshold.", kind="thought"),
        Dialogue(player, "A board squealed.", kind="thought"),

        Dialogue(felix, "Who are you?!", kind="npc"),

        Dialogue(player, "The door opened slightly. A gloved hand gripping the frame.", kind="thought"),

        Dialogue(felix, "You’re not Hans!", kind="npc"),

        Dialogue(player, "You raised your hands slightly.", kind="thought"),

        Dialogue(felix, "You’re new?", kind="npc"),

        Dialogue(player, "You nodded.", kind="thought"),

        Dialogue(felix, "Huh… a… a… alright.", kind="npc"),

        Dialogue(felix, "I… I… I’m Felix…", associated_flag="introduced_felix", associated_flag="introduced_felix", kind="npc"),

        Dialogue(player, "You stepped closer.", kind="thought"),

        Dialogue(felix, "Don’t come!!!", kind="npc"),

        Dialogue(player, "You stopped immediately.", kind="thought"),
        Dialogue(player, "He didn’t sound well.", kind="thought"),

        Dialogue(felix, "L… Listen… Do you like fish?", kind="npc", next_node="fish_choice")
    ],

    # ---------- PLAYER CHOICE ----------
    "fish_choice": [
        Dialogue(player, "I like fish.", kind="choice", next_node="likes_fish"),
        Dialogue(player, "I don’t like fish.", kind="choice", next_node="dislikes_fish"),
    ],

    # ---------- LIKES FISH ----------
    "likes_fish": [
        Dialogue(felix, "Huh, I knew you were among the normals…", kind="npc"),
        Dialogue(player, "Felix laughed, the sound gurgling in his mouth.", kind="thought"),

        Dialogue(felix, "The fish is… it is… it’s the truth… always will be.", kind="npc"),
        Dialogue(felix, "And those who see it… they end up greatly gifted.", kind="npc"),

        Dialogue(player, "The gurgling continued.", kind="thought", next_node="after_choice")
    ],

    # ---------- DISLIKES FISH ----------
    "dislikes_fish": [
        Dialogue(felix, "How dare you!?", kind="npc"),

        Dialogue(player, "His voice deepened. Breathing uneven.", kind="thought"),

        Dialogue(felix, "Pathetic… Only pathetic beings don’t like fish…", kind="npc"),
        Dialogue(felix, "Pathetic… pathetic!", kind="npc"),

        Dialogue(player, "You heard thick gurgling. His mouth must be full of saliva.", kind="thought"),

        Dialogue(felix, "More for me… not you… pathetic…", kind="npc"),
        Dialogue(felix, "The truth will—", kind="npc"),

        Dialogue(player, "He coughed violently.", kind="thought", next_node="after_choice")
    ],

    # ---------- SHARED CONTINUATION ----------
    "after_choice": [
        Dialogue(felix, "I… I need fish…", kind="npc"),

        Dialogue(player, "Felix let out sharp, inhuman shrieks.", kind="thought"),

        Dialogue(felix, "I haven’t got enough… I need more…", kind="npc"),

        Dialogue(player, "The shrieking grew more alarming.", kind="thought"),

        Dialogue(felix, "I… I…", kind="npc"),

        Dialogue(player, "You heard something.", kind="thought"),
        Dialogue(player, "Was he… crying?", kind="thought"),

        Dialogue(felix, "I… I really need some… please… just some…", kind="npc"),

        Dialogue(player, "You realized how broken he was.", kind="thought"),
        Dialogue(player, "The illness must have left him starving.", kind="thought"),

        Dialogue(player, "You managed to calm him down.", kind="thought"),

        Dialogue(felix, "Please… return with some fish… and I… I’ll tell you something important.", kind="npc"),

        Dialogue(player, "You didn’t care about secrets.", kind="thought"),
        Dialogue(player, "You just wanted to help him.", kind="thought"),

        Dialogue(felix, "Thank you… thank you very much…", kind="npc"),

        Dialogue(
            player,
            "You are now able to visit Felix.",
            kind="thought",
            associated_flag="met_felix",
            next_node="end"
        )
    ],

    "end": []
}