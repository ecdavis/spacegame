from pantsmud.driver import hook, parser
from spacegame.game import command_manager


def echo_command(brain, _, args):
    brain.message("echo", {"line": args})


def quit_command(brain, _, args):
    parser.parse([], args)
    brain.close()


def shutdown_command(brain, _, args):
    parser.parse([], args)
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command_manager.add_command("echo", echo_command)
    command_manager.add_command("quit", quit_command)
    command_manager.add_command("shutdown", shutdown_command)
