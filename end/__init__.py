from otree.api import *
import numpy as np
import random
import operator


doc = """
End page with redirections
"""



class C(BaseConstants):
    NAME_IN_URL = 'end'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    participation_fee = models.CurrencyField()
    prolific_id = models.StringField(default=str(" "))
    
    # Survey fields
    validation_word = models.StringField(
        label="Please type the word 'validated' below to confirm you are a human participant:",
        blank=False
    )
    
    age = models.IntegerField(
        label="What is your age?",
        min=18,
        max=100,
        blank=False
    )
    
    gender = models.StringField(
        label="What is your gender?",
        choices=[
            'Male',
            'Female',
            'Other',
            'Prefer not to say'
        ],
        blank=False
    )
    
    feedback = models.LongStringField(
        label="Please share any feedback about the tasks or describe the strategies you used (optional):",
        blank=True
    )

class Survey(Page):
    form_model = 'player'
    form_fields = ['validation_word', 'age', 'gender', 'feedback']

    @staticmethod
    def error_message(player, values):
        if values['validation_word'].lower() != 'validated':
            return 'Please type exactly the word "validated" to proceed'

# PAGES

# class WaitPageResults(WaitPage):
#     title_text = "Please Wait"
#     body_text = "Please wait while everyone finishes the experiment."
#     @staticmethod
#     def is_displayed(player):
#         return player.session.config['context'] == 'lab'

# class EndOfExperiment(Page):
#     @staticmethod
#     def vars_for_template(player):
#         return dict(
#             context=player.session.config['context']
#         )
#     @staticmethod
#     def is_displayed(player):
#         return (
#             player.round_number == C.NUM_ROUNDS and
#                 player.session.config['context'] == "lab" and
#                 not player.participant.vars.get('failed_captcha', False)
        # )

# next_app/pages.py
class PayoffCalculationPage(Page):
    form_model = 'player'
    timeout_seconds = 1  #
    auto_submit = True   # 

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.prolific_id = player.participant.label



        

class RedirectProlific(Page):
        @staticmethod
        def is_displayed(player):
            return (
                player.round_number == C.NUM_ROUNDS and
                player.session.config['context'] == "prolific" 
            )
# and not player.participant.vars.get('failed_captcha', False)
        @staticmethod
        def js_vars(player):
            return dict(
                completionlink=
                player.subsession.session.config['completionlink']
            )


    
page_sequence = [
    Survey,
    PayoffCalculationPage,
    RedirectProlific,
    # EndOfExperiment
]
