from pantsmud.driver import hook, parser
from spacegame.core import command_manager, game, user


def echo_command(mobile, _, args):
    mobile.message("echo", {"line": args})


def quit_command(mobile, _, args):
    parser.parse([], args)
    mobile.brain.close()


def shutdown_command(mobile, _, args):
    parser.parse([], args)
    universe = game.get_universe()
    for m in [universe.mobiles[u] for u in universe.mobiles]:
        if m.brain.is_user:
            user.save_player(m)
            m.brain.close()
    hook.run(hook.HOOK_SHUTDOWN)


def init():
    command_manager.add_command("echo", echo_command)
    command_manager.add_command("quit", quit_command)
    command_manager.add_command("shutdown", shutdown_command)
