import logging
import random
import pantsmud.game
from pantsmud.driver import command, parser
from pantsmud.util import error, message
from spacegame.core import user
from spacegame.universe import entity


class Service(object):
    def __init__(self, entities, game_commands, messages, universe, users):
        self.entities = entities
        self.game_commands = game_commands
        self.messages = messages
        self.universe = universe
        self.users = users

    def register(self, brain, name):
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
        self.messages.command_success(brain, "register", {"name": p.name, "uuid": str(u.uuid)})

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
        self.messages.command_success(brain, "login", {"name": p.name})
        brain.replace_input_handler(self.game_commands.command_input_handler, "game")

    def quit(self, brain):
        brain.close()


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def register(self, request):
        self.service.register(
            request["brain"],
            request["name"]
        )

    def login(self, request):
        self.service.login(
            request["brain"],
            request["user_uuid"]
        )

    def quit(self, request):
        self.service.quit(
            request["brain"]
        )


def make_register_command(endpoint):
    def register_command(brain, cmd, args):
        params = parser.parse([("name", parser.WORD)], args)
        request = {
            "brain": brain,
            "name": params["name"]
        }
        endpoint.register(request)
    return register_command


def make_login_command(endpoint):
    def login_command(brain, cmd, args):
        params = parser.parse([("uuid", parser.UUID)], args)
        request = {
            "brain": brain,
            "user_uuid": params["uuid"]
        }
        endpoint.login(request)
    return login_command


def make_quit_command(endpoint):
    def quit_command(brain, _, args):
        parser.parse([], args)
        request = {
            "brain": brain
        }
        endpoint.quit(request)
    return quit_command


def init(game_commands, login_commands, universe):
    service = Service(
        entity,
        game_commands,
        message,
        universe,
        user
    )
    endpoint = Endpoint(service)
    login_commands.add_command("register", make_register_command(endpoint))
    login_commands.add_command("login", make_login_command(endpoint))
    login_commands.add_command("quit", make_quit_command(endpoint))
