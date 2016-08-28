# df-style-worldgen

![alt text](/Screenshots/1.png "Screenshots")

# What is it?

df-style-worldgen is a 2D world generator inspired by Dwarf Fortress. It generates 2D worlds with multiple map modes and will eventually simulate civilizations, gods and beasts and their history.

# What's different from Dwarf Fortress?

Dwarf Fortress is both a simulation and a game meaning that DF main goal is to generate a world and it's history but at some point allow the player to enter the world either as a Adventurer or leading a group of dwarfs without a predertermined goal except to have !!fun!!. However Dwarf Fortress generates the history of the world with incredible amount of detail in which every single entity(except creatures) has a name, a family, dreams, physical and psychological description and history record, meaning that history generation starts to slow down by the year 250. This project aims to mimic and if possible improve DF's world and history generator to have it run for longer and possibly create thousands of years of history by focusing on Adventurers, Beasts, Gods, etc and leaving the general population as a number.

# Installation

Windows:

- Download repository .zip and extract folder.
- Open pyWorld/dist
- Run pyWorld.exe (not pyWorld.py)

Note: These Distributions will be built every saturday, if you have python 2.7.11 installed you can run pyWorld\pyWorld.py (Not tested)

Linux (WIP):

Note: Linux version is currently broken in both 32/64 bit getting stuck after ReadGovernemnts probably missing library.

# Instructions

After opening pyWorld it generates a map for you and displays Biome Map Mode

Keys:

- r - Generate brand new world
- b - Display Biome Map Mode
- p - Display Precipitation Map Mode
- d - Display Drainage Map Mode
- w - Display Temperature Map Mode
- h - Display Altitude Map Mode
- t - Display Obsolete Terrain Map Mode
- f - Display Prosperity Map Mode

Simulation:

Currently only Civ expansion is generated. It's visible in the map by ▼ chars. More information is visible on the side console that displays Civ name, Civ race, Civ government form and each month display all sites and their population.

- SPACE to start/pause simulation

# Resources Used

df-style-worldgen is written in python and uses the libtcod API. df-style-worldgen uses Andux's modified version of the CP866 tileset.

# To do list

- Volcanism 
- Civilizations Expansion/Diplomacy
- Random Beasts/Gods/Adventurers
- Civ Independent Sites (ie: Beast Lair)
