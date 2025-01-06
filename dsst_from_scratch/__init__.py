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
    NUM_TRIALS_MAX = 150
    TIMEOUT_SECONDS = 30
    TEST_MODE = 0  # 0 - production mode, 1 - test mode
    
    # Bonus amounts
    BONUS_HIGH = 0.60
    BONUS_LOW = 0.40

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

    # Пороги для компьютера
    COMPUTER_THRESHOLD_MIN = 0
    COMPUTER_THRESHOLD_MAX = 40


def creating_session(subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            p.participant.first_set_type = random.choice(['simple', 'complex'])
            
            # Create deep copies of the sets
            simple_sets = [list(set_tuple) for set_tuple in C.SIMPLE_SETS]
            complex_sets = [list(set_tuple) for set_tuple in C.COMPLEX_SETS]
            basic_symbols = list(C.BASIC_SYMBOLS)
            
            # Shuffle the copies
            random.shuffle(simple_sets)
            random.shuffle(complex_sets)
            
            # Swap first elements between simple and complex sets
            simple_sets[0], complex_sets[0] = complex_sets[0], simple_sets[0]
            
            # Calculate actual positions of swapped elements after arrangement
            if p.participant.first_set_type == 'simple':
                swapped_positions = [2, 5]  # Adjusted for training round: 2 (first after training) and 5 (first of complex)
                all_sets = [basic_symbols] + simple_sets + complex_sets
                set_types = ['training'] + ['simple'] * 3 + ['complex'] * 3
            else:
                swapped_positions = [2, 5]  # Same positions but different set types
                all_sets = [basic_symbols] + complex_sets + simple_sets
                set_types = ['training'] + ['complex'] * 3 + ['simple'] * 3
            
            # Store information
            p.participant.symbol_sets = all_sets
            p.participant.set_types = set_types
            p.participant.swapped_positions = swapped_positions

    # Set up each player's round
    for player in subsession.get_players():
        current_symbols = player.participant.symbol_sets[player.round_number - 1]
        player.set_type = player.participant.set_types[player.round_number - 1]
        # Now this correctly identifies swapped sets
        player.is_swapped = player.round_number in player.participant.swapped_positions
        
        # Generate trials without consecutive repetitions
        trials = []
        last_draw = None
        for i in range(C.NUM_TRIALS_MAX):
            trial_num = i + 1
            available_options = [opt for opt in C.OPTIONS if opt != last_draw]
            draw = random.choice(available_options)
            last_draw = draw
            trials.append((trial_num, draw))
        
        # Save the generated sequence
        player.trials_sequence = str(trials)
        player.current_trial = 1
        player.wrong_attempts = str({})
        player.total_trials_completed = 0
        player.total_wrong_attempts = 0
        player.symbol_names = str(current_symbols)
        
        # Add computer's random choice
        player.computer_threshold = random.randint(C.COMPUTER_THRESHOLD_MIN, C.COMPUTER_THRESHOLD_MAX)



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
    set_type = models.StringField()  # 'simple' or 'complex'
    is_swapped = models.BooleanField()  # whether this round's symbol was swapped
    computer_threshold = models.IntegerField()  # Random number chosen by computer
    bonus = models.FloatField(initial=0)  # Bonus earned in this round
    total_bonus = models.FloatField(initial=0)  # Total bonus across all rounds


# PAGES
class Instructions(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1


class Instructions2(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player):
        return {
            'bonus_high': C.BONUS_HIGH,
            'bonus_low': C.BONUS_LOW
        }


class ReadyPage(Page):
    @staticmethod
    def vars_for_template(player):
        # Show difficulty based on actual set type rather than fixed rounds
        difficulty = 'high' if player.set_type == 'complex' else (
            'training' if player.set_type == 'training' else 'low'
        )
        return {
            'round_type': difficulty
        }


class TaskPage(Page):
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def vars_for_template(player):
        symbols = eval(player.symbol_names)
        # Show difficulty based on actual set type rather than fixed rounds
        difficulty = 'high' if player.set_type == 'complex' else (
            'training' if player.set_type == 'training' else 'low'
        )
        return {
            'symbol_paths': [f"dsst-t/img/{symbol}.png" for symbol in symbols],
            'round_type': difficulty
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
            'round_number': player.round_number,
            'computer_threshold': player.computer_threshold,
            'num_rounds': C.NUM_ROUNDS
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

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.total_wrong_attempts >= 5:
            player.bonus = 0
        else:
            effective_score = player.total_trials_completed - player.total_wrong_attempts
            if effective_score > player.computer_threshold:
                if player.set_type == 'complex':
                    player.bonus = C.BONUS_HIGH
                elif player.set_type == 'simple':
                    player.bonus = C.BONUS_LOW
                else:  # training round
                    player.bonus = 0
            else:
                player.bonus = 0
        
        player.computer_threshold = random.randint(C.COMPUTER_THRESHOLD_MIN, C.COMPUTER_THRESHOLD_MAX)




class Results(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS
    
    @staticmethod
    def vars_for_template(player):
        all_rounds = player.in_all_rounds()
        rounds_data = []
        total_bonus = 0
        
        for round in all_rounds:
            if round.set_type != 'training':  # Пропускаем тренировочный раунд
                round_data = {
                    'round_number': round.round_number,
                    'difficulty': 'High' if round.set_type == 'complex' else 'Low',
                    'correct_matches': round.total_trials_completed,
                    'wrong_attempts': round.total_wrong_attempts,
                    'effective_score': round.total_trials_completed - round.total_wrong_attempts,
                    'computer_threshold': round.computer_threshold,
                    'bonus': round.bonus,
                }
                rounds_data.append(round_data)
                total_bonus += round.bonus

        return {
            'rounds_data': rounds_data,
            'total_bonus': total_bonus,
            'bonus_high': C.BONUS_HIGH,
            'bonus_low': C.BONUS_LOW
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # Вычисляем и сохраняем total_bonus
        all_rounds = player.in_all_rounds()
        total_bonus = sum(round.bonus for round in all_rounds if round.set_type != 'training')
        player.total_bonus = total_bonus


page_sequence = [Instructions, Instructions2, ReadyPage, TaskPage, Results]
