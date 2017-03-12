import spacegame.core
import spacegame.commands
import spacegame.modules


def init(auxiliaries, game_commands, hooks, login_commands, universe):
    spacegame.core.init(hooks)
    spacegame.modules.init(auxiliaries, game_commands, hooks, login_commands, universe)  # Init modules after core


def start():
    spacegame.modules.start()
