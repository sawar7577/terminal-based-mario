# Terminal based Mario Game

### Instructions

* The game consists of three levels
* Each level is constructed in a way to ensure the difficulty increases with each level
* Enemies are killed (except for **Spikey**) when mario jumps over them
* Level ends when player reaches his Castle
* The BOSS enemy comes in the final level
* BOSS jumps randomly and fires bullets towards mario
* Each level has a time limit of 360 seconds
* Spring gives you a boost of 5 units

### Additional Features

* A level generator is provided to the user for designing custom levels
* Colored objects, enemies and players
* Smart enemies that follows you, jumps and shoot bullets


### Enemies

Following are the enemies in the game:
* **Goomba** : The dreaded Goomba changes it direction on collision with fixed objects and can jump anytime. Hit it on the head as soon as you see one before it causes you some serious trouble.
* **Spikey** : The Spikey (as the name suggests) has a body covered with spikes. Avoid it when you see it as you have no way to kill it. Fortunately it cannot jump over obstacles.
* **Stalker** :  The Stalker followes you wherever you go but it can jump over obstacles. You can kill it by jumping over it. Although pretty easy to kill, it can prove to be a deadly combination with Goomba.
* **Boss** : The Boss is the hardest enemy. It jumps randomly and shoots bullets randomly towards mario. Owing to its big body it can not move. It also dies when mario jumps over it.


### Powerup

Mario can increase his size and his jump height when by getting the powerup "GO BIG" from the special brick.



### Level Generator

* The player can choose to design his/her own levels when prompted in the beginning of the game
* The player is provided with a dummy marker to decide where to place certain objects in custom level
* The dummy marker has following controls:
    * Left - A
    * Right - D
    * Up - W
    * Down - S
    * Place object - X
* The objects provide to the player for designing levels are (in order):
    * Brick
    * Goomba
    * Spikey
    * Stalker
    * Spring
    * Coin
    * Special Brick
    * Castle


### Requirements
* Python 3

### Directory Structure

```
mario
    ├── board.py
    ├── collisionCheck.py
    ├── config.py
    ├── figures.py
    ├── game.py
    ├── levelGenerator.py
    ├── levels
    │   ├── level1
    │   ├── level2
    │   └── level3
    ├── objects.py
    ├── README.md
    └── requirements.txt

```



### Controls

* Left - A
* Right - D
* Jump - W

### Scoring 

* Collecting coins - 100 points
* Killing enemy - 50 points
* Hitting special bricks - 0 / 50 / 500 points (randomly decided)
* killing enemy bullets - 10 points

