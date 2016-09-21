import pantsmud.game
from pantsmud.driver import command, hook, parser
from pantsmud.util import message
from spacegame.core import user


def echo_command(brain, cmd, args):
    mobile = brain.mobile
    message.command_success(mobile, cmd, {"line": args})


def quit_command(brain, _, args):
    parser.parse([], args)
    brain.close()


def shutdown_command(brain, _, args):
    parser.parse([], args)
    universe = pantsmud.game.environment
    for m in [universe.mobiles[u] for u in universe.mobiles]:
        if m.brain.is_client:
            user.save_player(m)
            m.brain.close()
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command.add_command("echo", echo_command)
    command.add_command("quit", quit_command)
    command.add_command("shutdown", shutdown_command)
