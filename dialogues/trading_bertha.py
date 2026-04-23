from npc_interactions import Dialogue, bertha, player

bertha_trading = {
    "intro": [
        Dialogue(
            player,
            "Bertha met you with a kind smile.",
            kind="thought"
        ),
        Dialogue(
            bertha,
            "Hello again, dear. Please, come in.",
            kind="npc",
            next_node="shop_menu"
        ),
    ],

    # ---------- MAIN SHOP MENU ----------
    "shop_menu": [
        # Lighter
        Dialogue(
            player,
            "Purchase a Lighter for 3 fish",
            kind="choice",
            next_node="trade_lighter",
            associated_flag="purchased_lighter"
        ),

        # Cooler
        Dialogue(
            player,
            "Purchase a Cooler for 3 fish",
            kind="choice",
            next_node="trade_cooler",
            associated_flag="purchased_extra_cooler"
        ),

        # Salt
        Dialogue(
            player,
            "Purchase Salt and Spice for 3 fish",
            kind="choice",
            next_node="trade_salt",
            associated_flag="purchased_salt"
        ),

        # Exit
        Dialogue(
            player,
            "Return to lake",
            kind="choice",
            next_node="end"
        ),
    ],

    # ---------- FAILURE ----------
    "not_enough": [
        Dialogue(
            bertha,
            "I’m sorry, but these items are worth a lot down here. I'd need you to bring me some more fish before I'm ready to part with it.",
            kind="npc",
            next_node="shop_menu"
        )
    ],

    # ---------- SUCCESS ----------
    "lighter_success": [
        Dialogue(
            bertha,
            "Thank you. I hope my old lighter will help you in this darkness.",
            kind="npc",
            associated_flag="purchased_lighter",
            next_node="shop_menu"
        )
    ],

    "cooler_success": [
        Dialogue(
            bertha,
            "Thank you. Here is my cooler. I believe it will be more helpful to you than for me.",
            kind="npc",
            associated_flag="purchased_extra_cooler",
            next_node="shop_menu"
        )
    ],

    "salt_success": [
        Dialogue(
            bertha,
            "So much fish… I wasn’t wrong about you. Here, take my spices, I know they make eating fish a bit more interesting.",
            kind="npc",
            associated_flag="purchased_salt",
            next_node="shop_menu"
        )
    ],

    # ---------- ALL ITEMS BOUGHT ----------
    "all_sold_out": [
        Dialogue(
            bertha,
            "Thank you for your services. You are truly amazing. I no longer have anything of value with me. If you wish, come and vist from time to time.",
            kind="npc",
            associated_flag="trading_with_bertha_complete",
            next_node="end"
        )
    ],

    "end": []
}

bertha_trading["_trade"] = {
    "trade_lighter": {
        "item_id": "lighter",
        "required_fish": 3,
        "purchase_flag": "purchased_lighter",
        "fail_node": "not_enough",
        "resume_node": "lighter_success"
    },

    "trade_cooler": {
        "item_id": "extra_cooler",
        "required_fish": 3,
        "purchase_flag": "purchased_extra_cooler",
        "fail_node": "not_enough",
        "resume_node": "cooler_success"
    },

    "trade_salt": {
        "item_id": "salt",
        "required_fish": 3,
        "purchase_flag": "purchased_salt",
        "fail_node": "not_enough",
        "resume_node": "salt_success"
    }
}