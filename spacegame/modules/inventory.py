import pantsmud
from pantsmud.driver import auxiliary, command, hook, parser
from pantsmud.util import message
from spacegame.core import aux_types, hook_types
from spacegame.universe import item


class InventoryAux(object):
    def __init__(self):
        self.inventory = []

    def load_data(self, data):
        inv_items = []
        for item_data in data["inventory"]:
            inv_item = item.Item()
            inv_item.load_data(item_data)
            inv_items.append(inv_item)
            pantsmud.game.environment.add_item(inv_item)
        self.inventory = inv_items

    def save_data(self):
        return {
            "inventory": [inv_item.save_data() for inv_item in self.inventory]
        }


def inventory_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    inventory = mobile.aux["inventory"].inventory
    inventory_data = {i.name: str(i.uuid) for i in inventory}
    message.command_success(mobile, cmd, {"inventory": inventory_data})


def test_add_active_warp_scanner_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    i = item.Item()
    i.name = "Active Warp Scanner"
    mobile.aux["inventory"].inventory.append(i)
    pantsmud.game.environment.add_item(i)
    message.command_success(mobile, cmd)


def clear_inventory_hook(_, mobile):
    for i in mobile.aux["inventory"].inventory:
        pantsmud.game.environment.remove_item(i)


def init():
    auxiliary.install(aux_types.AUX_TYPE_ENTITY, "inventory", InventoryAux)
    command.add_command("inventory", inventory_command)
    command.add_command("test.add_active_warp_scanner", test_add_active_warp_scanner_command)
    hook.add(hook_types.REMOVE_MOBILE, clear_inventory_hook)
