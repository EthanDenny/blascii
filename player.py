from base_classes import *
from colorama import Fore

import game
import keyboard as key
import weapon


class Crosshair(Drawable):
    def __init__(self, speed=30, max_radius=8):
        super().__init__(char='☩', x=0, y=0, z=99, style=Fore.RED)
        self._speed = speed
        self._max_radius = max_radius
    
    def step(self, delta):
        if key.is_pressed('j') and not key.is_pressed('l'):
            self.x -= self._speed * delta
        elif key.is_pressed('l'):
            self.x += self._speed * delta
        if key.is_pressed('i') and not key.is_pressed('k'):
            self.y -= self._speed * delta
        elif key.is_pressed('k'):
            self.y += self._speed * delta
        
        if self.get_length() > self._max_radius:
            new_pos = self.get_normal() * self._max_radius
            self.x = new_pos.x
            self.y = new_pos.y
        
        super().step(delta)


class Player(Moveable):
    def __init__(self, speed=15):
        start_x = game.WIDTH // 2 - (1 - game.WIDTH % 2)
        start_y = game.HEIGHT // 2 - (1 - game.WIDTH % 2)

        super().__init__(char='@', x=start_x, y=start_y, z=100, style=Fore.CYAN)

        self._crosshair = Crosshair()
        self.add_child(self._crosshair)

        self._speed = speed
        self._weapon = weapon.Shotgun(self)
        self._can_switch = True
    
    def step(self, delta):
        if key.is_pressed('a') and not key.is_pressed('d'):
            self.velocity.x = -self._speed
        elif key.is_pressed('d'):
            self.velocity.x = self._speed
        else:
            self.velocity.x *= 0.5

        if key.is_pressed('w') and not key.is_pressed('s'):
            self.velocity.y = -self._speed
        elif key.is_pressed('s'):
            self.velocity.y = self._speed
        else:
            self.velocity.y *= 0.5
        
        if key.is_pressed('space'):
            if self._weapon.__class__.__name__ == 'SMG':
                self._speed = 5
            else:
                self._speed = 15
            self._weapon.shoot(self._crosshair)
        else:
            self._speed = 15
        
        if key.is_pressed('e') and self._can_switch:
            if self._weapon.__class__.__name__ == 'Shotgun':
                self._weapon = weapon.SMG(self)
            elif self._weapon.__class__.__name__ == 'SMG':
                self._weapon = weapon.RocketLauncher(self)
            elif self._weapon.__class__.__name__ == 'RocketLauncher':
                self._weapon = weapon.Shotgun(self)
            
            self._can_switch = False
        
        if not key.is_pressed('e'):
            self._can_switch = True
        
        super().step(delta)
