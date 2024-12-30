from otree.api import Currency as c, currency_range, expect, Bot, SubmissionMustFail
from . import *
import random


class PlayerBot(Bot):
    def play_round(self):
        if self.round_number == 1:
            yield Submission(EndOfExperiment, check_html = False)
        