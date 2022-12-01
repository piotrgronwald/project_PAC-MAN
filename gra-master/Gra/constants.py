from pgzero.builtins import Actor, Rect

HUD = 80
GOLD = 255, 215, 0
GRAY = 100, 100, 100
RED = 255, 0, 0
f_name = 'bungee-regular'


def rect_for_pacman(pacman):
    x, y, width, height = pacman.x, pacman.y, pacman.width, pacman.height
    rect = Rect(x - width / 2, y - height / 2, width, height)
    return rect


def text_draw(screen, text, color, size, position):
    screen.draw.text(text, color=color, fontsize=size, fontname='bungee-regular',
                     topleft=position, owidth=1, ocolor=GRAY)
