import logging
from spacegame.application import main

if __name__ == '__main__':
    if __debug__:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    main("data", ('127.0.0.1', 4040))
