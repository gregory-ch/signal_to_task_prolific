from otree.api import *
import random


doc = """
Калькулятор с визуальным интерфейсом для выполнения арифметических операций
с четырьмя числами, включая функции отмены и повтора действий.
"""


class C(BaseConstants):
    NAME_IN_URL = 'calculator'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 12
    # 42 row
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
    # 805 row
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
    SOLUTIONS={
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

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    pass


class Player(BasePlayer):
    result = models.FloatField()
    is_hard = models.BooleanField()
    sample_index = models.IntegerField()
    solution = models.StringField()  # Добавляем поле для хранения решения

# FUNCTIONS
def creating_session(subsession):
    for player in subsession.get_players():
        player.is_hard = random.choice([True, False])
        if player.is_hard:
            player.sample_index = random.randint(0, len(C.HARD_SAMPLE) - 1)
            sample = C.HARD_SAMPLE
        else:
            player.sample_index = random.randint(0, len(C.SIMPLE_SAMPLE) - 1)
            sample = C.SIMPLE_SAMPLE
        
        initial_numbers = sample[player.sample_index]
        key = tuple(sorted(initial_numbers))
        player.solution = C.SOLUTIONS.get(key, "No solution available")

# PAGES
class calculator(Page):
    form_model = 'player'
    form_fields = ['result']

    @staticmethod
    def vars_for_template(player: Player):
        sample = C.HARD_SAMPLE if player.is_hard else C.SIMPLE_SAMPLE
        initial_numbers = sample[player.sample_index]
        return dict(
            initial_numbers=initial_numbers,
            solution=player.solution,
            is_hard='Hard' if player.is_hard else 'Simple'
        )

    @staticmethod
    def js_vars(player: Player):
        sample = C.HARD_SAMPLE if player.is_hard else C.SIMPLE_SAMPLE
        initial_numbers = sample[player.sample_index]
        return dict(
            initial_numbers=initial_numbers,
        )

    @staticmethod
    def live_method(player: Player, data):
        # Этот метод можно использовать для обработки действий в реальном времени
        pass

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Убедимся, что результат сохранен
        if player.result is None:
            player.result = 0  # или любое другое значение по умолчанию

page_sequence = [calculator]
