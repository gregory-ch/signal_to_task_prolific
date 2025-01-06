from otree.api import *
import random
import time


doc = """
Калькулятор с визуальным интерфейсом для выполнения арифметических операций
с четырьмя числами, включая функции отмены и повтора действий.
"""


class C(BaseConstants):
    NAME_IN_URL = 'calculator'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 7
    DEMO_MODE = False
    TIMEOUT_SECONDS = 90  # 1.5 минуты
    TEST_MODE = 0  # 0 - production mode, 1 - test mode
    
    # Бонусы для разных уровней сложности и временных интервалов
    BONUS_HIGH = {
        30: 0.80,  # до 30 секунд
        60: 0.60,  # до 60 секунд
        90: 0.40   # до 90 секунд
    }
    
    BONUS_LOW = {
        30: 0.40,  # до 30 секунд
        60: 0.30,  # до 60 секунд
        90: 0.20   # до 90 секунд
    }
    
    # Образцы задач
    SIMPLE_SAMPLE = [
        [2,7,7,12],
        [2,2,3,8],
        # [2,11,11,12],
        # [10,10,12,12],
        [1,5,7,12],
        # [3,8,13,13],
        [11,11,11,12],
        # [2,9,9,12],
        [1,1,5,5],
        # [8,8,12,12],
        # [9,9,12,12],
        [1,1,4,5],
        [5,6,12,12]
        # [3,3,12,12]
    ]
    
    HARD_SAMPLE = [
        [6,6,6,12],
        [3,7,8,9],
        [4,4,5,10],
        [6,8,11,13],
        [4,5,10,13],
        [2,2,5,11],
        [2,3,4,11],
        [1,5,10,13],
        [7,12,12,13],
        [2,3,8,12],
        [2,10,11,11],
        [3,4,6,12]
    ]

    SOLUTIONS = {
        (2,7,7,12):"12+7+7-2, 12x2+7-7",
        (2,2,3,8):"8x3+2-2, (8+3)x2+2",
        (2,11,11,12): "12x2+11-11",
        (10,10,12,12): "12+12+10-10",
        (1,5,7,12): "(7-5)x12x1 7x5+1-12",
        (3,8,13,13): '8x3+13-13',
        (11,11,11,12):'(11+11)x12/11, 11/11+12+11',
        (2,9,9,12):'12x2+9-9, 12/2+9+9',
        (1,1,5,5):"(5+1)x(5-1), (5x5-1)x1",
        (8,8,12,12):"12+12+8-8, 12x8/(12-8)",
        (9,9,12,12): "12+12+9-9",
        (1,1,4,5):"(4+1)x5-1",
        (5,6,12,12):'(12+12)x(6-5)',
        (6,6,6,12):'(6+6)x12/6, (6-12/6)x6',
        (3,7,8,9):"(9+7-8)x3",
        (3,3,12,12): "12x12/(3+3), 12+12+3-3, (12-12/3)x3, (12-3)x12/3",
        (4,4,5,10): "(10-5)x4+4, (10/5+4)x4, 10x4-10-4",
        (6,8,11,13):"8x6-13-11, 8x6/(13-11)",
        (4,5,10,13):"13+10+5-4",
        (2,2,5,11):"(11-5)x(2+2), (11-5)x2x2",
        (2,3,4,11):"(11-3-2)x4, (11+4-3)x2",
        (1,5,10,13):"(13-1)x10/5",
        (7,12,12,13): "12x12/(13-7)",
        (2,3,8,12):"(12-8)x3x2, (8-3x2)x12, 8x3/2+12",
        (2,10,11,11):"(11+11-10)x2",
        (3,4,6,12):"12x4x3/6",
    }

    ROUNDS_INDICATION = {1:"t", 2:"s", 3:"s", 4:'s', 5:"h", 6:"h", 7:"h"}


