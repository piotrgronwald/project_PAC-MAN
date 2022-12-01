
from pgzero.builtins import animate
from random import randint, shuffle
from map import get_possible_directions
from time import time
from constants import *

ghost_should_move = 4  # 4 - YES, 0 - NO


def ghost_should_move_up():
    global ghost_should_move
    ghost_should_move += 1


class Ghost:
    def __init__(self, level=1):
        self.ghosts = [Actor(f'ghost{i}', pos=(250+(i*20), 370), anchor=(14, 8)) for i in range(1, 5)]
        ghost_types = ['predator', 'normal', 'normal', 'prey']
        shuffle(ghost_types)
        for ghost in self.ghosts:
            ghost.dir = randint(0, 3)
            ghost.last_dir = -100
            ghost.in_center = True
            ghost.decide_point = 0, 8
            ghost.g_type = ghost_types.pop()
            ghost.start_pos = ghost.pos
            ghost.current_animation = None
        self.disable_ghost_image = 'ghost5'
        self.enable = True
        self.disable_time = 0
        self.ghost_moves = (18, 0), (0, -18), (-18, 0), (0, 18)
        self.ghost_speed = 3
        self.disable_max_time = max(3, 15 - (level-1)*0.5)

    def disable_ghost(self):
        self.enable = False
        self.disable_time = time()
        for ghost in self.ghosts:
            ghost.image = self.disable_ghost_image

    def enable_ghost(self):
        self.enable = True
        self.disable_time = 0
        for i, ghost in enumerate(self.ghosts):
            ghost.image = f'ghost{i+1}'

    def ghost_in_center(self):
        for ghost in self.ghosts:
            if 231 < ghost.x < 370 and 257+HUD < ghost.y < 337+HUD:
                ghost.in_center = True
            else:
                ghost.in_center = False

    def draw(self):
        for ghost in self.ghosts:
            ghost.draw()

    def update(self, pacman_pos):
        if not self.enable:
            left = self.disable_max_time - (time() - self.disable_time)
            if 0 < left < 2:
                if str(left)[:3][-1] in ['1', '3', '5', '7', '9']:
                    for i, ghost in enumerate(self.ghosts):
                        ghost.image = f'ghost{i+1}'
                else:
                    for ghost in self.ghosts:
                        ghost.image = self.disable_ghost_image
            elif left < 0:
                self.enable_ghost()
        self.ghost_in_center()
        self.move_ghost(pacman_pos)
        for ghost in self.ghosts:
            ghost.last_dir = ghost.dir

    @staticmethod
    def distance(ghost_pos, pacman_pos):
        return ((ghost_pos[0]-pacman_pos[0])**2 + (ghost_pos[1]-pacman_pos[1])**2)**0.5

    def move_ghost(self, pacman_pos):
        global ghost_should_move
        if ghost_should_move < 4:
            return
        ghost_should_move = 0
        for ghost in self.ghosts:
            directions = get_possible_directions(ghost)
            if ghost.in_center and directions[1]:
                ghost.dir = 1
            elif ghost.g_type == 'normal' or (ghost.g_type == 'predator' and randint(1, 50) % 5 == 0) or \
                    (ghost.g_type == 'prey' and randint(1, 50) % 4 == 0):
                ghost.dir = randint(0, 3)
                while directions[ghost.dir] == 0 or (abs(ghost.last_dir - ghost.dir) == 2 and directions.count(1) > 1):
                    ghost.dir = randint(0, 3)
            elif ghost.g_type == 'predator' or ghost.g_type == 'prey':
                best_direction = None
                for i, direction in enumerate(directions):
                    if not direction:
                        continue
                    if abs(ghost.last_dir - i) == 2 and directions.count(1) > 1:
                        continue
                    if best_direction is None:
                        best_direction = i
                    else:
                        current_best_pos_x = ghost.x + self.ghost_moves[best_direction][0]
                        current_best_pos_y = ghost.y + self.ghost_moves[best_direction][1]
                        current_best_pos = (current_best_pos_x, current_best_pos_y)
                        new_pos_x = ghost.x + self.ghost_moves[i][0]
                        new_pos_y = ghost.y + self.ghost_moves[i][1]
                        new_pos = (new_pos_x, new_pos_y)
                        current_distance = self.distance(current_best_pos, pacman_pos)
                        new_distance = self.distance(new_pos, pacman_pos)
                        if ghost.g_type == 'predator':
                            if new_distance < current_distance:
                                best_direction = i
                        if ghost.g_type == 'prey':
                            if new_distance > current_distance:
                                best_direction = i
                ghost.dir = best_direction
            ghost.current_animation = animate(ghost, pos=(ghost.x + self.ghost_moves[ghost.dir][0],
                                                          ghost.y + self.ghost_moves[ghost.dir][1]),
                                              duration=1/self.ghost_speed, tween='linear',
                                              on_finished=ghost_should_move_up)

    def check_collision(self, pacman):
        for ghost in self.ghosts:
            if ghost.colliderect(rect_for_pacman(pacman)):
                if self.enable:
                    return 'pacman_busted', 'None'
                else:
                    return 'ghost_busted', ghost
        return 'None', 'None'

