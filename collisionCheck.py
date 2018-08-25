import board
import config
import objects
import os
import sys
import random
import time
import levelGenerator


def brickCollision(lst, plr, bd):
    """ This function checks the collision of player with bricks """
    plr.left = True
    plr.right = True
    plr.up = True
    plr.down = True
    lst = [i for i in lst if i.state != "dbrick"]
    for ob in lst:
        col_res = ob.collision(plr)
        if col_res[0] == False:
            plr.up = False
            if plr.jumping == True:
                ob.kill()
        if col_res[1] == False:
            plr.down = False
        if col_res[2] == False:
            plr.left = False
        if col_res[3] == False:
            plr.right = False


def specialbrickCollision(lst, plr, bd):
    """ This function checks the collision of player with special bricks """
    for ob in lst:
        col_res = ob.collision(plr)
        if col_res[0] == False:
            plr.up = False
            ob.hit(plr)
        if col_res[1] == False:
            plr.down = False
        if col_res[2] == False:
            plr.left = False
        if col_res[3] == False:
            plr.right = False


def enemyCollision(lst, remove_from, plr, bd):
    """ This function checks collision of mario and enemies"""
    for ob in lst:
        col_res = ob.collision(plr)
        if col_res[1] == False:
            if isinstance(ob, objects.Spikey) == True and isinstance(ob, objects.Stalker) == False:
                plr.hp -= 1
            else:
                plr.score += ob.points
                bd.remove(ob, ob.x, ob.y)
                remove_from.remove(ob)
                break
        elif col_res[0] == False or col_res[2] == False or col_res[3] == False:
            plr.hp -= 1


def springCollision(lst, plr, bd):
    """ This function checks the collision of player with springs """
    for ob in lst:
        col_res = ob.collision(plr)
        if col_res[1] == False:
            plr.y -= 5
            plr.up = True
            plr.down = False
            break
        if col_res[0] == False:
            plr.down = False
        if col_res[2] == False:
            plr.left = False
        if col_res[3] == False:
            plr.right = False


def coinCollision(lst, plr, bd):
    """ This function checks the collision of player with coins """
    for ob in lst:
        col_res = ob.collision(plr)
        if col_res[0] == False or col_res[1] == False or col_res[2] == False or col_res[3] == False:
            plr.score += ob.points
            bd.remove(ob, ob.x, ob.y)
            lst.remove(ob)
            break


def collisionChecker(check_list, check_for):
    """ This function checks the collision of an object(check_for) with a list  of objects(check_list) """
    for obj in check_list:
        col_res = obj.collision(check_for)
        if col_res[0] == False:
            check_for.up = False
        if col_res[1] == False:
            check_for.down = False
        if col_res[2] == False:
            check_for.left = False
        if col_res[3] == False:
            check_for.right = False


def updateEnemy(lst, bd, player_x, *args):
    """updates the position of enemies"""
    for i in lst:
        i.up = True
        i.down = True
        i.left = True
        i.right = True

        for arg in args:
            collisionChecker(arg, i)

        i.changedir(player_x)
    for i in lst:
        if i.x >= bd.at and i.x <= bd.at + config.show_width:
            i.move()


def bossFight(lst, bosl, bd, plr):
    """makes bullets by boss in boss fight"""
    for bos in bosl:
        try:
            if bos.shoot(plr):
                lst.append(levelGenerator.makeObject("bullet", bos.x, bos.y))
        except:
            pass