def creating_session(subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            # Создаем копии списков для каждого игрока
            simple_tasks = C.SIMPLE_SAMPLE.copy()
            hard_tasks = C.HARD_SAMPLE.copy()
            
            # Определяем, какой тип задач идет первым
            p.participant.first_set_type = random.choice(['simple', 'hard'])
            
            # Определяем, какую позицию будем менять (0, 1 или 2)
            swap_position = random.randint(0, 2)
            p.participant.swap_position = swap_position  # Сохраняем для последующего использования
            
            # Для тренировочного раунда
            practice_task = random.choice(simple_tasks)
            simple_tasks.remove(practice_task)
            
            # Подготовка задач для первой и второй тройки
            if p.participant.first_set_type == 'simple':
                first_set = random.sample(simple_tasks, 3)
                for task in first_set:
                    simple_tasks.remove(task)
                second_set = random.sample(hard_tasks, 3)
            else:
                first_set = random.sample(hard_tasks, 3)
                for task in first_set:
                    hard_tasks.remove(task)
                second_set = random.sample(simple_tasks, 3)
            
            # Меняем местами элементы на выбранной позиции
            first_set[swap_position], second_set[swap_position] = second_set[swap_position], first_set[swap_position]
            
            # Вычисляем номер раунда, где произошла замена (учитывая тренировочный раунд)
            swapped_round = swap_position + 2  # +2 потому что: +1 для индекса в раунд и +1 для пропуска тренировочного
            second_swapped_round = swap_position + 5  # +5 потому что: +2 для начала второй тройки и +3 для позиции
            
            # Формируем последовательность всех раундов
            all_tasks = [(practice_task, 'training')]  # Раунд 1
            all_tasks.extend((task, p.participant.first_set_type) for task in first_set)  # Раунды 2-4
            all_tasks.extend((task, 'hard' if p.participant.first_set_type == 'simple' else 'simple') for task in second_set)  # Раунды 5-7
            
            # Сохраняем информацию
            p.participant.tasks = all_tasks
            p.participant.swapped_positions = [swapped_round, second_swapped_round]
            # print(f"Player {p.id_in_group} tasks:", all_tasks)
            # print(f"Swapped position {swap_position}, rounds {swapped_round} and {second_swapped_round}")

    # Устанавливаем задачу для текущего раунда
    for player in subsession.get_players():
        current_task, task_type = player.participant.tasks[player.round_number - 1]
        player.task_numbers = str(list(current_task))
        player.task_source = task_type
        player.is_swapped = player.round_number in player.participant.swapped_positions
        player.swap_position = player.participant.swap_position if player.round_number in player.participant.swapped_positions else None
        key = tuple(sorted(current_task))
        player.solution = C.SOLUTIONS.get(key, "No solution available")


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    result = models.FloatField()
    task_numbers = models.StringField()
    solution = models.StringField()
    is_correct = models.BooleanField(initial=False)
    all_used = models.BooleanField(initial=False)
    timeout_happened = models.BooleanField(initial=False)
    solving_time = models.IntegerField()
    task_source = models.StringField()  # 'simple', 'hard', или 'training'
    is_swapped = models.BooleanField()  # был ли этот раунд обменен местами
    swap_position = models.IntegerField(blank=True)  # какая позиция была обменена
    action_history = models.LongStringField(initial='', blank=True)
    bonus = models.FloatField(initial=0)  # бонус за текущий раунд
    total_bonus = models.FloatField(initial=0)  # общий бонус за все раунды





# PAGES
class calculator(Page):
    form_model = 'player'
    form_fields = ['result', 'is_correct', 'all_used', 'solving_time', 'action_history']
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.is_correct = False
            player.all_used = False
            player.result = 0
            player.bonus = 0
        else:
            # Расчет бонуса на основе времени и сложности
            if player.is_correct and player.all_used:
                if player.task_source == 'hard':
                    if player.solving_time <= 30:
                        player.bonus = C.BONUS_HIGH[30]
                    elif player.solving_time <= 60:
                        player.bonus = C.BONUS_HIGH[60]
                    elif player.solving_time <= 90:
                        player.bonus = C.BONUS_HIGH[90]
                    else:
                        player.bonus = 0
                elif player.task_source == 'simple':
                    if player.solving_time <= 30:
                        player.bonus = C.BONUS_LOW[30]
                    elif player.solving_time <= 60:
                        player.bonus = C.BONUS_LOW[60]
                    elif player.solving_time <= 90:
                        player.bonus = C.BONUS_LOW[90]
                    else:
                        player.bonus = 0
                else:  # training
                    player.bonus = 0
            else:
                player.bonus = 0

    @staticmethod
    def vars_for_template(player):
        if player.task_numbers is None:
            current_task, task_type = player.participant.tasks[player.round_number - 1]
            player.task_numbers = str(list(current_task))
            key = tuple(sorted(current_task))
            player.solution = C.SOLUTIONS.get(key, "No solution available")

        # Show difficulty based on actual task type
        difficulty = 'high' if player.task_source == 'hard' else (
            'training' if player.task_source == 'training' else 'low'
        )
        
        return dict(
            initial_numbers=eval(player.task_numbers),
            solution=player.solution,
            round_type=difficulty,
            timeout_seconds=C.TIMEOUT_SECONDS
        )

    @staticmethod
    def js_vars(player):
        if player.task_numbers is None:
            current_task = player.participant.tasks[player.round_number - 1]
            player.task_numbers = str(current_task)

        return dict(
            initial_numbers=eval(player.task_numbers),
            round_number=player.round_number,
            timeout_seconds=C.TIMEOUT_SECONDS
        )

    @staticmethod
    def live_method(player, data):
        data_type = data.get('type')
        
        if data_type == 'save_time':
            player.participant.vars['time_left'] = data['time_left']

    # @staticmethod
    # def before_next_page(player, timeout_happened):
    #     print("Before next page:")
    #     print("is_correct:", player.is_correct)
    #     print("result:", player.result)
    #     print("all_used:", player.all_used)




class ReadyPage(Page):
    @staticmethod
    def vars_for_template(player):
        # Convert new difficulty types to old format for template compatibility
        difficulty_map = {
            'high': 'h',
            'low': 's',
            'training': 't'
        }
        difficulty = 'h' if player.task_source == 'hard' else (
            't' if player.task_source == 'training' else 's'
        )
        return {
            'round_type': difficulty
        }


class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Instructions2(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1  # Показываем только перед вторым раундом


class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def before_next_page(player, timeout_happened):
        # Подсчитываем общий бонус перед переходом на следующую страницу
        all_rounds = player.in_all_rounds()
        total_bonus = sum(round.bonus for round in all_rounds if round.task_source != 'training')
        player.total_bonus = total_bonus

    @staticmethod
    def vars_for_template(player):
        # Собираем данные для отображения
        all_rounds = player.in_all_rounds()
        rounds_data = []
        total_bonus = sum(round.bonus for round in all_rounds if round.task_source != 'training')
        
        for round in all_rounds:
            if round.task_source != 'training':
                round_data = {
                    'round_number': round.round_number,
                    'difficulty': 'High' if round.task_source == 'hard' else 'Low',
                    'time_taken': round.solving_time,
                    'is_correct': round.is_correct,
                    'all_used': round.all_used,
                    'bonus': round.bonus,
                }
                rounds_data.append(round_data)

        return {
            'rounds_data': rounds_data,
            'total_bonus': total_bonus  # Используем только что подсчитанное значение
        }

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars['X'] == 0:
            return 'end'
        else:
            return 'dsst_from_scratch2'

page_sequence = [Instructions, Instructions2, ReadyPage, calculator, Results]
