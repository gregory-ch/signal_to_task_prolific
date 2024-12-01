from otree.api import *
import random


doc = """
DSST (Digit Symbol Substitution Test) - a cognitive task where participants match symbols with corresponding numbers.
"""


class C(BaseConstants):
    NAME_IN_URL = 'dsst_from_scratch'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 7
    OPTIONS = [1, 2, 3]
    NUM_TRIALS_MAX = 100
    TIMEOUT_SECONDS = 30

    # Define symbol sets
    BASIC_SYMBOLS = ['circle', 'square', 'triangle']
    
    SIMPLE_SETS = [
        ('true_simple_1', 'true_simple_2', 'true_simple_3'),
        ('true_simple_1_1', 'true_simple_2_2', 'true_simple_3_3'),
        ('false_simple_1', 'false_simple_2', 'false_simple_3')
    ]
    
    COMPLEX_SETS = [
        ('true_complex_1', 'true_complex_2', 'true_complex_3'),
        ('true_complex_1_1', 'true_complex_2_2', 'true_complex_3_3'),
        ('false_complex_1', 'false_complex_2', 'false_complex_3')
    ]
    ROUNDS_INDICATION = {1:"t", 2: "s", 3: "s", 4:'s', 5:"c", 6:"c", 7:"c"}


def creating_session(subsession):
    if subsession.round_number == 1:
        # Создаем копии списков перед модификацией
        simple_sets = [list(x) for x in C.SIMPLE_SETS.copy()]
        random.shuffle(simple_sets)
        
        complex_sets = [list(x) for x in C.COMPLEX_SETS.copy()]
        random.shuffle(complex_sets)
        
        # Создаем копию базовых символов
        basic_symbols = list(C.BASIC_SYMBOLS)
        
        # Combine all sets in order
        all_sets = [basic_symbols] + simple_sets + complex_sets
        
        # Сохраняем в participant.symbol_sets для всех игроков
        for p in subsession.get_players():
            p.participant.symbol_sets = all_sets

    for player in subsession.get_players():
        # Get the symbol set for this round from participant.symbol_sets
        current_symbols = player.participant.symbol_sets[subsession.round_number - 1]
        
        # Создаем trials явно
        trials = []
        for i in range(C.NUM_TRIALS_MAX):
            trial_num = i + 1
            draw = random.choice(C.OPTIONS)
            trials.append((trial_num, draw))
        
        # Сохраняем и проверяем
        player.trials_sequence = str(trials)
        player.current_trial = 1
        player.wrong_attempts = str({})
        player.total_trials_completed = 0
        player.total_wrong_attempts = 0
        player.symbol_names = str(current_symbols)


def get_current_symbol(player):
    if player.trials_sequence is None:
        trials = []
        for i in range(C.NUM_TRIALS_MAX):
            trial_num = i + 1
            draw = random.choice(C.OPTIONS)
            trials.append((trial_num, draw))
        player.trials_sequence = str(trials)
        player.current_trial = 1
        player.wrong_attempts = str({})
    
    trials = eval(player.trials_sequence)
    for trial_num, draw in trials:
        if trial_num == player.current_trial:
            return draw
    return random.choice(C.OPTIONS)


def get_symbol_name(player, number):
    if not player.symbol_names:
        if player.round_number == 1:
            player.symbol_names = str(C.BASIC_SYMBOLS)
        else:
            current_symbols = player.participant.symbol_sets[player.round_number - 1]
            player.symbol_names = str(current_symbols)
    
    symbols = eval(player.symbol_names)
    if 1 <= number <= len(symbols):
        return symbols[number - 1]
    return None


def increment_wrong_attempts(player):
    attempts = eval(player.wrong_attempts or '{}')
    current = str(player.current_trial)
    attempts[current] = attempts.get(current, 0) + 1
    player.wrong_attempts = str(attempts)
    player.total_wrong_attempts += 1


def next_trial(player):
    if player.current_trial < C.NUM_TRIALS_MAX:
        player.current_trial += 1
        player.total_trials_completed = player.current_trial - 1
        return True
    return False


class Subsession(BaseSubsession):
    symbol_set_order = models.StringField()


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    trials_sequence = models.StringField()
    current_trial = models.IntegerField(initial=1)
    wrong_attempts = models.StringField(initial='{}')
    total_trials_completed = models.IntegerField(initial=0)
    total_wrong_attempts = models.IntegerField(initial=0)
    symbol_names = models.StringField()


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Instructions2(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class ReadyPage(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            'round_type': C.ROUNDS_INDICATION[player.round_number]
        }


class TaskPage(Page):
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def vars_for_template(player):
        symbols = eval(player.symbol_names)
        return {
            'symbol_paths': [f"dsst-t/img/{symbol}.png" for symbol in symbols],
            'round_type': C.ROUNDS_INDICATION[player.round_number]
        }

    @staticmethod
    def js_vars(player):
        current_symbol = get_current_symbol(player)
        if current_symbol is None:
            current_symbol = random.choice(C.OPTIONS)
        symbols = eval(player.symbol_names)
        return {
            'current_symbol': current_symbol,
            'current_trial': player.current_trial,
            'timeout_seconds': C.TIMEOUT_SECONDS,
            'total_wrong_attempts': player.total_wrong_attempts,
            'symbol_paths': [f"/static/dsst-t/img/{symbol}.png" for symbol in symbols],
        }

    @staticmethod
    def live_method(player, data):
        if data.get('type') == 'timeout':
            player.total_trials_completed = player.current_trial - 1
            return {
                player.id_in_group: {
                    'status': 'finished',
                    'total_wrong_attempts': player.total_wrong_attempts
                }
            }
            
        if 'pressed_key' in data:
            pressed_key = int(data['pressed_key'])
            current_symbol = get_current_symbol(player)
            
            if pressed_key == current_symbol:
                if next_trial(player):
                    next_symbol = get_current_symbol(player)
                    return {
                        player.id_in_group: {
                            'current_symbol': next_symbol,
                            'current_trial': player.current_trial,
                            'status': 'next',
                            'total_wrong_attempts': player.total_wrong_attempts,
                            'symbol_path': f"/static/dsst-t/img/{get_symbol_name(player, next_symbol)}.png"
                        }
                    }
                else:
                    return {
                        player.id_in_group: {
                            'status': 'finished',
                            'total_wrong_attempts': player.total_wrong_attempts
                        }
                    }
            else:
                increment_wrong_attempts(player)
                return {
                    player.id_in_group: {
                        'status': 'wrong',
                        'total_wrong_attempts': player.total_wrong_attempts
                    }
                }


page_sequence = [Instructions, Instructions2, ReadyPage, TaskPage]
