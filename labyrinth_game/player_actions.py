
from constants import ROOMS
from utils import describe_current_room


def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("В вашем инвентаре:", ', '.join(inventory))
    else:
        print("Инвентарь пуст.")


def get_input(prompt="> "):
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("Выход из игры.")
        return "quit"


def move_player(game_state, direction):
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    exits = room['exits']
    if direction in exits:
        new_room = exits[direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")


def take_item(game_state, item_name):
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    if item_name in room['items']:
        room['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")


def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return

    if item_name == 'torch':
        print("Вы зажгли факел. Стало светлее.")
    elif item_name == 'sword':
        print("Вы уверенно держите меч в руках.")
    elif item_name == 'bronze box':
        print("Вы открываете бронзовую шкатулку.")
        if 'rusty key' not in game_state['player_inventory']:
            game_state['player_inventory'].append('rusty key')
            print("В шкатулке вы нашли ржавый ключ.")
        else:
            print("Шкатулка пуста.")
    else:
        print("Вы не знаете, как использовать этот предмет.")
