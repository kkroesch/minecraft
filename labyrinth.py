import random

import mcpi.block as block
from minecraft import mc, position, PLAYER_ID


# Dimensionen des Labyrinths
breite = 32
laenge = 32

# Startposition für das Labyrinth
start_x, start_y, start_z, _, _ = position(PLAYER_ID)

# Labyrinth als 2D-Array initialisieren
labyrinth = [[0 for _ in range(breite)] for _ in range(laenge)]

def labyrinth_erstellen(x, y):
    richtungen = [(1,0), (-1,0), (0,1), (0,-1)]
    random.shuffle(richtungen)

    for dx, dy in richtungen:
        nx, ny = x + dx*2, y + dy*2
        if 0 <= nx < laenge and 0 <= ny < breite and labyrinth[nx][ny] == 0:
            labyrinth[x+dx][y+dy] = 1
            labyrinth[nx][ny] = 1
            labyrinth_erstellen(nx, ny)

# Labyrinth generieren
labyrinth_erstellen(0, 0)

# Labyrinth in Minecraft erstellen
for x in range(laenge):
    for y in range(breite):
        block_type = block.STONE_BRICK if labyrinth[x][y] == 0 else block.AIR
        mc.setBlock(start_x + x, start_y, start_z + y, block_type)
        mc.setBlock(start_x + x, start_y+1, start_z + y, block_type)

# Eingang und Ausgang setzen
mc.setBlock(start_x, start_y, start_z, block.AIR)
mc.setBlock(start_x, start_y+1, start_z, block.AIR)
mc.setBlock(start_x + laenge - 1, start_y, start_z + breite - 1, block.AIR)
mc.setBlock(start_x + laenge - 1, start_y+1, start_z + breite - 1, block.AIR)

