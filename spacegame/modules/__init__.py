from pantsmud.util import message
from spacegame.core import user
from spacegame.modules import chat, echo, info, inventory, jump, login, thrust, warp
from spacegame.universe import entity


def init(auxiliaries, game_commands, hooks, login_commands, universe):
    chat.init(game_commands, message, universe)
    echo.init(game_commands, hooks, message, universe, user)
    info.init(game_commands, message)
    inventory.init(auxiliaries, game_commands, hooks, message, universe)
    jump.init(game_commands, hooks, message, universe)
    login.init(entity, game_commands, login_commands, message, universe, user)
    thrust.init(game_commands, message)
    warp.init(auxiliaries, game_commands, entity, hooks, universe)


def start():
    thrust.start()
