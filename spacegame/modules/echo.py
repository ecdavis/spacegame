from pantsmud.driver import parser
from pantsmud.util import message


class Service(object):
    def __init__(self, hooks, universe, users):
        self.hooks = hooks
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


def make_echo_endpoint(service):
    def echo_endpoint(request):
        result = service.echo(
            request["line"]
        )
        return {
            "line": result
        }
    return echo_endpoint


def make_quit_endpoint(service):
    def quit_endpoint(request):
        service.quit(
            request["brain"]
        )
    return quit_endpoint


def make_shutdown_endpoint(service):
    def shutdown_endpoint(request):
        service.shutdown()
    return shutdown_endpoint


def make_echo_command(endpoint):
    def echo_command(brain, cmd, args):
        request = {
            "line": args
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return echo_command


def make_quit_command(endpoint):
    def quit_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "brain": brain
        }
        endpoint(request)
    return quit_command


def make_shutdown_command(endpoint):
    def shutdown_command(brain, _, args):
        parser.parse([], args)
        request = {}
        endpoint(request)
    return shutdown_command


def init(commands, hooks, universe, users):
    service = Service(hooks, universe, users)
    commands.add_command(
        "echo",
        make_echo_command(
            make_echo_endpoint(service)
        )
    )
    commands.add_command(
        "quit",
        make_quit_command(
            make_quit_endpoint(service)
        )
    )
    commands.add_command(
        "shutdown",
        make_shutdown_command(
            make_shutdown_endpoint(service)
        )
    )
