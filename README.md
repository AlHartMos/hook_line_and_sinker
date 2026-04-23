# Hook, Line, and Sinker

A narrative-driven fishing game built with Python and Pygame.

# OVERVIEW

Hook, Line, and Sinker is a small game that combines:

fishing mechanics
dialogue-driven storytelling
exploration between locations
NPC interactions and trading systems

The player progresses through different areas, catches fish, interacts with characters, and unlocks new parts of the world through choices and actions.

# HOW TO RUN THE CODE

1. Download or clone the repository:
   git clone <your-repo-url>
   cd <repo-folder>

2. Create and activate a virtual environment (recommended)

Using Conda:
conda create -n mygame python=3.12
conda activate mygame

OR using venv:
python -m venv venv
source venv/bin/activate (Mac/Linux)
venv\Scripts\activate (Windows)

3. Install dependencies:
   pip install pygame numpy

OR (with conda):
conda install numpy
conda install -c conda-forge pygame

4. Run the game:
   python main.py

The game will open in a window and start automatically.

# PROJECT STRUCTURE

main.py

- Entry point of the game.

game.py

- Controls the main game loop and manages states.
- Stores player progress (SaveData).

locations.py

- Defines all locations and progression between them.

fishes.py

- Defines fish and trash objects, including stats and visuals.

npc_interactions.py

- Defines NPCs and the Dialogue class used throughout the game.

states/
Contains all gameplay systems:

    - base_state.py → base class for all states

- free_state.py → main exploration state
- fishing_state.py → fishing interaction
- dialogue_state.py → dialogue system
- cooler_state.py → inventory and trading
- popup_state.py → system popups
- button_overlay_state.py → overlay UI button
- valley_menu_state.py → village interaction menu

dialogues/
Contains all dialogue content:

- meeting_bertha.py
- trading_bertha.py
- visiting_bertha.py
- meeting_hans_lake.py
- meeting_felix.py
- visiting_felix.py

dialogues/location_starters/

- tutorial_starter.py
- lake_starter.py
- valley_starter.py

assets/

- Contains images (fish, backgrounds, NPCs)

# CORE SYSTEMS

State System
The game uses a stack-based state system. Different states handle different parts of the game:

- FreeState (exploration)
- FishingState (catching fish)
- DialogueState (conversations)
- CoolerState (inventory and trading)
- PopupState (messages)

Dialogue System

- Conversations are stored as dictionaries of nodes.
- Each node contains dialogue lines or choices.
- Supports branching paths and conditional options using flags.

Fishing System

- Players catch fish or trash depending on location.
- Fish have mutation levels and energy values.
- Fishing reduces player energy.

Inventory (Cooler)

- Stores caught fish.
- Has limited capacity (can be upgraded).
- Allows eating, releasing, and trading fish.

NPC Interactions

Bertha

- Introduces trading system.
- Items can be bought using fish.
- Dialogue choices can permanently remove her from interaction.

Felix

- Requires giving fish over multiple visits.
- Uses cumulative progress system.
- Unlocks important story information.

Hans

- One-time interaction.
- Provides background context.

Progression System

- Uses flags stored in SaveData.
- Flags unlock locations, dialogue, and new gameplay options.

# REQUIRED DEPENDENCIES

- Python 3.12
- pygame
- numpy

# NOTES

- The assets folder must remain intact for images to load correctly.
- The game currently does not include a save/load system.
- Progress resets when the game is restarted.
