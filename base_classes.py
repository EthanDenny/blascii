from colorama import Fore

import game
import math


class Positional:
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    def get_length(self):
        return math.sqrt(self.x**2 + self.y**2)

    def get_normal(self):
        return self / self.get_length()

    def __mul__(self, other):
        if isinstance(other, Positional):
            return Positional(self.x * other.x, self.y * other.y)
        else:
            return Positional(self.x * other, self.y * other)

    def __truediv__(self, other):
        if isinstance(other, Positional):
            return Positional(self.x / other.x, self.y / other.y)
        else:
            return Positional(self.x / other, self.y / other)


class Drawable(Positional):
    def __init__(self, char=' ', x=0.0, y=0.0, z=0, parent=None, solid=False, style=Fore.WHITE):
        super().__init__(x=x, y=y)

        self.char = char
        self.z = z
        self.parent = parent
        self.children = []
        self.solid = solid
        self.style = style
    
    def step(self, _):
        pass

    def add_child(self, child):
        child.parent = self
        self.children.append(child)
        game.add_object(child)

    def collide(self, collider):
        pass


class Moveable(Drawable):
    def __init__(self, **kwargs):
        super().__init__(solid=True, **kwargs)

        self.velocity = Positional()
    
    def step(self, delta):
        self.x += self.velocity.x * delta
        self.y += self.velocity.y * delta
