from base_classes import *
from bullet import Bullet
from colorama import Fore
from player import Player

import game
import random


class Rat(Moveable):
    def __init__(self, speed=5):
        start_x = random.randint(0, game.WIDTH - 1)
        start_y = random.randint(0, game.HEIGHT - 1)

        super().__init__(char='R', x=start_x, y=start_y, z=98, style=Fore.YELLOW)

        self._speed = speed
        self._move = True
        self._timer = 2
    
    def step(self, delta):
        self._timer -= delta

        if self._timer <= 0:
            self._move = not self._move
            self.velocity = Positional()
            self._timer = random.randint(1, 3)
            self._shoot()

        if self._move and self.velocity.x == self.velocity.y == 0:
            self.velocity.x = random.randint(-self._speed, self._speed)
            self.velocity.y = random.randint(-self._speed, self._speed)
        
        super().step(delta)

    def _shoot(self):
        for obj in game.get_objects():
            if isinstance(obj, Player):
                target = Positional(obj.x - self.x, obj.y - self.y)
                Bullet.spawn(spawn=self, dir=target, speed=20, ignore={'Rat'})
