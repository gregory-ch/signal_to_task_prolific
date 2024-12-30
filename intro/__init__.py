from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'intro'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


def creating_session(subsession):
    for p in subsession.get_players():
        # Randomly assign X (0 or 1) to participant vars to choose app sequence
        p.participant.vars['X'] = random.randint(0, 1)
        p.X = p.participant.vars['X']
        # print(f"Player {p.id_in_group} assigned X = {p.participant.vars['X']}")


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    X = models.FloatField(initial=0)


class Introduction(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(
            X=player.participant.vars['X']
        )
    
    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        if player.participant.vars['X'] == 0:
            return 'dsst_from_scratch'
        else:
            return 'cursor2'


page_sequence = [Introduction]
