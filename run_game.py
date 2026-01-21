#!/usr/bin/env python
"""
Launcher script for Dodge Game 2D
"""
import sys
from Game.main import DodgeGame

if __name__ == '__main__':
    game = DodgeGame()
    game.run()
