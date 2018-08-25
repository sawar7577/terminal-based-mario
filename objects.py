import sys
import config
import time
import random
import figures

powerups = {
    'pts50': figures.pts50,
    'pts500': figures.pts500,
    'gobig': figures.gobig
}


class sprite:
    def __init__(self, width, height, posx, posy):
        self.width = width
        self.height = height
        self.matrix = [[' ' for x in range(self.width)]
                       for y in range(self.height)]
        self.x = posx
        self.y = posy
        self.right = True
        self.left = True
        self.up = True
        self.down = True
        self.color = 'White'
        self.back_color = 'Blue'

    def collision(self, obj):
        """gives the result of collision of self with given object the allowed dictionary specifies the movement allowed for given object"""
        up, down, left, right = range(4)
        allowed = {up: True, down: True, left: True, right: True}
        if self.x <= (obj.x + obj.width) and (self.x + self.width) >= obj.x and self.y <= (obj.y + obj.height) and (self.y + self.height) >= obj.y:
            if self.y == (obj.y + obj.height):
                allowed[down] = False
            if (self.y + self.height) == obj.y:
                allowed[up] = False
            if self.x == (obj.x + obj.width):
                if self.y == (obj.y + obj.height):
                    pass
                else:
                    allowed[right] = False
            if (self.x + self.width) == obj.x:
                if self.y == (obj.y + obj.height):
                    pass
                else:
                    allowed[left] = False

        return allowed


class Brick(sprite):
    def __init__(self, width, height, posx, posy):
        super(Brick, self).__init__(width, height, posx, posy)
        self.matrix = figures.brick
        self.state = "brick"
        self.color = 'Red'

    def kill(self):
        self.matrix = figures.dbrick
        self.state = "dbrick"


class SpecialBrick(Brick):
    def __init__(self, width, height, posx, posy):
        super(SpecialBrick, self).__init__(width, height, posx, posy)
        self.matrix = figures.specialbrick
        self.points = 0
        self.type = random.choice(['pts50', 'pts500', 'gobig'])
        self.used = False
        self.color = 'Light Red'
        self.back_color = 'Red'

    def hit(self, plr):
        if self.used == False:
            self.used = True
            self.matrix = powerups[self.type]
            if self.type == 'pts50':
                plr.score += 50
            elif self.type == 'pts500':
                plr.score += 500
            elif self.type == 'gobig':
                plr.togglesize('small')


class Marker(sprite):
    def __init__(self, ob, width, height, pox, posy):
        super(Marker, self).__init__(width, height, pox, posy)
        self.matrix = ob.matrix

    def move(self, event):
        if event == config.RIGHT:
            if self.x < config.board_width - 2 * self.width:
                self.x += self.width
        elif event == config.LEFT:
            if self.x > 2 * self.width:
                self.x -= self.width
        elif event == config.JUMP:
            self.y -= self.height
        elif event == config.DOWN:
            self.y += self.height


class Castle(sprite):
    def __init__(self, width, height, posx, posy):
        super(Castle, self).__init__(width, height, posx, posy)
        self.matrix = figures.castle


class Coin(sprite):
    def __init__(self, width, height, posx, posy):
        super(Coin, self).__init__(width, height, posx, posy)
        self.matrix = figures.coin
        self.points = 100
        self.color = 'Yellow'


class Cloud(sprite):
    def __init__(self, width, height, posx, posy):
        super(Cloud, self).__init__(width, height, posx, posy)
        self.matrix = figures.cloud
        self.color = 'White'


class Bullet(sprite):
    def __init__(self, width, height, posx, posy):
        super(Bullet, self).__init__(width, height, posx, posy)
        self.matrix = figures.bullet
        self.born = time.time
        self.points = 10

    def move(self):
        self.x -= 1

    def changedir(self, player_x):
        pass


class Spring(sprite):
    def __init__(self, width, height, posx, posy):
        super(Spring, self).__init__(width, height, posx, posy)
        self.matrix = figures.spring
        self.color = 'Cyan'


