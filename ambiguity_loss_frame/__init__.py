from otree.api import *
import random


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'ambiguity_loss_frame'
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
    m = models.FloatField()
    guess = models.IntegerField(
        label="Your guess:",
        min=0,
        max=100
    )


# PAGES
class Instructions(Page):
    def is_displayed(player):
        return player.participant.treatment == 3
    
    def before_next_page(player, timeout_happened):
        n = random.randint(1, 100)
        if n <= 50:
            player.refund = True
        else:
            player.refund = False

    form_model = 'player'
    form_fields = ['invest', 'm']



class Refund(Page):
    def is_displayed(player):
        return player.participant.treatment == 3

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
        return player.participant.treatment == 3

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
                tokens += player.m * 100

        player.participant.payoff += tokens / 500

    form_model = 'player'
    form_fields = ['outcome']


class SecondOutcome(Page):
    def is_displayed(player):
        return player.participant.treatment == 3

    def before_next_page(player, timeout_happened):
        tokens = 200
        tokens -= player.second_invest
        if player.second_outcome:
            tokens += player.m * player.second_invest

        player.participant.payoff += tokens / 500
    
    form_model = 'player'
    form_fields = ['second_outcome']


class SecondInvest(Page):
    def is_displayed(player):
        return player.participant.treatment == 3

    form_model = 'player'
    form_fields = ['second_invest']


class Guess(Page):
    def is_displayed(player):
        return player.participant.treatment == 3

    def before_next_page(player, timeout_happened):
        if player.guess in [78, 79, 80, 81, 82]:
            player.participant.payoff += 0.25

    form_model = 'player'
    form_fields = ['guess']


class End(Page):
    def is_displayed(player):
        return player.participant.treatment == 3

    def vars_for_template(player):
        return dict(
            pay = "$"+str(round(player.participant.payoff, 2))
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.participant.finished = True


class ThankYou(Page):
    def is_displayed(player):
        return player.participant.treatment == 3

page_sequence = [Instructions, Refund, Outcome, SecondInvest, SecondOutcome, Guess, End, ThankYou]
