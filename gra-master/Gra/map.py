
from pygame import image, Color
from constants import *

moveimage = image.load('Gra/images/move_map.png')
dotimage = image.load('Gra/images/dot_map.png')


def check_move_point(pacman):
    move_x, move_y = 0, 0
    if pacman.keys_active['right']:
        move_x = 1
    if pacman.keys_active['up']:
        move_y = -1
    if pacman.keys_active['left']:
        move_x = -1
    if pacman.keys_active['down']:
        move_y = 1

    if pacman.x+move_x < 0:
        pacman.x = 576
        return True
    if pacman.x+move_x+pacman.width/2 > 600:
        pacman.x = 0
        return True

    if moveimage.get_at((int(pacman.x+move_x), int(pacman.y+move_y-HUD))) != Color('black'):
        return False
    return True


def get_possible_directions(ghost):
    bw = 18  # black_width
    if ghost.in_center:
        bw = 20
    directions = [0, 0, 0, 0]  # right, up, left, down
    if ghost.x - bw < 0:
        ghost.x = 576
    elif ghost.x + bw > 600:
        ghost.x = bw

    move_x, move_y = ghost.decide_point
    dpx = ghost.x + move_x
    dpy = ghost.y + move_y

    try:
        if moveimage.get_at((int(dpx+bw), int(dpy - HUD))) == Color('black'):
            directions[0] = 1
    except IndexError:
        directions[0] = 1
    if moveimage.get_at((int(dpx), int(dpy - HUD - bw))) == Color('black'):
        directions[1] = 1
    try:
        if moveimage.get_at((int(dpx-bw), int(dpy - HUD))) == Color('black'):
            directions[2] = 1
    except IndexError:
        directions[2] = 1
    if moveimage.get_at((int(dpx), int(dpy - HUD + bw))) == Color('black'):
        directions[3] = 1
    return directions


def check_dot_point(x, y):
    point = int(x), int(y)
    if dotimage.get_at(point) == Color('blue'):
        return 1
    if dotimage.get_at(point) == Color('green'):
        return 2
    return 0
