import pantsmud.game
from pantsmud.driver import parser
from pantsmud.util import error, message


POSITION_UPDATE_TICK = 0.1


class Service(object):
    def thrust_speed(self, mobile, speed):
        if speed < 0 or speed > 10:
            raise error.CommandFail()  # TODO Add error message.
        mobile.speed = speed

    def thrust_vector(self, mobile, x, y, z):
        vector = (x, y, z)
        if x > 1.0 or y > 1.0 or z > 1.0:
            raise error.CommandFail()  # TODO Add error message.
        if abs(1.0 - sum((abs(x), abs(y), abs(z)))) > 0.001:
            raise error.CommandFail()  # TODO Add error message.
        mobile.vector = vector


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def thrust_speed(self, request):
        self.service.thrust_speed(
            request["mobile"],
            request["speed"]
        )

    def thrust_vector(self, request):
        self.service.thrust_vector(
            request["mobile"],
            request["x"],
            request["y"],
            request["z"]
        )


def make_thrust_speed_command(endpoint):
    def thrust_speed_command(brain, cmd, args):
        params = parser.parse([("speed", parser.INT)], args)
        request = {
            "mobile": brain.mobile,
            "speed": params["speed"]
        }
        endpoint.thrust_speed(request)
        message.command_success(brain, cmd, None)
    return thrust_speed_command


def make_thrust_vector_command(endpoint):
    def thrust_vector_command(brain, cmd, args):
        params = parser.parse([("x", parser.FLOAT), ("y", parser.FLOAT), ("z", parser.FLOAT)], args)
        request = {
            "mobile": brain.mobile,
            "x": params["x"],
            "y": params["y"],
            "z": params["z"]
        }
        endpoint.thrust_vector(request)
        message.command_success(brain, cmd, None)
    return thrust_vector_command


def position_update(mobile, seconds):
    mobile.position = (round(mobile.position[0] + (mobile.velocity()[0] * seconds), 3),
                       round(mobile.position[1] + (mobile.velocity()[1] * seconds), 3),
                       round(mobile.position[2] + (mobile.velocity()[2] * seconds), 3))


def position_update_cycle():
    for mobile in pantsmud.game.environment.entities.values():
        position_update(mobile, POSITION_UPDATE_TICK)


def init(commands):
    service = Service()
    endpoint = Endpoint(service)
    commands.add_command("thrust.speed", make_thrust_speed_command(endpoint))
    commands.add_command("thrust.vector", make_thrust_vector_command(endpoint))


def start():
    pantsmud.game.engine.cycle(POSITION_UPDATE_TICK, position_update_cycle)
