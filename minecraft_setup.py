
"""
Start with
  $ PYTHONSTARTUP=~/minecraft_startup.py python3
to get a Python REPL where you can interactively use some of the functions below.
"""

import math

from mcpi.minecraft import Minecraft
import mcpi.block as block

DEBUG = True

mc = Minecraft.create()
player_ids = mc.getPlayerEntityIds()

print("Minecraft connected as `mc`")
print("Block module imported as `block`")
print(f"Players online: {player_ids}")

PLAYER_ID = 1181

x,y,z = 0,0,0


def debug(message):
    if DEBUG:
        print(message)


def position(player_id=PLAYER_ID):
    # Position und Orientierung des Spielers abfragen
    start_x, start_y, start_z = mc.entity.getPos(player_id)
    pitch = mc.entity.getPitch(PLAYER_ID)
    yaw = mc.entity.getRotation(PLAYER_ID)
    print(f"Position X={start_x}, Y={start_y}, Z={start_z}")
    print(f"Yaw (horizontale Drehung): {yaw}")
    print(f"Pitch (vertikale Drehung): {pitch}")
    x, y, z = math.floor(start_x), math.floor(start_y), math.floor(start_z)

    return x,y,z,pitch,yaw


def is_bodenschatz(block_id):
    # Liste der IDs für Bodenschätze
    bodenschaetze = [block.COAL_ORE.id, block.IRON_ORE.id, block.GOLD_ORE.id,
                     block.DIAMOND_ORE.id, block.EMERALD_ORE.id, block.REDSTONE_ORE.id]
    return block_id in bodenschaetze



def flatten(width=5, height=40):
    """ Planiert um die Position des Spielers herum bis zur angegebenen Höhe. """
    x,y,z,_,_ = position()
    for xx in range(x-width, x+width):
        for zz in range(z-width, z+width):
            for yy in range(y, y+height):
                mc.setBlock(xx, yy, zz, block.AIR)


def floor(width=20, material=block.STONE):
    """ Belegt die Fläche um den Spieler mit Steinen oder anderem Material. """
    x,y,z,_,_ = position()
    for xx in range(x-width, x+width):
        for zz in range(z-width, z+width):
                mc.setBlock(xx, y-1, zz, block.STONE)


def tower(width, height, material=block.STONE_BRICK):
    """ Baut einen Turm mit Decke an der Position """
    x,y,z,_,_ = position()
    for k in range(height):
        for i in range(width):
            for j in range(width):
                if i == 0 or i == width - 1 or j == 0 or j == width - 1 or k == height-1:
                    mc.setBlock(x+i, y+k, z+j, material)


def find_blocks(radius, funktion):
    x,y,z,pitch,_ = position()

    # Durchlaufen des quadratischen Bereichs um den Spieler
    for dx in range(-radius, radius + 1):
        for dy in range(-radius, radius + 1):
            for dz in range(-radius, radius + 1):
                block_x = x + dx
                block_y = y + dy
                block_z = z + dz

                # Block-ID und Datenwert des aktuellen Blocks abfragen
                block_id = mc.getBlock(block_x, block_y, block_z)

                # Anwenden der übergebenen Funktion auf den Block
                funktion(block_x, block_y, block_z, block_id)


def block_handler(x, y, z, block_id):
    # Hier können Sie definieren, was mit jedem Block geschehen soll
    print(f"Block gefunden bei ({x}, {y}, {z}) mit ID {block_id}")


def stairs(length=10):
    """ Baut eine gerade Treppe auf einen Berg. """
    x,y,z,pitch,yaw = position()

    # Richtung der Treppe bestimmen basierend auf Yaw-Wert
    dx = int(round(-math.sin(math.radians(yaw))))
    dz = int(round(math.cos(math.radians(yaw))))

    # Datenwert für die Ausrichtung der Treppe bestimmen
    if dx == 1:
        data = 0  # Treppe nach Osten
    elif dx == -1:
        data = 1  # Treppe nach Westen
    elif dz == 1:
        data = 2  # Treppe nach Süden
    elif dz == -1:
        data = 3  # Treppe nach Norden

    for i in range(length):
        # Position der nächsten Stufe
        x += dx
        z += dz
        # Höhe der nächsten Stufe anpassen
        while mc.getBlock(x, y - 1, z) == block.AIR.id:
            y -= 1
        while mc.getBlock(x, y - 1, z) != block.AIR.id:
            y += 1

        # Stufe setzen
        mc.setBlock(x, y - 1, z, block.STONE_BRICK.id, data)


def upstairs(hoehe=5):
    """ Gräbt ein Treppenhaus nach oben. """
    x,y,z,_,_ = position()
    xx, yy, zz, = x, y, z

    richtungen = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    richtungsindex = 0
    schritte = 0

    for h in range(hoehe):
        # Aktuelle Richtung bestimmen
        dx, dz = richtungen[richtungsindex % 4]

        # Vorwärts und nach oben graben
        mc.setBlock(xx, yy-1, zz, block.AIR)
        mc.setBlock(xx, yy, zz, block.AIR)
        mc.setBlock(xx, yy+1, zz, block.AIR)
        xx += dx
        zz += dz
        yy += 1
        schritte += 1

        # Nach fünf Schritten Richtung ändern
        if schritte == 5:
            schritte = 0
            richtungsindex += 1


def seddle_roof(dachlaenge=10, dachhoehe=5):
    start_x, start_y, start_z, _, _ = position()

    # Dach erstellen
    for i in range(dachhoehe):
        # Jede Ebene des Daches
        breite = dachlaenge - (2 * i)
        hoehe = start_y + i
        for j in range(breite):
            # Linke Seite des Daches
            mc.setBlock(start_x + j, hoehe, start_z - i, block.STAIRS_WOOD.id, 0)
            # Rechte Seite des Daches
            mc.setBlock(start_x + j, hoehe, start_z + i, block.STAIRS_WOOD.id, 1)


def circle(radius, height=1, block_id=block.STONE_BRICK):
    """ Baut einen Kreis aus Blöcken um den Spieler. """
    start_x, start_y, start_z, _, _ = position()

    for h in range(height):
        for winkel in range(360):
            radian = math.radians(winkel)
            x = start_x + radius * math.cos(radian)
            z = start_z + radius * math.sin(radian)
            mc.setBlock(int(x), start_y+h, int(z), block_id)
