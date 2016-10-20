import spacegame.commands
import spacegame.core
import spacegame.modules

def init():
    spacegame.core.init()
    spacegame.modules.init()  # Init modules after core
    spacegame.commands.init()  # Init commands after modules


def start():
    spacegame.modules.start()
