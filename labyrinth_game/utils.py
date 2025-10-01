
from constants import ROOMS


def describe_current_room(game_state):
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


def solve_puzzle(game_state):
    current_room = game_state['current_room']
    room = ROOMS[current_room]
    if room['puzzle'] is None:
        print("Загадок здесь нет.")
        return
    question, answer = room['puzzle']
    print(question)
    user_answer = input("Ваш ответ: ").strip().lower()
    if user_answer == answer.lower():
        print("Правильно! Загадка решена.")
        room['puzzle'] = None
        if current_room == 'library':
            game_state['player_inventory'].append('magic key')
            print("Вы получили магический ключ!")
    else:
        print("Неверно. Попробуйте снова.")


def show_help():
    print("Команды игры:")
    print("  go [направление] - переместиться")
    print("  look - осмотреться")
    print("  take [предмет] - взять предмет")
    print("  use [предмет] - использовать предмет")
    print("  inventory - показать инвентарь")
    print("  solve - решить загадку")
    print("  quit - выйти из игры")


def attempt_open_treasure(game_state):
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
            if code_input == correct_code:
                print("Код верный. Сундук открыт!")
                room['items'].remove('treasure chest')
                print("В сундуке сокровище! Вы победили!")
                game_state['game_over'] = True
            else:
                print("Неверный код.")
        else:
            print("Вы отступаете от сундука.")

