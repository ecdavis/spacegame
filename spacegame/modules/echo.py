from pantsmud.driver import parser


class Service(object):
    def __init__(self, hooks, messages, universe, users):
        self.hooks = hooks
        self.messages = messages
        self.universe = universe
        self.users = users

    def echo(self, mobile, line):
        self.messages.command_success(mobile, "echo", {"line": line})

    def quit(self, brain):
        if brain.mobile and brain.identity:
            self.users.save_player(brain.mobile)
        brain.close()

    def shutdown(self):
        for m in self.universe.get_mobiles():
            if m.brain.identity:
                self.users.save_player(m)
                m.brain.close()
        self.hooks.run(self.hooks.HOOK_SHUTDOWN)


class Endpoint(object):
    def __init__(self, service):
        self.service = service

    def echo(self, request):
        self.service.echo(
            request["mobile"],
            request["line"]
        )

    def quit(self, request):
        self.service.quit(
            request["brain"]
        )

    def shutdown(self, request):
        self.service.shutdown()


def make_echo_command(endpoint):
    def echo_command(brain, cmd, args):
        request = {
            "mobile": brain.mobile,
            "line": args
        }
        endpoint.echo(request)
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
