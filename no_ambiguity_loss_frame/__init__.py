from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'no_ambiguity_loss_frame'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    invest = models.BooleanField(
        widget=widgets.RadioSelect,
        choices=[
            [False, 'No'],
            [True, 'Yes']
        ]
    )
    refund = models.BooleanField()
    outcome = models.BooleanField()
    second_outcome = models.BooleanField()
    second_invest = models.IntegerField()


# PAGES
class Instructions(Page):
    def is_displayed(player):
        return player.participant.treatment == 1

    def before_next_page(player, timeout_happened):
        n = random.randint(1, 100)
        if n <= 50:
            player.refund = True
        else:
            player.refund = False

    form_model = 'player'
    form_fields = ['invest']


class Refund(Page):
    def is_displayed(player):
        return player.participant.treatment == 1

    @staticmethod
    def vars_for_template(player):
        if player.refund:
            ws = "was"
            wl = "will not"
            wd = "would"
            wdn = "would not"
        else:
            ws = "was not"
            wl = "will"
            wd = "would not"
            wdn = "would"
        
        return dict(
            ws=ws,
            wl=wl,
            wd=wd,
            wdn=wdn
        )


class Outcome(Page):
    def is_displayed(player):
        return player.participant.treatment == 1

    @staticmethod
    def vars_for_template(player):
        if player.invest:
            invest = 1
        else:
            invest = 0
        return dict(
            invest=invest
        )

    def before_next_page(player, timeout_happened):
        tokens = 200
        if player.invest:
            if not player.refund:
                tokens -= 100
            if player.outcome:
                tokens += 8 * 100

        player.participant.payoff += tokens / 500

    form_model = 'player'
    form_fields = ['outcome']


class SecondOutcome(Page):
    def is_displayed(player):
        return player.participant.treatment == 1

    def before_next_page(player, timeout_happened):
        tokens = 200
        tokens -= player.second_invest
        if player.second_outcome:
            tokens += 8 * player.second_invest

        player.participant.payoff += tokens / 500
    
    form_model = 'player'
    form_fields = ['second_outcome']


class SecondInvest(Page):
    def is_displayed(player):
        return player.participant.treatment == 1

    form_model = 'player'
    form_fields = ['second_invest']


class End(Page):
    def is_displayed(player):
        return player.participant.treatment == 1
    
    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finished = True

    def vars_for_template(player):
        return dict(
            pay = "$"+str(round(player.participant.payoff, 2))
        )

class ThankYou(Page):
    def is_displayed(player):
        return player.participant.treatment == 1

page_sequence = [Instructions, Refund, Outcome, SecondInvest, SecondOutcome, End, ThankYou]
