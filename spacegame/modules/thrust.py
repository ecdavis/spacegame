from pantsmud.driver import error, game, message, parser
from spacegame.core import command_manager
from spacegame.core.game import get_universe


POSITION_UPDATE_TICK = 0.1


def thrust_speed_command(mobile, cmd, args):
    params = parser.parse([("speed", parser.INT)], args)
    speed = params["speed"]
    if speed < 0 or speed > 10:
        raise error.CommandError()  # TODO Add error message.
    mobile.speed = speed
    message.command_success(mobile, cmd)


def thrust_vector_command(mobile, cmd, args):
    params = parser.parse([("x", parser.FLOAT), ("y", parser.FLOAT), ("z", parser.FLOAT)], args)
    x = round(params["x"], 3)
    y = round(params["y"], 3)
    z = round(params["z"], 3)
    vector = (x, y, z)
    if x > 1.0 or y > 1.0 or z > 1.0:
        raise error.CommandError()  # TODO Add error message.
    if abs(1.0 - sum((abs(x), abs(y), abs(z)))) > 0.001:
        raise error.CommandError()  # TODO Add error message.
    mobile.vector = vector
    message.command_success(mobile, cmd)


def position_update(mobile, seconds):
    mobile.position = (round(mobile.position[0] + (mobile.velocity()[0] * seconds), 3),
                       round(mobile.position[1] + (mobile.velocity()[1] * seconds), 3),
                       round(mobile.position[2] + (mobile.velocity()[2] * seconds), 3))


def position_update_cycle():
    for mobile in get_universe().mobiles.values():
        position_update(mobile, POSITION_UPDATE_TICK)


def init():
    command_manager.add_command("thrust.speed", thrust_speed_command)
    command_manager.add_command("thrust.vector", thrust_vector_command)


def start():
    game.engine.cycle(POSITION_UPDATE_TICK, position_update_cycle)