class MovingEntity(sprite):
    def __init__(self, width, height, posx, posy):
        super(MovingEntity, self).__init__(width, height, posx, posy)
        self.state = 0
        self.hp = 1
        self.jumping = False
        self.jump_timer = 0
        self.jumpState = 0
        self.score = 0
        self.jump_time = 10
        self.color = 'White'

    def jump(self):
        if self.jump_timer < self.jump_time and self.jumpState == 0 and self.up == True and self.jumping == True:
            self.jump_timer += 1
            self.y -= 1
        elif self.down == True:
            self.up = False
            self.jumpState = 1
            self.jump_timer -= 1
            self.y += 1
        else:
            self.jump_timer = 0
            self.jumping = False
            self.jumpState = 0


class Player(MovingEntity):
    def __init__(self, width, height, posx, posy):
        super(Player, self).__init__(width, height, posx, posy)
        self.matrix = figures.smallmario[0]
        self.mario = figures.smallmario
        self.hp = 5
        self.score = 0
        self.jump_time = 10
        self.size = 'small'
        self.color = 'White'

    def togglesize(self, arg):
        if arg == 'small':
            self.mario = figures.bigmario
            self.matrix = figures.bigmario[0]
            self.height = 3
            self.jump_time = 14
            self.size = 'big'
        if arg == 'big':
            self.mario = figures.smallmario
            self.matrix = figures.smallmario[0]
            self.height = 2
            self.jump_time = 10
            self.size = 'small'

    def move(self, event):
        if self.jumping == True or self.down == True:
            self.jump()

        if event == config.RIGHT and self.right == True:
            self.state += 1
            self.matrix = self.mario[self.state % 2]
            self.x += 1
            return "move"
        elif event == config.LEFT and self.left == True:
            if self.x > 15:
                self.state += 1
                self.matrix = self.mario[self.state % 2]
                self.x -= 1
            return "move"
        elif event == config.JUMP and self.jumping == False:
            self.jumping = True
        return "don't"


class enemy(MovingEntity):
    def __init__(self, width, height, posx, posy):
        super(enemy, self).__init__(width, height, posx, posy)
        self.direction = "left"
        self.points = 50
        self.color = 'Purple'
        self.jump_time = 7
        self.var = 0

    def enemyMove(self):
        self.var += 1
        if self.var % 2 == 0:
            if self.direction == "right" and self.right == True:
                self.x += 1
            elif self.left == True:
                self.x -= 1

    def changedir(self, player_x):
        if self.direction == "left" and self.left == False:
            self.direction = "right"
        elif self.direction == "right" and self.right == False:
            self.direction = "left"


class Goomba(enemy):
    def __init__(self, width, height, posx, posy):
        super(Goomba, self).__init__(width, height, posx, posy)
        self.matrix = figures.goomba
        self.var = 0

    def move(self):
        if random.randint(0, 10) == 5:
            self.jumping = True
        self.jump()
        self.enemyMove()


class Boss(Goomba):
    def __init__(self, width, height, posx, posy):
        super(Boss, self).__init__(width, height, posx, posy)
        self.matrix = figures.boss
        self.var = 0

    def shoot(self, plr):
        if plr.x - self.x < 50 or self.x - plr.x < 50:
            if random.randint(0, 10) == 5:
                return True
            else:
                return False
        else:
            return False

    def move(self):
        if random.randint(0, 10) == 5:
            self.jumping = True
        self.jump()


class Spikey(enemy):
    def __init__(self, width, height, posx, posy):
        super(Spikey, self).__init__(width, height, posx, posy)
        self.matrix = figures.spikey
        self.var = 0

    def move(self):
        self.jump()
        self.enemyMove()


class Stalker(Spikey):
    def __init__(self, width, height, posx, posy):
        super(Stalker, self).__init__(width, height, posx, posy)
        self.matrix = figures.stalker
        self.var = 0

    def changedir(self, player_x):
        if self.x < player_x:
            self.direction = "right"
        else:
            self.direction = "left"
