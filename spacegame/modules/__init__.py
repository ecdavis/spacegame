from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp


def init(auxiliaries, game_commands, hooks, login_commands, universe):
    chat.init(game_commands, universe)
    echo.init(game_commands, universe)
    info.init(game_commands)
    inventory.init(auxiliaries, game_commands, hooks, universe)
    jump.init(game_commands, universe)
    login.init(login_commands)
    thrust.init(game_commands)
    warp.init(auxiliaries, hooks)


def start():
    thrust.start()
