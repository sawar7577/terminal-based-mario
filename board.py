import sys
import config


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.at = 0
        self.matrix = [[' ' for x in range(self.width)]
                       for y in range(self.height)]
        self.colormatrix = [
            [' ' for x in range(self.width)] for y in range(self.height)]

    def add(self, obj, posx, posy):
        for row in range(obj.height):
            for col in range(obj.width):
                if (row + posy) < self.height and (col + posx) < self.width:
                    try:
                        self.matrix[row + posy][col +
                                                posx] = obj.matrix[row][col]
                        self.colormatrix[row + posy][col + posx] = obj.color
                    except:
                        pass

    def remove(self, obj, posx, posy):
        for row in range(obj.height):
            for col in range(obj.width):
                if (row + posy) < self.height and (col + posx) < self.width:
                    try:
                        self.matrix[row + posy][col + posx] = ' '
                    except:
                        pass

    def show(self, width, height):
        sys.stdout.flush()
        for row in range(height):
            for col in range(width):
                if row == 0 or row == height - 1 or col == 0 or col == width - 1:
                    sys.stdout.write('*')
                elif row < self.height and col + self.at < self.width:
                    sys.stdout.write(
                        config.colors[self.colormatrix[row][col + self.at]] + self.matrix[row][col + self.at] + config.ENDC)
            sys.stdout.write('\n')

    def move(self, event, incrementer):
        if event == config.RIGHT:
            if self.at < self.width - config.show_width / 4:
                self.at += incrementer
        elif event == config.LEFT:
            if self.at > 0:
                self.at -= incrementer

    def clear(self, width):
        for row in range(self.height):
            for col in range(self.at, min(self.at + width, config.board_width)):
                self.matrix[row][col] = ' '
                self.colormatrix[row][col] = 'Black'
