"""
Global variables and methods
"""

# CONFIG

WIDTH = 100
HEIGHT = 40
FRAME_DELAY = 0.01


# GLOBAL IMPORTS

from colorama import just_fix_windows_console
import os

# SETUP

just_fix_windows_console()
os.system(f'mode {WIDTH}, {HEIGHT + 4}')

# INTERNAL (DO NOT EDIT)

EMPTY_SCREEN = []

for i in range(HEIGHT):
    for j in range(WIDTH):
        EMPTY_SCREEN.append(' ')
    EMPTY_SCREEN.append('\n')

EMPTY_SCREEN = EMPTY_SCREEN[:-1]

empty_screen = EMPTY_SCREEN.copy

objects = []

def obj_count():
    return len(objects)

def add_object(obj):
    objects.append(obj)

def del_object(obj):
    from base_classes import Drawable

    if obj and isinstance(obj, Drawable):
        for child in obj.children:
            del_object(child)
        
        if obj.parent:
            obj.parent.children.remove(obj)
        
        if obj in objects:
            objects.remove(obj)

def get_objects():
    return objects

def get_solids():
    return [obj for obj in objects if obj.solid]

def clear():
    os.system('cls || clear')
