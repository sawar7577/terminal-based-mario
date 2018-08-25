'''

contains all the symbols, constants
directions, etc

'''

'''
    Allow certain inputs and translate to easier to read format
    UP : 0
    DOWN : 1
    LEFT : 2
    RIGHT : 3
    BOMB : 4
'''


board_height = 44
board_width = 1200

show_height = 44
show_width = 100


# key presses
JUMP, DOWN, LEFT, RIGHT, SHOOT, QUIT = range(6)
DIR = [JUMP, DOWN, LEFT, RIGHT]
INVALID = -1

# allowed inputs
_allowed_inputs = {
    JUMP: ['w'],
    DOWN: ['s'],
    LEFT: ['a'],
    RIGHT: ['d'],
    SHOOT: ['x'],
    QUIT: ['q']
}

colors = {
    'Black': '\x1b[0;30m',
    'Blue': '\x1b[0;34m',
    'Green': '\x1b[0;32m',
    'Cyan': '\x1b[0;36m',
    'Red': '\x1b[0;31m',
    'Purple': '\x1b[0;35m',
    'Brown': '\x1b[0;33m',
    'Gray': '\x1b[0;37m',
    'Dark Gray': '\x1b[1;30m',
    'Light Blue': '\x1b[1;34m',
    'Light Green': '\x1b[1;32m',
    'Light Cyan': '\x1b[1;36m',
    'Light Red': '\x1b[1;31m',
    'Light Purple': '\x1b[1;35m',
    'Yellow': '\x1b[1;33m',
    'White': '\x1b[1;37m'
}
ENDC = '\x1b[0m'


def get_key(key):
    for x in _allowed_inputs:
        if key in _allowed_inputs[x]:
            return x
    return INVALID

# Gets a single character from standard input.  Does not echo to the screen.


class _Getch:

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self):
        return self.impl()


class _GetchUnix:

    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


_getch = _Getch()


class AlarmException(Exception):
    pass


def alarmHandler(signum, frame):
    raise AlarmException


def get_input():
    import signal
    signal.signal(signal.SIGALRM, alarmHandler)
    signal.setitimer(signal.ITIMER_REAL, 0.3, 0.3)
    try:
        text = _getch()
        signal.setitimer(signal.ITIMER_REAL, 0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''
