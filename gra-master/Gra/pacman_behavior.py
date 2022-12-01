
from pgzero.builtins import Actor
from time import time
from map import check_move_point


class Pacman:
    def __init__(self, keys, lives=1):
        self.images = ["pacman_o", "pacman_or", "pacman_c", "pacman_cr", ]
        self.keys = keys
        self.pacman = Actor("pacman_o")
        self.pacman.keys_active = {'right': False, 'up': False, 'left': False, 'down': False}
        self.pacman.x = 290
        self.pacman.y = 580
        self.start_pos = self.pacman.x, self.pacman.y
        self.lives = lives
        self.teeth_time = 0.1
        self.teeth = False
        self.dt = None

    def on_key_down(self, key):
        if key == self.keys.RIGHT:
            self.pacman.keys_active['right'] = True
        if key == self.keys.UP:
            self.pacman.keys_active['up'] = True
        if key == self.keys.LEFT:
            self.pacman.keys_active['left'] = True
        if key == self.keys.DOWN:
            self.pacman.keys_active['down'] = True

    def on_key_up(self, key):
        if key == self.keys.RIGHT:
            self.pacman.keys_active['right'] = False
        if key == self.keys.UP:
            self.pacman.keys_active['up'] = False
        if key == self.keys.LEFT:
            self.pacman.keys_active['left'] = False
        if key == self.keys.DOWN:
            self.pacman.keys_active['down'] = False

    def draw(self, screen):
        self.pacman.draw()
        for live in range(self.lives):
            screen.blit("pacman_o", (10 + live * 40, 40))

    def move_pressed(self):
        pressed = any(value for value in self.pacman.keys_active.values())
        if not pressed:
            self.teeth = False
            self.dt = None
        return pressed

    def update(self):
        move_pressed = self.move_pressed()
        if not move_pressed:
            return

        can_move = check_move_point(self.pacman)
        if not can_move:
            return

        if move_pressed and self.dt is None:
            self.teeth = True
            self.dt = time()
        if self.dt is not None:
            now = time()
            if now - self.dt > self.teeth_time:
                self.teeth = not self.teeth
                self.dt = now

        straight_pacman_image = "pacman_c" if self.teeth else "pacman_o"
        flipped_pacman_image = "pacman_cr" if self.teeth else "pacman_or"

        if self.pacman.keys_active['right']:
            self.pacman.x += 1
            self.pacman.image = straight_pacman_image
            self.pacman.angle = 0
        if self.pacman.keys_active['up']:
            self.pacman.y -= 1
            self.pacman.image = straight_pacman_image
            self.pacman.angle = 90
        if self.pacman.keys_active['left']:
            self.pacman.x -= 1
            self.pacman.image = flipped_pacman_image
            self.pacman.angle = 180
        if self.pacman.keys_active['down']:
            self.pacman.y += 1
            self.pacman.image = flipped_pacman_image
            self.pacman.angle = 270
