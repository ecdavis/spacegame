from pantsmud.driver import command

_game_command_manager = command.CommandManager(__name__)
add_command = _game_command_manager.add
command_exists = _game_command_manager.exists
command_input_handler = _game_command_manager.input_handler
