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


class Service(object):
    def __init__(self, universe):
        self.universe = universe

    def inventory(self, mobile):
        fitted_data = mobile.aux["inventory"].fitted
        if fitted_data:
            fitted_data = {fitted_data.name: str(fitted_data.uuid)}
        inventory = mobile.aux["inventory"].inventory
        inventory_data = {i.name: str(i.uuid) for i in inventory}
        return fitted_data, inventory_data

    def fit(self, mobile, item_uuid):
        if mobile.aux["inventory"].fitted:
            raise error.CommandFail()
        inventory = mobile.aux["inventory"].inventory[:]
        fittable_item = None
        for i in inventory:
            if i.uuid == item_uuid:
                fittable_item = i
        if fittable_item is None:
            raise error.CommandFail()
        inventory = [i for i in inventory if i.uuid != item_uuid]
        mobile.aux["inventory"].fitted = fittable_item
        mobile.aux["inventory"].inventory = inventory

    def unfit(self, mobile):
        if mobile.aux["inventory"].fitted is None:
            raise error.CommandFail()
        inventory = mobile.aux["inventory"].inventory[:]
        fitted_item = mobile.aux["inventory"].fitted
        inventory.append(fitted_item)
        mobile.aux["inventory"].fitted = None
        mobile.aux["inventory"].inventory = inventory

    def test_add_active_warp_scanner(self, mobile):
        i = item.Item()
        i.name = "Active Warp Scanner"
        mobile.aux["inventory"].inventory.append(i)
        self.universe.add_item(i)
        return i.uuid


def make_inventory_endpoint(service):
    def inventory_endpoint(request):
        fitted_data, inventory_data = service.inventory(
            request["mobile"]
        )
        return {
            "fitted": fitted_data,
            "inventory": inventory_data
        }
    return inventory_endpoint


def make_fit_endpoint(service):
    def fit_endpoint(request):
        service.fit(
            request["mobile"],
            request["item_uuid"],
        )
    return fit_endpoint


def make_unfit_endpoint(service):
    def unfit_endpoint(request):
        service.unfit(
            request["mobile"]
        )
    return unfit_endpoint


def make_test_add_active_warp_scanner_endpoint(service):
    def test_add_active_warp_scanner_endpoint(request):
        item_uuid = service.test_add_active_warp_scanner(
            request["mobile"]
        )
        return {
            "item": str(item_uuid)
        }
    return test_add_active_warp_scanner_endpoint


def make_inventory_command(endpoint):
    def inventory_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return inventory_command


def make_fit_command(endpoint):
    def fit_command(brain, cmd, args):
        params = parser.parse([("item_uuid", parser.UUID)], args)
        request = {
            "mobile": brain.mobile,
            "item_uuid": params["item_uuid"]
        }
        endpoint(request)
        message.command_success(brain, cmd, None)
    return fit_command


def make_unfit_command(endpoint):
    def unfit_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        endpoint(request)
        message.command_success(brain, cmd, None)
    return unfit_command


def make_test_add_active_warp_scanner_command(endpoint):
    def test_add_active_warp_scanner_command(brain, cmd, args):
        parser.parse([], args)
        request = {
            "mobile": brain.mobile
        }
        response = endpoint(request)
        message.command_success(brain, cmd, response)
    return test_add_active_warp_scanner_command


def clear_inventory_hook(_, mobile):
    if mobile.aux["inventory"].fitted is not None:
        pantsmud.game.environment.remove_item(mobile.aux["inventory"].fitted)
    for i in mobile.aux["inventory"].inventory:
        pantsmud.game.environment.remove_item(i)


def init(auxiliaries, commands, hooks, universe):
    auxiliaries.install(aux_types.AUX_TYPE_ENTITY, "inventory", InventoryAux)
    hooks.add(hook_types.REMOVE_MOBILE, clear_inventory_hook)
    service = Service(universe)
    commands.add_command(
        "inventory",
        make_inventory_command(
            make_inventory_endpoint(service)
        )
    )
    commands.add_command(
        "fit",
        make_fit_command(
            make_fit_endpoint(service)
        )
    )
    commands.add_command(
        "unfit",
        make_unfit_command(
            make_unfit_endpoint(service)
        )
    )
    commands.add_command(
        "test.add_active_warp_scanner",
        make_test_add_active_warp_scanner_command(
            make_test_add_active_warp_scanner_endpoint(service)
        )
    )
