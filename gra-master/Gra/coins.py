
from map import check_dot_point
from constants import *


class Coin:
    def __init__(self):
        self.coin_name = 'coin'
        self.power_name = 'power_up'
        self.coins = []
        for x in range(20, 580):
            for y in range(20, 580):
                where_check = x, y
                dot_type = check_dot_point(*where_check)
                where_put = x, y + HUD
                if dot_type == 0:
                    continue
                new_coin = None
                if dot_type == 1:
                    new_coin = Actor(self.coin_name, where_put, anchor=(13, 13))
                if dot_type == 2:
                    new_coin = Actor(self.power_name, where_put, anchor=(13, 13))
                new_coin.type = dot_type
                new_coin.hidden = False
                self.coins.append(new_coin)
        self.left_coins = len(self.coins)

    def draw_coins(self):
        for coin in self.coins_to_draw():
            coin.draw()

    def coins_to_draw(self):
        coins = []
        for coin in self.coins:
            if not coin.hidden:
                coins.append(coin)
        return coins

    def check_collision(self, pacman):
        for coin in self.coins_to_draw():
            if coin.colliderect(rect_for_pacman(pacman)):
                coin.hidden = True
                self.left_coins -= 1
                if self.left_coins == 0:
                    return "won"
                if coin.type == 1:
                    return "coin"
                else:
                    return "powerup"
        return "None"
