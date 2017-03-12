import spacegame.core
import spacegame.commands
import spacegame.modules


def init(auxiliaries, entities, game_commands, hooks, login_commands, messages, universe, users):
    spacegame.core.init(hooks)
    spacegame.modules.init(
        auxiliaries,
        entities,
        game_commands,
        hooks,
        login_commands,
        messages,
        universe,
        users
    )


def start():
    spacegame.modules.start()
