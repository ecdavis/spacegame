from pantsmud.driver import auxiliary, command, hook
import spacegame.core
from spacegame.core import login_manager
import spacegame.commands
import spacegame.modules


def init():
    spacegame.core.init(hook)
    spacegame.modules.init(auxiliary, command, hook, login_manager)  # Init modules after core
    spacegame.commands.init(command)  # Init commands after modules


def start():
    spacegame.modules.start()
