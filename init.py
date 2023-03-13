from base_classes import *
from colorama import Fore, Style
from player import Player
from rat import Rat

import game
import random
import time


def top_bar():

    """
    ╔═════════════════════════════════════════════════════════════════════════════╗
    ║ WEAPON: SHOTGUN                                                             ║
    ╚═════════════════════════════════════════════════════════════════════════════╝
    """

    weapon = 'DEAD!'
    for obj in game.get_objects():
        if isinstance(obj, Player):
            weapon = obj._weapon.name
    
    string = ''
    string += '╔' + '═' * (game.WIDTH - 2) + '╗\n'
    string += '║ WEAPON: ' + weapon + ' ' * (game.WIDTH - len(weapon) - 11) + '║\n'
    string += '╚' + '═' * (game.WIDTH - 2) + '╝\n'

    return string


def display():
    screen = game.empty_screen()

    for obj in sorted(game.get_objects(), key=lambda obj: obj.z):
        real_x = round(obj.x)
        real_y = round(obj.y)

        if obj.parent != None:
            real_x += round(obj.parent.x)
            real_y += round(obj.parent.y)
        
        if (0 <= real_x <= game.WIDTH - 1) and (0 <= real_y <= game.HEIGHT - 1):
            str_pos = real_y * (game.WIDTH + 1) + real_x
            screen[str_pos] = obj.style + obj.char + Style.RESET_ALL
    
    display_string = top_bar() + ''.join(screen)

    game.clear()
    print(display_string)


def handle_collisions():
    for obj in game.get_solids():
        for obj_col in game.get_solids():
            if not obj is obj_col:
                diff = Positional(obj.x - obj_col.x, obj.y - obj_col.y)
                if diff.get_length() <= 1:
                    obj.collide(obj_col)


def distribute_objects(gen, count):
    spaces = game.WIDTH * game.HEIGHT

    for x in range(game.WIDTH):
        for y in range(game.HEIGHT):
            if spaces == 1 or random.randint(0, spaces - 1) <= count:
                game.add_object(gen(x, y))
                count -= 1
            
            spaces -= 1


def generate_foliage(x, y):
    chars = (',', '.', '\'', '"', '`')
    return Drawable(char=random.choice(chars), x=x, y=y, style=Fore.GREEN)


def generate_trees(x, y):
    chars = ('♠', '♣', '▲')
    return Drawable(char=random.choice(chars), x=x, y=y, z=1, solid=True, style=Fore.GREEN)


def init_map():
    distribute_objects(generate_foliage, 100)
    #distribute_objects(generate_trees, 20)

    for _ in range(10):
        game.add_object(Rat())


def main():
    game.add_object(Player())

    init_map()
    
    delta = 0.0
    start = time.time()

    while True:
        display()

        for obj in game.get_objects():
            obj.step(delta)
        
        handle_collisions()

        time.sleep(game.FRAME_DELAY)

        delta = time.time() - start
        start = time.time()


if __name__ == "__main__":
    main()
