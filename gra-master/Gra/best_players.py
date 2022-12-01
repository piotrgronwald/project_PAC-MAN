import sqlite3

from constants import *

conn = sqlite3.connect('Gra/db.sqlite3')
c = conn.cursor()
#c.execute("""CREATE TABLE IF NOT EXISTS GRA(id integer primary key autoincrement, gracz TEXT,wynik integer)""")
class BestPlayers:
    def __init__(self, screen):
        self.screen = screen
        self.best_players = []
        self.score = 0
        self.name = ''
        self.new_player_color = RED
        # with open('best.txt', 'r') as file:
        #     for line in file:
        #         if len(line) < 2:
        #             continue
        #         split_line = line.split()
        #         self.best_players.append((split_line[0], int(split_line[1])))

    def set_score(self, score): # ustawiamy punktacje
        self.score = score

    def exit(self):
        self.best_players.append((self.name, self.score))
        self.best_players.sort(key=lambda x: -x[1])
        if len(self.best_players) > 10:
            self.best_players.pop()
        lines = []
        for name, score in self.best_players: # zapisujemy do pliku
            d = conn.cursor()
            d.execute("insert into Game_gra('gracz','wynik') values('{}','{}')".format(name,score))
            conn.commit()
        #     lines.append(f'{name} {score}\n')
        # with open('best.txt', 'w') as file:
        #     file.writelines(lines)




    def change_color(self):
        if self.new_player_color == RED:
            self.new_player_color = GOLD
            return 'ok'
        else:
            self.exit()
        return 'exit'

    def append_to_name(self, key):
        if key.name == 'BACKSPACE' and self.name:
            self.name = self.name[:-1]
        elif key.name[:2] == 'K_':
            self.name += key.name[-1]
        elif len(key.name) == 1:
            self.name += key.name
        elif key.name == 'SPACE':
            self.name += ' '

    def draw(self):
        better_than = len(self.best_players)
        for i, line in enumerate(self.best_players):
            name, score = line
            if score < self.score:
                better_than = i
                break
            self.screen.draw.text(f'{name}', color=GOLD, fontsize=32, fontname='bungee-regular',
                                  topleft=(100, 100+40*i), owidth=1, ocolor=(100, 100, 100))
            self.screen.draw.text(f'{score}', color=GOLD, fontsize=32, fontname='bungee-regular',
                                  topleft=(400, 100 + 40 * i), owidth=1, ocolor=(100, 100, 100))
        if not self.name:
            self.screen.draw.text(f'_', color=self.new_player_color, fontsize=32,
                                  fontname='bungee-regular',
                                  topleft=(100, 100 + 40 * better_than), owidth=1, ocolor=(100, 100, 100))
        else:
            self.screen.draw.text(f'{self.name}', color=self.new_player_color, fontsize=32,
                                  fontname='bungee-regular',
                                  topleft=(100, 100 + 40 * better_than), owidth=1, ocolor=(100, 100, 100))
        self.screen.draw.text(f'{self.score}', color=self.new_player_color, fontsize=32, fontname='bungee-regular',
                              topleft=(400, 100 + 40 * better_than), owidth=1, ocolor=(100, 100, 100))

        for i, line in enumerate(self.best_players[better_than:]):
            name, score = line
            self.screen.draw.text(f'{name}', color=GOLD, fontsize=32, fontname='bungee-regular',
                                  topleft=(100, 100 + 40 * (i+better_than+1)), owidth=1, ocolor=(100, 100, 100))
            self.screen.draw.text(f'{score}', color=GOLD, fontsize=32, fontname='bungee-regular',
                                  topleft=(400, 100 + 40 * (i+better_than+1)), owidth=1, ocolor=(100, 100, 100))