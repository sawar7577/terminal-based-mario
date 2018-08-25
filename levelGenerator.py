import board
import config
import objects
import os
import sys
import random
import time


dir_path = "./levels/"

specialbrick = []
brick = []
enemy = []
spring = []
coin = []
cloud = []
goomba = []
spikey = []
stalker = []
boss = []
castle = []

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


def addobjects(bd, *args):
    for arg in args:
        for ob in arg:
            if ob.x > bd.at and ob.x < bd.at + config.show_width:
                bd.add(ob, ob.x, ob.y)


def removeobjects(bd, *args):
    for arg in args:
        for ob in arg:
            if ob.x > bd.at and ob.x < bd.at + config.show_width:
                bd.remove(ob, ob.x, ob.y)


def addCloud(lst, bd, level_name):

    completeName = os.path.join(dir_path + level_name, "cloud.txt")
    file = open(completeName, "w")
    choice = input('Do you want the scene to be cloudy?(y/n)	')
    if choice == 'y':
        for row in range(1, 4):
            for col in range(bd.width):
                if random.randint(0, 70) == 5:
                    temp = objects.Cloud(14, 4, col, row)
                    file.write(str(temp.x) + ',' + str(temp.y) + '\n')
                    lst.append(temp)


def addObjectList(bd, level_name, *names):

    for name in names:

        bd.at = 0

        completeName = os.path.join(dir_path + level_name, name + ".txt")
        file = open(completeName, "w")

        ob = makeObject(name)
        mk = objects.Marker(ob, ob.width, ob.height, 60, 30)

        bd.add(mk, mk.x, mk.y)
        while True:
            bd.clear(config.show_width)

            addobjects(bd, brick, enemy, goomba, spikey, stalker,
                       spring, coin, cloud, specialbrick, boss, castle)

            bd.add(mk, mk.x, mk.y)

            os.system('clear')
            bd.show(config.show_width, config.show_height)
            event = config.get_key(config.get_input())
            if event == config.QUIT:
                break
            elif event == config.SHOOT:
                bd.add(mk, mk.x, mk.y)
                file.write(str(mk.x) + ',' + str(mk.y) + '\n')
                lists[name].append(makeObject(name, mk.x, mk.y))
            else:
                mk.move(event)
                bd.move(event, mk.width)
                bd.add(mk, mk.x, mk.y)
        bd.remove(mk, mk.x, mk.y)
        bd.at = 0


def makeDirectory(name):
    if not os.path.exists(dir_path + name):
        os.makedirs(dir_path + name)


def makeLevel(name):
    if not os.path.exists(dir_path + name):
        os.makedirs(dir_path + name)

    bd = board.Board(config.board_width, config.show_height)
    addCloud(cloud, bd, name)
    addObjectList(bd, name, "brick", "goomba", "spikey", "stalker",
                  "spring", "coin", "specialbrick", "castle", "boss")


def giveList(filename):
    f = open(filename)
    lines = f.readlines()
    lines = [item.rstrip("\n") for item in lines]
    newList = list()
    for item in lines:
        item = item.split(",")
        item = tuple(int(items) for items in item)
        newList.append(item)
    f.close()
    return newList


def loadList(lt, level_name, name):
    l = giveList(os.path.join(dir_path + level_name, name + ".txt"))
    for tup in l:
        lt.append(makeObject(name, tup[0], tup[1]))


def makeObject(obj, x=config.show_width / 2, y=config.show_height / 2):
    if obj == "brick":
        return objects.Brick(7, 3, x, y)
    if obj == "coin":
        return objects.Coin(7, 3, x, y)
    if obj == "spring":
        return objects.Spring(7, 3, x, y)
    if obj == "specialbrick":
        return objects.SpecialBrick(14, 3, x, y)
    if obj == "goomba":
        return objects.Goomba(3, 2, x, y)
    if obj == "spikey":
        return objects.Spikey(4, 2, x, y)
    if obj == "stalker":
        return objects.Stalker(4, 2, x, y)
    if obj == "cloud":
        return objects.Cloud(14, 4, x, y)
    if obj == "castle":
        return objects.Castle(41, 15, x, y)
    if obj == "bullet":
        return objects.Bullet(4, 1, x, y)
    if obj == "boss":
        return objects.Boss(8, 4, x, y)
