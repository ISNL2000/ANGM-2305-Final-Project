# Platformer Game

## Repository
https://github.com/ISNL2000/ANGM-2305-Final-Project.git

## Description
I will create a simple platformer game using pygame as a way to put to use everything that I've learned in this course.
It is relevant to digital arts (and to me) because it is a videogame, which is probably one of the best representations of what digital arts are.

## Features
- Movement
    - Movement includes, walking from side to side, dashing and jumping. It will be executed using the update function in pygame to update the player character's translation.
- Shooting
    - The player will be able to shoot projectiles to destroy enemies and obstacles. Implemented by instantiating a projectile object in the direction that the player is facing and giving it velocity.
- Enemies and Obstacles
    - Enemies that move around and hurt the player if they come into contact. Obstacles just stand in your way and must be destroyed to progress. Enemies will need some AI.
- Health System
    - Health system for the player. When all life is lost it will trigger a game over.
- Game State and Pause Menu
    - A pause feature that stops the game and allows the player to resume or quit. Also displays Win or Lose screens that allow the player to play again or quit.

## Challenges
- Learning how translations in pygame work and how to make them react to player input for both the player movement and projectile firing.
- AI for the enemies. This will likely be the hardest one to execute.
- How to pause the game, and not breaking the game while also allowing the user to restart it from the beginning or quit.

## Outcomes
Ideal Outcome:
- A simple, but enjoyable platformer game that controls well and looks appealing with it's minimalist graphics. Includes enemies with AI, a lose screeen, a win screen and a pause menu.

Minimal Viable Outcome:
- A platformer game with a somewhat interesting level that functions properly and has no gamebreaking glitches.

## Milestones

- Week 1
    1. Get the player movement and collision detection working.
    2. Display the player as a blue cube and create a simple, small level to test the mechanics.
    3. Allow the player to quit by clicking the close window button on the game window.

- Week 2
    1. Implement projectile shooting mechanic. 
    2. Begin implementing obstacles and enemy AI.
    3. Implement Win and Lose screens

- Week 3
    1. Finish Enemy AI.
    2. Create Pause screen that functions properly.
    3. Polish and build an interesting level.