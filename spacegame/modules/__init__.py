from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp


def init(auxiliaries, entities, game_commands, hooks, login_commands, messages, universe, users):
    chat.init(game_commands, messages, universe)
    echo.init(game_commands, hooks, messages, universe, users)
    info.init(game_commands, messages)
    inventory.init(auxiliaries, game_commands, hooks, messages, universe)
    jump.init(game_commands, hooks, messages, universe)
    login.init(entities, game_commands, login_commands, universe, users)
    thrust.init(game_commands, messages)
    warp.init(auxiliaries, game_commands, entities, hooks, universe)


def start():
    thrust.start()
