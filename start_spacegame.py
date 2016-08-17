import logging
import pants
from pantsmud.driver import game, net

if __name__ == '__main__':
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.DEBUG)

    # Initialize the game.
    engine = pants.Engine.instance()
    game.init(engine, None)
    net.init()
    game.start()
