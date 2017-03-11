import logging
import pantsmud.game
from pantsmud.driver import hook
from spacegame.core import hook_types, login_manager


def open_brain_hook(_, brain):
    logging.debug("brain %r opened" % brain)
    pantsmud.game.environment.add_brain(brain)
    brain.push_input_handler(login_manager.login_input_handler, "login")


def close_brain_hook(_, brain):
    logging.debug("brain %r closed" % brain)
    if brain.mobile:
        mobile = brain.mobile
        mobile.detach_brain()
        if pantsmud.game.environment:
            pantsmud.game.environment.remove_entity(mobile)
            hook.run(hook_types.REMOVE_MOBILE, mobile)
    if brain.identity:
        identity = brain.identity
        identity.detach_brain()
        if pantsmud.game.environment:
            pantsmud.game.environment.remove_identity(identity)
    if pantsmud.game.environment:
        pantsmud.game.environment.remove_brain(brain)


def init(hooks):
    hooks.add(hooks.HOOK_OPEN_BRAIN, open_brain_hook)
    hooks.add(hooks.HOOK_CLOSE_BRAIN, close_brain_hook)
