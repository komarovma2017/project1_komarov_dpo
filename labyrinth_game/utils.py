import math

from .constants import COMMANDS, ROOMS


def pseudo_random(seed, modulo):
    """
    Возвращает псевдослучайное целое в диапазоне [0, modulo) 
    на основе математической формулы с синусом.
    """
    x = math.sin(seed * 12.9898) * 43758.5453
    fract = x - math.floor(x)
    return int(fract * modulo)

def trigger_trap(game_state):
    """
    Активирует ловушку: теряется случайный предмет или с шансом закончится игра.
    """
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        idx = pseudo_random(game_state['steps_taken'], len(inventory))
        lost = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost}!")
    else:
        dmg = pseudo_random(game_state['steps_taken'], 10)
        if dmg < 3:
            print("Вы не выдержали ловушку и погибаете...")
            game_state['game_over'] = True
        else:
            print("Вам повезло, вы пережили ловушку!")

def random_event(game_state):
    """
    Выполняет небольшое случайное событие после перемещения игрока:
    находка, испуг, ловушка (в trap_room без факела).
    """
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        event = pseudo_random(game_state['steps_taken'] + 1, 3)
        room = ROOMS[game_state['current_room']]
        if event == 0:
            print("Вы находите на полу монетку!")
            room['items'].append('coin')
        elif event == 1:
            print("Вы слышите мистический шорох в темноте.")
            if 'sword' in game_state['player_inventory']:
                print("Вы нервно сжимаете меч. Существо в панике убегает.")
        elif (
            event == 2
            and game_state['current_room'] == 'trap_room'
            and 'torch' not in game_state['player_inventory']
        ):
            print("Вы вдруг чувствуете опасность в темной комнате!")
            trigger_trap(game_state)

def describe_current_room(game_state):
    """
    Выводит описание текущей комнаты, список предметов и возможные выходы.
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    print(f"== {current_room.upper()} ==")
    print(room['description'])
    if room['items']:
        print("Заметные предметы:", ', '.join(room['items']))
    else:
        print("Заметные предметы отсутствуют.")
    print("Выходы:", ', '.join(room['exits'].keys()))
    if room['puzzle'] is not None:
        print("Кажется, здесь есть загадка (используйте команду solve).")

def show_help(command_dict=COMMANDS):
    """
    Выводит справку по возможным командам игры с коротким описанием для каждой.
    """
    print("Команды игры:")
    for cmd, desc in command_dict.items():
        print(f"{cmd.ljust(16)} — {desc}")

def solve_puzzle(game_state):
    """
    Позволяет решить загадку в текущей комнате; награда зависит от комнаты.
    Некоторые загадки допускают альтернативные верные варианты ответа.
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    question, answer = room['puzzle']
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()
    alternatives = { '10': ['десять'], 'резонанс': [] }
    valid = [answer.lower()]
    if answer.lower() in alternatives:
        valid += alternatives[answer.lower()]
    if user_answer in valid:
        print("Правильно! Загадка решена.")
        room['puzzle'] = None
        if current_room == 'library':
            game_state['player_inventory'].append('rusty key')
            print("Вы получили ржавый ключ!")
        elif current_room == 'hall':
            game_state['player_inventory'].append('treasure_key')
            print("Вы получили ключ от сокровищницы!")
    elif current_room == 'trap_room':
        trigger_trap(game_state)
    else:
        print("Неверно. Попробуйте снова.")

def attempt_open_treasure(game_state):
    """
    Реализует попытку открыть сундук в комнате сокровищ.
    Учитывает наличие ключей и возможность ввода кода.
    """
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    if 'treasure chest' not in room['items']:
        print("Сундук уже открыт или отсутствует.")
        return

    has_rusty_key = 'rusty key' in game_state['player_inventory']
    has_treasure_key = 'treasure_key' in game_state['player_inventory']

    if has_treasure_key or has_rusty_key:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        room['items'].remove('treasure chest')
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
    else:
        user_choice = input("Сундук заперт. У вас нет ключа. " \
        "Ввести код? (да/нет) ").strip().lower()
        if user_choice == 'да':
            code_input = input("Введите код: ").strip()
            correct_code = None
            if room['puzzle'] is not None:
                _, correct_code = room['puzzle']
            if code_input == correct_code or code_input == 'десять':
                print("Код верный. Сундук открыт!")
                room['items'].remove('treasure chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")