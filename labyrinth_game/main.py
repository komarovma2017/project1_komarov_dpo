from .constants import COMMANDS, ROOMS
from .player_actions import (
    get_input,
    move_player,
    show_inventory,
    take_item,
    use_item,
)

from .utils import (
    attempt_open_treasure,
    describe_current_room,
    show_help,
    solve_puzzle,
)


def process_command(game_state, command_line):
    parts = command_line.strip().split(maxsplit=1)
    command = parts.lower() if parts else ''
    argument = parts[1].lower() if len(parts) > 1 else ''
    move_commands = {'north', 'south', 'east', 'west'}

    if command in move_commands:
        move_player(game_state, command)
        return

    match command:
        case 'look':
            describe_current_room(game_state)
        case 'inventory':
            show_inventory(game_state)
        case 'go':
            if argument:
                move_player(game_state, argument)
            else:
                print("Укажите направление.")
        case 'take':
            if argument:
                take_item(game_state, argument)
            else:
                print("Укажите предмет.")
        case 'use':
            if argument == 'treasure_chest' or argument == 'treasure chest':
                current_room = game_state['current_room']
                if current_room == 'treasure_room':
                    attempt_open_treasure(game_state)
                else:
                    use_item(game_state, argument)
            elif argument:
                use_item(game_state, argument)
            else:
                print("Укажите предмет для использования.")
        case 'solve':
            current_room = game_state['current_room']
            if (
                current_room == 'treasure_room'
                and 'treasure chest' in ROOMS[current_room]['items']
            ):
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)
        case 'quit' | 'exit':
            print("Выход из игры. До свидания!")
            game_state['game_over'] = True
        case 'help':
            show_help(COMMANDS)
        case _:
            print("Неизвестная команда. Введите 'help' для списка команд.")

def main():
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }

    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)

    while not game_state['game_over']:
        command_line = get_input()
        process_command(game_state, command_line)

if __name__ == '__main__':
    main()