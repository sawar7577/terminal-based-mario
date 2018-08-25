import board
import config
import objects
import os
import sys
import random
import time
import levelGenerator
import collisionCheck

specialbrick = []
brick = []
enemy = []
spring = []
coin = []
cloud = []
boss = []
castle = []
goomba = []
spikey = []
stalker = []

lists = {
    "specialbrick": specialbrick,
    "brick": brick,
    "enemy": enemy,
    "spring": spring,
    "coin": coin,
    "cloud": cloud,
    "goomba": enemy,
    "spikey": enemy,
    "stalker": enemy,
    "boss": boss,
    "castle": castle
}


dir_path = "./levels/"


def loadLevel(level_name, *args):
    for arg in args:
        levelGenerator.loadList(lists[arg], level_name, arg)


def clearLists(*args):
    for arg in args:
        del arg[:]


def main():
    lives = 3
    reply = input('Do want to make your own level?(y/n)		')
    if reply == "y":
        level_name = input('What do you want to name your cutom level?		')
        levelGenerator.makeLevel(level_name)

    level_name = input('Please enter level name:	')

    while lives:
        tme = 360 + int(time.time())

        clearLists(specialbrick, brick, enemy,
                   spring, coin, cloud, castle, boss)

        bd = board.Board(config.board_width, config.board_width)
        try:
            loadLevel(level_name, "brick", "spring", "goomba", "stalker",
                      "spikey", "boss", "castle", "cloud", "coin", "specialbrick")
        except:
            print("No such level exists")
            exit()

        mario = objects.Player(2, 2, 54, 15)
        bd.at = 0

        while True:

            bd.clear(config.show_width)

            levelGenerator.addobjects(
                bd, brick, enemy, spring, coin, cloud, specialbrick, boss, castle)
            bd.add(mario, mario.x, mario.y)

            collisionCheck.bossFight(enemy, boss, bd, mario)

            collisionCheck.enemyCollision(enemy, enemy, mario, bd)
            collisionCheck.enemyCollision(boss, boss, mario, bd)

            collisionCheck.updateEnemy(boss, bd, mario.x, brick, spring)
            collisionCheck.updateEnemy(enemy, bd, mario.x, brick, spring)

            collisionCheck.brickCollision(brick, mario, bd)
            collisionCheck.specialbrickCollision(specialbrick, mario, bd)

            collisionCheck.springCollision(spring, mario, bd)
            collisionCheck.coinCollision(coin, mario, bd)

            if mario.hp <= 0 or mario.y > config.show_height or int(tme - time.time()) <= 0:
                lives -= 1
                break

            if mario.x >= castle[0].x:
                print("YOU WIN \t TOTAL SCORE:",
                      mario.score + int(tme - time.time()))
                lives = 0
                break

            os.system('tput reset')
            bd.show(config.show_width, config.show_height)
            print("LIVES:", lives, "\t", "HEALTH:", mario.hp, "\t", "SCORE:",
                  mario.score, "\t", "TIME LEFT:", int(tme - time.time()))

            event = config.get_key(config.get_input())

            if event == config.QUIT:
                lives = 0
                break

            if mario.move(event) == "move":
                bd.move(event, 1)

    print("GAME OVER")


if __name__ == "__main__":
    main()
