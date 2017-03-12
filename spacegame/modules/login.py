import logging
import random
from pantsmud.driver import parser
from pantsmud.util import error, message


class Service(object):
    def __init__(self, entities, game_commands, universe, users):
        self.entities = entities
        self.game_commands = game_commands
        self.universe = universe
        self.users = users

    def register(self, name):
        if self.users.player_name_exists(name):
            raise error.CommandFail()  # TODO Add error message.
        u = self.users.User()
        u.name = name
        p = self.entities.new_mobile()
        p.name = name
        star_system = random.choice(list(self.universe.core_star_systems))
        p.celestial = random.choice(list(star_system.core_celestials))
        u.player_uuid = p.uuid
        self.users.save_user(u)
        self.users.save_player(p)
        return p.name, u.uuid

    def login(self, brain, user_uuid):
        if not self.users.user_exists(user_uuid):
            logging.debug("login failed due to non-existent user")
            raise error.CommandFail()  # TODO Add error message.
        u = self.users.load_user(user_uuid)
        if not u.player_uuid or not self.users.player_exists(u.player_uuid):
            logging.debug("login failed due to non-existent player")
            raise error.CommandFail()  # TODO Add error message.
        u.attach_brain(brain)
        self.universe.add_identity(u)
        p = self.users.load_player(u.player_uuid)
        p.attach_brain(brain)
        self.universe.add_entity(p)
        brain.replace_input_handler(self.game_commands.command_input_handler, "game")
        return p.name

    def quit(self, brain):
        brain.close()


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def register(self, request):
        player_name, user_uuid = self.service.register(
            request["name"]
        )
        return {
            "name": player_name,
            "uuid": str(user_uuid)
        }

    def login(self, request):
        player_name = self.service.login(
            request["brain"],
            request["user_uuid"]
        )
        return {
            "name": player_name
        }

    def quit(self, request):
        self.service.quit(
            request["brain"]
        )


def make_register_command(endpoint):
    def register_command(brain, cmd, args):
        params = parser.parse([("name", parser.WORD)], args)
        request = {
            "name": params["name"]
        }
        response = endpoint.register(request)
        message.command_success(brain, cmd, response)
    return register_command


def make_login_command(endpoint):
    def login_command(brain, cmd, args):
        params = parser.parse([("uuid", parser.UUID)], args)
        request = {
            "brain": brain,
            "user_uuid": params["uuid"]
        }
        response = endpoint.login(request)
        message.command_success(brain, cmd, response)
    return login_command


def make_quit_command(endpoint):
    def quit_command(brain, _, args):
        parser.parse([], args)
        request = {
            "brain": brain
        }
        endpoint.quit(request)
    return quit_command


def init(entities, game_commands, login_commands, universe, users):
    service = Service(
        entities,
        game_commands,
        universe,
        users
    )
    endpoint = Endpoint(service)
    login_commands.add_command("register", make_register_command(endpoint))
    login_commands.add_command("login", make_login_command(endpoint))
    login_commands.add_command("quit", make_quit_command(endpoint))
