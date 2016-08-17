from pantsmud.driver import hook, parser
from spacegame.core import command_manager


def echo_command(mobile, _, args):
    mobile.message("echo", {"line": args})


def quit_command(mobile, _, args):
    parser.parse([], args)
    mobile.brain.close()


def shutdown_command(mobile, _, args):
    parser.parse([], args)
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command_manager.add_command("echo", echo_command)
    command_manager.add_command("quit", quit_command)
    command_manager.add_command("shutdown", shutdown_command)
