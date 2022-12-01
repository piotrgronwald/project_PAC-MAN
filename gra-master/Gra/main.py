

from pacman_behavior import Pacman
import pgzrun
from pgzero.builtins import Actor, keyboard, music, sounds
from pgzero.screen import Screen
from ghost import Ghost, ghost_should_move_up
from coins import Coin
import sys
from time import time
from best_players import BestPlayers
from typing import Optional
from constants import *

BLACK = 0, 0, 0
WIDTH = 600
HEIGHT = 600 + HUD
keys: keyboard
screen: Screen
POINTS = 0
LEVEL = 1

pacman = Pacman(keys)
ghost = Ghost()
coin = Coin()
bests: Optional[BestPlayers] = None

color_map = Actor("colorful_map", pos=(0, HUD), anchor=(0, 0))


def draw():
    global LEVEL
    screen.fill(BLACK)
    if not pacman.lives:
        bests.draw()
        return
    color_map.draw()
    pacman.draw(screen)
    ghost.draw()
    coin.draw_coins()
    #screen.draw.text(f'Poziom: {LEVEL}', color=GOLD, fontsize=32, fontname='bungee-regular',
    #                 topleft=(8, 4), owidth=1, ocolor=GRAY)
    screen.draw.text(f'{POINTS}', color=GOLD, fontsize=50, fontname='bungee-regular',
                     topright=(WIDTH-10, 10), owidth=1, ocolor=GRAY)
    screen.draw.text(f'GOLD', color=GOLD, fontsize=20, fontname='bungee-regular',
                     center=(WIDTH/2, 20), owidth=1, ocolor=GRAY)
    screen.draw.text(f'PACMAN', color=GOLD, fontsize=40, fontname='bungee-regular',
                     center=(WIDTH/2, 60), owidth=1, ocolor=GRAY)

    if not ghost.enable:
        time_left = time() - ghost.disable_time
        screen.draw.text(f'{ghost.disable_max_time-time_left:.2f}', color=(188, 19, 254),
                         fontsize=25, fontname='bungee-regular', center=(WIDTH/2+100, 50),
                         owidth=1, ocolor=GRAY)


def on_key_down(key):
    if not pacman.lives:
        bests.append_to_name(key)
        if key.name == 'RETURN':
            answer = bests.change_color()
            if answer == 'exit':
                sys.exit()
        return
    pacman.on_key_down(key)


def on_key_up(key):
    if not pacman.lives:
        return
    pacman.on_key_up(key)


def add_points(some_points):
    global POINTS
    POINTS += some_points
    if POINTS % 10000 == 0:
        pacman.lives += 1
        sounds.new_life.play()
        return 'sound'
    return None


def update_by_coin():
    global LEVEL, ghost, coin
    if pacman.move_pressed():
        coin_type = coin.check_collision(pacman.pacman)
        if coin_type == "coin":
            sound = add_points(10)
            if not sound:
                sounds.eating.play()
        if coin_type == "powerup":
            ghost.disable_ghost()
            sounds.powerup.play()
        if coin_type == "won":
            LEVEL += 1
            add_points(100)
            sounds.level_up.play()
            pacman.x, pacman.y = pacman.start_pos
            ghost = Ghost(level=LEVEL)
            coin = Coin()


def update_by_ghost():
    global POINTS
    if not pacman.lives:
        return
    coll_type, optional_ghost = ghost.check_collision(pacman.pacman)
    if coll_type == 'ghost_busted':
        sound = add_points(100)
        if not sound:
            sounds.eating.play()
        optional_ghost.pos = optional_ghost.start_pos
        optional_ghost.current_animation.stop()
        ghost_should_move_up()
    if coll_type == 'pacman_busted':
        for some_ghost in ghost.ghosts:
            some_ghost.pos = some_ghost.start_pos
            some_ghost.current_animation.stop()
            ghost_should_move_up()
        pacman.pacman.pos = pacman.start_pos
        pacman.lives -= 1
    if not pacman.lives:
        bests.set_score(POINTS)



def update():
    global bests
    if not bests:
        bests = BestPlayers(screen)
    pacman.update()
    ghost.update(pacman.pacman.pos)
    update_by_coin()
    update_by_ghost()


# music.play('music')
# music.set_volume(0.2)
pgzrun.go()



