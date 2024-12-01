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
    TIMEOUT_SECONDS = 20  # 1.5 минуты
    
    # Образцы задач
    SIMPLE_SAMPLE = [
        [2,7,7,12],
        [2,2,3,8],
        [2,11,11,12],
        [10,10,12,12],
        [1,5,7,12],
        [3,8,13,13],
        [11,11,11,12],
        [2,9,9,12],
        [1,1,5,5],
        [8,8,12,12],
        [9,9,12,12],
        [3,3,12,12]
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
        # Копируем списки для безопасной работы
        simple_tasks = C.SIMPLE_SAMPLE.copy()
        hard_tasks = C.HARD_SAMPLE.copy()
        
        for p in subsession.get_players():
            # Для тренировочного раунда
            practice_task = random.choice(simple_tasks)
            simple_tasks.remove(practice_task)
            
            # Для раундов 2-4 (2 простых, 1 сложное)
            simple_for_early = random.sample(simple_tasks, 2)
            for task in simple_for_early:
                simple_tasks.remove(task)
            hard_for_early = [random.choice(hard_tasks)]
            hard_tasks.remove(hard_for_early[0])
            
            # Для раундов 5-7 (1 простое, 2 сложных)
            simple_for_late = [random.choice(simple_tasks)]
            hard_for_late = random.sample(hard_tasks, 2)
            
            # Формируем последовательность всех раундов
            all_tasks = [practice_task]  # Раунд 1
            
            # Раунды 2-4
            early_tasks = simple_for_early + hard_for_early
            random.shuffle(early_tasks)
            all_tasks.extend(early_tasks)
            
            # Раунды 5-7
            late_tasks = simple_for_late + hard_for_late
            random.shuffle(late_tasks)
            all_tasks.extend(late_tasks)
            
            # Сохраняем в participant.vars
            p.participant.tasks = all_tasks
            print(f"Player {p.id_in_group} tasks:", all_tasks)

    # Устанавливаем задачу для текущего раунда
    for player in subsession.get_players():
        current_task = player.participant.tasks[subsession.round_number - 1]
        player.task_numbers = str(current_task)
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


# PAGES
class calculator(Page):
    form_model = 'player'
    form_fields = ['result']
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def vars_for_template(player):
        if player.task_numbers is None:
            current_task = player.participant.tasks[player.round_number - 1]
            player.task_numbers = str(current_task)
            key = tuple(sorted(current_task))
            player.solution = C.SOLUTIONS.get(key, "No solution available")

        return dict(
            initial_numbers=eval(player.task_numbers),
            solution=player.solution,
            round_type=C.ROUNDS_INDICATION[player.round_number],
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
        if data.get('type') == 'save_time':
            player.participant.vars['time_left'] = data['time_left']
            return


class ReadyPage(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            'round_type': C.ROUNDS_INDICATION[player.round_number]
        }


page_sequence = [ReadyPage, calculator]
