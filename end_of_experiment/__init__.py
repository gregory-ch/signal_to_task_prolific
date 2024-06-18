import numpy as np
import random


from otree.api import *


class C(BaseConstants):
    NAME_IN_URL = 'end_of_experiment'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1



class Subsession(BaseSubsession):
    pass



class Group(BaseGroup):
    pass

class Player(BasePlayer):
    paypal_address = models.StringField(blank=True)
    account_number = models.StringField(blank=True)
    sort_code = models.StringField(blank=True)
    name= models.StringField()


# FUNCTIONS


# PAGES
class Payment(Page):
    form_model = 'player'
    form_fields = [
        'paypal_address', 'account_number','sort_code','name'
    ]

    @staticmethod
    def error_message(player, values):
        if values["paypal_address"] == "" and values["account_number"] == "" and values["sort_code"] == "" :
            return "Please introduce all the details for at least one method of payment"
        elif values["paypal_address"] == "" and (values["account_number"] == "" or values["sort_code"] == ""):
            return "Please  introduce all the details of your bank account"

class Results(Page):
    @staticmethod
    def vars_for_template(player):
        return dict(payoff_GG=player.participant.vars['payoff_GG_2']+player.participant.vars['payoff_GG_1'],
                    payoff_bret=player.participant.vars['payoff_bret'],
                    payoff_market=player.participant.vars['payoff_market'],
                    total_payment=player.participant.vars['payoff_GG_2'] + player.participant.vars['payoff_GG_1'] + player.participant.vars['payoff_bret'] + player.participant.vars['payoff_market'] + player.session.config['participation_fee']
                    )


class End_of_Experiment(Page):
    pass

page_sequence = [Payment, End_of_Experiment]
