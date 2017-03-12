from pantsmud.driver import parser
from pantsmud.util import message


class Service(object):
    def __init__(self, hooks, messages, universe, users):
        self.hooks = hooks
        self.messages = messages
        self.universe = universe
        self.users = users

    def echo(self, line):
        return line

    def quit(self, brain):
        if brain.mobile and brain.identity:
            self.users.save_player(brain.mobile)
        brain.close()
        return None

    def shutdown(self):
        for m in self.universe.get_mobiles():
            if m.brain.identity:
                self.users.save_player(m)
                m.brain.close()
        self.hooks.run(self.hooks.HOOK_SHUTDOWN)
        return None


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def echo(self, request):
        result = self.service.echo(
            request["line"]
        )
        return {
            "line": result
        }

    def quit(self, request):
        self.service.quit(
            request["brain"]
        )
        return None

    def shutdown(self, request):
        self.service.shutdown()
        return None


def make_echo_command(endpoint):
    def echo_command(brain, cmd, args):
        request = {
            "line": args
        }
        response = endpoint.echo(request)
        message.command_success(brain, cmd, response)
    return echo_command


def make_quit_command(endpoint):
    def quit_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "brain": brain
        }
        endpoint.quit(request)
    return quit_command


def make_shutdown_command(endpoint):
    def shutdown_command(brain, _, args):
        parser.parse([], args)
        request = {}
        endpoint.shutdown(request)
    return shutdown_command


def init(commands, hooks, messages, universe, users):
    service = Service(hooks, messages, universe, users)
    endpoint = Endpoint(service)
    commands.add_command("echo", make_echo_command(endpoint))
    commands.add_command("quit", make_quit_command(endpoint))
    commands.add_command("shutdown", make_shutdown_command(endpoint))
