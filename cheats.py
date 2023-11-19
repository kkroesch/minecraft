#!/usr/bin/env python3

"""
Some godmode cheats via RCON.
Call with

  $ RCON_PASSWORD=mySecurePassword ./cheats.py
"""

from os import environ as env
from mcrcon import MCRcon


RCON_SERVER = "localhost"
RCON_PASSWORD = env.get('RCON_PASSWORD')


def fill_toolkit(player):
	with MCRcon(RCON_SERVER, RCON_PASSWORD) as mcr:
		resp= mcr.command(f"give {player} minecraft:iron_pickaxe")
		resp= mcr.command(f"give {player} minecraft:iron_shovel")
		resp= mcr.command(f"give {player} minecraft:iron_axe")
