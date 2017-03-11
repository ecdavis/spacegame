from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp


def init(auxiliaries, game_commands, hooks, login_commands):
    chat.init(game_commands)
    echo.init(game_commands)
    info.init(game_commands)
    inventory.init(auxiliaries, game_commands, hooks)
    jump.init(game_commands)
    login.init(login_commands)
    thrust.init(game_commands)
    warp.init(auxiliaries, hooks)


def start():
    thrust.start()
