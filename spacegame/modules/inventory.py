import pantsmud
from pantsmud.driver import parser
from pantsmud.util import error, message
from spacegame.core import aux_types, hook_types
from spacegame.universe import item


class InventoryAux(object):
    def __init__(self):
        self.fitted = None
        self.inventory = []

    def load_data(self, data):
        if data["fitted"]:
            fitted_item = item.Item()
            fitted_item.load_data(data["fitted"])
            pantsmud.game.environment.add_item(fitted_item)
            self.fitted = fitted_item
        inv_items = []
        for item_data in data["inventory"]:
            inv_item = item.Item()
            inv_item.load_data(item_data)
            inv_items.append(inv_item)
            pantsmud.game.environment.add_item(inv_item)
        self.inventory = inv_items

    def save_data(self):
        return {
            "fitted": self.fitted.save_data() if self.fitted else None,
            "inventory": [inv_item.save_data() for inv_item in self.inventory]
        }


def inventory_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    fitted_data = mobile.aux["inventory"].fitted
    if fitted_data:
        fitted_data = {fitted_data.name: str(fitted_data.uuid)}
    inventory = mobile.aux["inventory"].inventory
    inventory_data = {i.name: str(i.uuid) for i in inventory}
    message.command_success(mobile, cmd, {"fitted": fitted_data, "inventory": inventory_data})


def fit_command(brain, cmd, args):
    params = parser.parse([("item_uuid", parser.UUID)], args)
    mobile = brain.mobile
    if mobile.aux["inventory"].fitted:
        raise error.CommandFail()
    inventory = mobile.aux["inventory"].inventory[:]
    fittable_item = None
    for i in inventory:
        if i.uuid == params["item_uuid"]:
            fittable_item = i
    if fittable_item is None:
        raise error.CommandFail()
    inventory = [i for i in inventory if i.uuid != params["item_uuid"]]
    mobile.aux["inventory"].fitted = fittable_item
    mobile.aux["inventory"].inventory = inventory
    message.command_success(mobile, cmd)


def unfit_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    if mobile.aux["inventory"].fitted is None:
        raise error.CommandFail()
    inventory = mobile.aux["inventory"].inventory[:]
    fitted_item = mobile.aux["inventory"].fitted
    inventory.append(fitted_item)
    mobile.aux["inventory"].fitted = None
    mobile.aux["inventory"].inventory = inventory
    message.command_success(mobile, cmd)


def test_add_active_warp_scanner_command(brain, cmd, args):
    parser.parse([], args)
    mobile = brain.mobile
    i = item.Item()
    i.name = "Active Warp Scanner"
    mobile.aux["inventory"].inventory.append(i)
    pantsmud.game.environment.add_item(i)
    message.command_success(mobile, cmd, {"item": str(i.uuid)})


def clear_inventory_hook(_, mobile):
    if mobile.aux["inventory"].fitted is not None:
        pantsmud.game.environment.remove_item(mobile.aux["inventory"].fitted)
    for i in mobile.aux["inventory"].inventory:
        pantsmud.game.environment.remove_item(i)


def init(auxiliaries, commands, hooks):
    auxiliaries.install(aux_types.AUX_TYPE_ENTITY, "inventory", InventoryAux)
    commands.add_command("inventory", inventory_command)
    commands.add_command("fit", fit_command)
    commands.add_command("unfit", unfit_command)
    commands.add_command("test.add_active_warp_scanner", test_add_active_warp_scanner_command)
    hooks.add(hook_types.REMOVE_MOBILE, clear_inventory_hook)
