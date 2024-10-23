from otree.api import *

doc = """
DSST (Digit Symbol Substitution Test) project
"""

class Constants(BaseConstants):
    name_in_url = 'dsst'
    players_per_group = None
    num_rounds = 1
    block_duration = 10000  # 90 секунд в миллисекундах
    waiting_time = 10  # 10 секунд для waiting page

class Player(BasePlayer):
    experiment_data = models.LongStringField()
    score = models.IntegerField(initial=0)
    total_trials = models.IntegerField(initial=0)
    incorrect_key_presses = models.IntegerField(initial=0)

class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass

# PAGES
class Instructions(Page):
    @staticmethod
    def vars_for_template(player):
        return {
            'img_files': [
                '/static/dsst-t/img/circle.png',
                '/static/dsst-t/img/square.png',
                '/static/dsst-t/img/triangle.png',
            ]
        }

    @staticmethod
    def js_vars(player: Player):
        return {
            'img_files': [
                '/static/dsst-t/img/circle.png',
                '/static/dsst-t/img/square.png',
                '/static/dsst-t/img/triangle.png',
            ]
        }

class Practice(Page):
    @staticmethod
    def js_vars(player: Player):
        return {
            'img_files': [
                '/static/dsst-t/img/circle.png',
                '/static/dsst-t/img/square.png',
                '/static/dsst-t/img/triangle.png',
            ]
        }

class Block1(Page):
    @staticmethod
    def js_vars(player: Player):
        return {
            'img_files': [
                '/static/dsst-t/img/asterisk.png',
                '/static/dsst-t/img/bracket.png',
                '/static/dsst-t/img/record.png',
            ],
            'block_duration': Constants.block_duration
        }

    @staticmethod
    def get_timeout_seconds(player):
        return Constants.block_duration / 1000  # Преобразуем миллисекунды в секунды

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print("Block 1 timed out")

    @staticmethod
    def live_method(player: Player, data):
        print("Received data for Block 1:", data)
        if data['action'] == 'save_data':
            player.experiment_data = data['data']
            player.total_trials = int(data['trials'])
            player.score = int(data['score'])
            player.incorrect_key_presses = int(data['incorrect_key_presses'])
        return {player.id_in_group: 'data_received'}

class WaitForBots(Page):
    """
    This is just for show, to make it feel more realistic.
    Also, note it's a Page, not a WaitPage.
    Removing this page won't affect functionality.
    """

    @staticmethod
    def get_timeout_seconds(player: Player):
        return Constants.waiting_time

class Block2(Page):
    @staticmethod
    def js_vars(player: Player):
        return {
            'img_files': [
                '/static/dsst-t/img/squiggles.png',
                '/static/dsst-t/img/corner.png',
                '/static/dsst-t/img/dots.png',
            ],
            'block_duration': Constants.block_duration
        }

    @staticmethod
    def get_timeout_seconds(player):
        return Constants.block_duration / 1000

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print("Block 2 timed out")

    @staticmethod
    def live_method(player: Player, data):
        print("Received data for Block 2:", data)
        if data['action'] == 'save_data':
            player.experiment_data += data['data']
            player.total_trials += int(data['trials'])
            player.score += int(data['score'])
            player.incorrect_key_presses += int(data['incorrect_key_presses'])
            print(f"Updated player data: trials={player.total_trials}, score={player.score}, incorrect_key_presses={player.incorrect_key_presses}")
        return {player.id_in_group: 'data_received'}



class Block3(Page):
    @staticmethod
    def js_vars(player: Player):
        return {
            'img_files': [
                '/static/dsst-t/img/epsilon.png',
                '/static/dsst-t/img/ring.png',
                '/static/dsst-t/img/diamond.png',
            ],
            'block_duration': Constants.block_duration
        }

    @staticmethod
    def get_timeout_seconds(player):
        return Constants.block_duration / 1000

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print("Block 3 timed out")

    @staticmethod
    def live_method(player: Player, data):
        print("Received data for Block 3:", data)
        if data['action'] == 'save_data':
            player.experiment_data += data['data']
            player.total_trials += int(data['trials'])
            player.score += int(data['score'])
            player.incorrect_key_presses += int(data['incorrect_key_presses'])
        return {player.id_in_group: 'data_received'}

class Finished(Page):
    pass

page_sequence = [Instructions, Practice, Block1, Finished]

# # Общий live_method для всех страниц
# def live_method(player: Player, data):
#     if data['action'] == 'save_data':
#         player.experiment_data += data['data']
#         player.total_trials += int(data['trials'])
#         player.score += int(data['score'])
#         player.incorrect_key_presses += int(data['incorrect_key_presses'])
#     return {player.id_in_group: 'data_received'}

# # Добавляем live_method ко всем страницам
# for page in page_sequence:
#     if not hasattr(page, 'live_method'):
#         page.live_method = live_method



# похоже что он удваивает счетчики каждый раз, легче всего переписать для одного блока всё
