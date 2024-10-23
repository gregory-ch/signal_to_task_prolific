from otree.api import *

doc = """
DSST (Digit Symbol Substitution Test) project
"""

class Constants(BaseConstants):
    name_in_url = 'dsst'
    players_per_group = None
    num_rounds = 1
    block_duration = 10000  # 90 секунд в миллисекундах

class Player(BasePlayer):
    experiment_data = models.LongStringField()
    score = models.IntegerField(initial=0)
    total_trials = models.IntegerField(initial=0)

class Group(BaseGroup):
    pass

class Subsession(BaseSubsession):
    pass

# PAGES
class Instructions(Page):
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
    def live_method(player: Player, data):
        print("Received data:", data)  # Добавим это для отладки
        if data['action'] == 'save_data':
            player.experiment_data = data['data']
            player.total_trials = int(data['trials'])
            player.score = int(data['score'])
            print(f"Saved data: trials={player.total_trials}, score={player.score}")  # И это
        return {player.id_in_group: 'data_received'}

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
    def live_method(player: Player, data):
        if data['action'] == 'save_data':
            player.experiment_data += data['data']
            player.total_trials += int(data['trials'])
            player.score += int(data['score'])
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
    def live_method(player: Player, data):
        if data['action'] == 'save_data':
            player.experiment_data += data['data']
            player.total_trials += int(data['trials'])
            player.score += int(data['score'])
        return {player.id_in_group: 'data_received'}

class Finished(Page):
    pass

page_sequence = [Instructions, Practice, Block1, Block2, Finished]

# Общий live_method для всех страниц
def live_method(player: Player, data):
    if data['action'] == 'save_data':
        player.experiment_data += data['data']
        player.total_trials += int(data['trials'])
        player.score += int(data['score'])
    return {player.id_in_group: 'data_received'}

# Добавляем live_method ко всем страницам
for page in page_sequence:
    if not hasattr(page, 'live_method'):
        page.live_method = live_method
