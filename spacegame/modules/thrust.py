from pantsmud.driver import parser
from spacegame.core import command_manager


def thrust_speed_command(mobile, _, args):
    params = parser.parse([("speed", parser.INT)], args)
    speed = params["speed"]
    if speed < 0 or speed > 10:
        mobile.message("thrust.speed.fail")
        return
    mobile.speed = speed
    mobile.message("thrust.speed.success")


def thrust_vector_command(mobile, _, args):
    params = parser.parse([("x", parser.FLOAT), ("y", parser.FLOAT), ("z", parser.FLOAT)], args)
    x = round(params["x"], 3)
    y = round(params["y"], 3)
    z = round(params["z"], 3)
    direction_vector = (x, y, z)
    if x > 1.0 or y > 1.0 or z > 1.0:
        mobile.message("thrust.vector.fail")
        return
    if abs(1.0 - sum((abs(x), abs(y), abs(z)))) > 0.001:
        mobile.message("thrust.vector.fail")
        return
    mobile.direction = direction_vector
    mobile.message("thrust.vector.success")


def init():
    command_manager.add_command("thrust.speed", thrust_speed_command)
    command_manager.add_command("thrust.vector", thrust_vector_command)
