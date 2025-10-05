from .constants import ROOMS
from .utils import describe_current_room, random_event


def show_inventory(game_state):
    """Показывает содержимое инвентаря игрока."""
    inventory = game_state['player_inventory']
    if inventory:
        print("В вашем инвентаре:", ', '.join(inventory))
    else:
        print("Инвентарь пуст.")

def get_input(prompt="> "):
    """Получает ввод пользователя, безопасно завершает игру /
    при EOF/KeyboardInterrupt."""
    try:
        return input(prompt)
    except (KeyboardInterrupt, EOFError):
        print("Выход из игры.")
        return "quit"

def move_player(game_state, direction):
    """
    Перемещает игрока в указанном направлении, 
    если выход существует и соответствует условиям (например, необходим ключ).
    Также после перемещения может сработать случайное событие.
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    exits = room['exits']
    if direction in exits:
        new_room = exits[direction]
        if new_room == 'treasure_room':
            if 'treasure_key' in game_state['player_inventory']:
                print(
                    "Вы используете найденный ключ, "
                    "чтобы открыть путь в комнату сокровищ."
                )
                game_state['current_room'] = new_room
            else:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
                return
        else:
            game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        describe_current_room(game_state)
        random_event(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    """Добавляет предмет из текущей комнаты в инвентарь игрока, если предмет есть."""
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    if item_name in room['items']:
        room['items'].remove(item_name)
        game_state['player_inventory'].append(item_name)
        print(f"Вы подняли: {item_name}")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    """
    Использует предмет из инвентаря игрока,
    реализует специальные эффекты для отдельных предметов.
    """
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