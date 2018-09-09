# df-style-worldgen

![alt text](/Screenshots/1.png "Screenshots")

# What is it?

df-style-worldgen is a 2D fantasy world generator inspired by Dwarf Fortress. It generates 2D worlds with multiple map modes and eventually simulate civilizations, gods and beasts and their history.

# Installation

Windows:

- Download repository .zip and extract folder.
- Open pyWorld/dist
- Run pyWorld.exe (not pyWorld.py)

# Instructions

After opening pyWorld it generates a new map for you and displays the Biome Map Mode

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

## Note

This project was developed during the summer holidays of my first year of college. It began as just a prototype and a learning experience to learn more about python and more importantly about procedural generation. I kept working on it and adding new things as I found more and more interesting things to do with procedural generation. Unfortunately, due to my lack of knowledge and good code practices, typical in someone that's starting to learn programming, the code grew to become poorly organized and poorly planned making working on it harder and harder. Eventually I felt that working on it made me waste more time trying to refactor it and make things work than actually learning more about procedural generation. This led me to publish it and move on to other projects. I still consider this one of my favorite projects that I worked on as it was the one where I first learned and used procedural generation.
