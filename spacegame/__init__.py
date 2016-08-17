import logging
from pantsmud.driver import hook

def open_brain_hook(_, brain):
    logging.debug("brain %r opened" % brain)

def close_brain_hook(_, brain):
    logging.debug("brain %r closed" % brain)

def init():
    hook.add(hook.HOOK_OPEN_BRAIN, open_brain_hook)
    hook.add(hook.HOOK_CLOSE_BRAIN, close_brain_hook)
