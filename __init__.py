#
# Minecraft connection and initialisation
#

from mcpi.minecraft import Minecraft
import mcpi.block as block

mc = Minecraft.create()
try:
    player_ids = mc.getPlayerEntityIds()
except:
    print("Nobody is online.")
    player_ids = [0]

PLAYER_ID = player_ids[0]
DEBUG = True

def debug(message):
    if DEBUG:
        print(message)


def position(player_id=PLAYER_ID):
    """ Position und Orientierung des Spielers abfragen
    """
    start_x, start_y, start_z = mc.entity.getPos(player_id)
    pitch = mc.entity.getPitch(PLAYER_ID)
    yaw = mc.entity.getRotation(PLAYER_ID)
    debug(f"Position X={start_x}, Y={start_y}, Z={start_z}")
    debug(f"Yaw (horizontale Drehung): {yaw}")
    debug(f"Pitch (vertikale Drehung): {pitch}")
    x, y, z = math.floor(start_x), math.floor(start_y), math.floor(start_z)

    return x,y,z,pitch,yaw


debug("Minecraft connected as `mc`")
debug("Block module imported as `block`")
debug(f"Players online: {player_ids}")

