from base_classes import *

import game


class Bullet(Moveable):
    def __init__(self, ignore=('Player'), **kwargs):
        super().__init__(**kwargs)
        self._ignore = ignore

    def step(self, delta):
        if (0 <= round(self.x) <= game.WIDTH - 1 and 0 <= round(self.y) <= game.HEIGHT - 1):
            super().step(delta)
        else:
           game.del_object(self)
    
    def is_collidable(self, collider):
        class_name = collider.__class__.__name__
        return collider.solid and not class_name in self._ignore and not isinstance(collider, Bullet)

    def collide(self, collider):
        if self.is_collidable(collider):
            game.del_object(collider)
            game.del_object(self)
    
    @staticmethod
    def spawn(spawn, dir, speed=40, **kwargs):
        bullet = Bullet(char='●', x=spawn.x, y=spawn.y, z=10, **kwargs)
        bullet.velocity = dir.get_normal() * speed
        game.add_object(bullet)
