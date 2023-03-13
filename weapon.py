from base_classes import *
from bullet import Bullet

import game
import random
import time

class Weapon():
    def __init__(self, name='', reload=1, wielder=None):
        self.name = name
        self._reload = reload
        self._wielder = wielder
        self._last_shot = 0
    
    def shoot(self, dir):
        if dir.x != 0 or dir.y != 0:
            if self._last_shot + self._reload <= time.time():
                self._last_shot = time.time()
                self._shoot(dir)
    
    def _shoot(self, dir):
        pass

class Shotgun(Weapon):
    def __init__(self, wielder):
        super().__init__(name='SHOTGUN', wielder=wielder)

    def _offset(self):
        return random.randint(-10, 10) / 20.0

    def _shoot(self, dir):
        for _ in range(6):
            dir = Positional(dir.x + self._offset(), dir.y + self._offset())
            Bullet.spawn(self._wielder, dir, 40, ignore=('Player'))

class SMG(Weapon):
    def __init__(self, wielder):
        super().__init__(name='MINIGUN', reload=0.07, wielder=wielder)

    def _shoot(self, dir):
        Bullet.spawn(self._wielder, dir, 80, ignore=('Player'))


class Rocket(Bullet):
    def __init__(self, spawn):
        super().__init__(char='R', x=spawn.x, y=spawn.y, z=10, ignore=('Player'))

    def collide(self, collider):
        super().collide(collider)

        if not self in game.get_objects(): # Was destroyed in collision
            i = 0
            while i < len(game.get_objects()):
                obj = game.get_objects()[i]

                diff = Positional(obj.x - self.x, obj.y - self.y)

                if self.is_collidable(obj) and diff.get_length() < 5:
                    game.del_object(obj)
                else:
                    i += 1

class RocketLauncher(Weapon):
    def __init__(self, wielder):
        super().__init__(name='ROCKET LAUNCHER', reload=2, wielder=wielder)

    def _shoot(self, dir):
        rocket = Rocket(spawn=self._wielder)
        rocket.velocity = dir.get_normal() * 20
        game.add_object(rocket)
