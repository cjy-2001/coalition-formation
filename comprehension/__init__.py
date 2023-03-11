from otree.api import *


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'comprehension'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    Q1 = models.BooleanField(
        widget=widgets.RadioSelect,
        choices=[
            [False, 'Just the left third.'],
            [True, 'Just the middle third.'],
            [False, 'Just the right third.'],
            [False, 'Any third of the screen.']
        ]
    )
    Q2 = models.BooleanField(
        widget=widgets.RadioSelect,
        choices=[
            [False, '50 for Representative A and 50 for myself.'],
            [False, '35 for Representative A and 35 for myself.'],
            [True, '45 for Representative A and 45 for myself.']
        ])
    Q3 = models.BooleanField(
        widget=widgets.RadioSelect,
        choices=[
            [False, '20'],
            [False, '70'],
            [True, '80'],
            [False, '90'],
            [False, '100']
        ])
    Q4 = models.BooleanField()


# PAGES
class Welcome(Page):
    pass


class CompQuestions(Page):
    def is_displayed(player):
        return not all([
            player.field_maybe_none('Q1'), 
            player.field_maybe_none('Q2'), 
            player.field_maybe_none('Q3'), 
            player.field_maybe_none('Q4')
        ])

    def before_next_page(player, timeout_happened):
        if not all([player.field_maybe_none('Q1'), player.field_maybe_none('Q2'), player.field_maybe_none('Q3'), player.field_maybe_none('Q4')]):
            player.Q1 = None
            player.Q2 = None
            player.Q3 = None
            player.Q4 = None


    form_model = 'player'
    form_fields = ['Q1', 'Q2', 'Q3', 'Q4']


class WrongAnswers(Page):
    def is_displayed(player):
        return not all([
            player.field_maybe_none('Q1'), 
            player.field_maybe_none('Q2'), 
            player.field_maybe_none('Q3'), 
            player.field_maybe_none('Q4')
        ])


class Passed(Page):
    def is_displayed(player):
        return all([
            player.field_maybe_none('Q1'), 
            player.field_maybe_none('Q2'), 
            player.field_maybe_none('Q3'), 
            player.field_maybe_none('Q4')
        ])

    def before_next_page(player, timeout_happened):
        player.participant.comprehend = True


class Kicked(Page):
    def is_displayed(player):
        return not all([
            player.field_maybe_none('Q1'), 
            player.field_maybe_none('Q2'), 
            player.field_maybe_none('Q3'), 
            player.field_maybe_none('Q4')
        ])

    def before_next_page(player, timeout_happened):
        player.participant.comprehend = False

page_sequence = [Welcome, CompQuestions, WrongAnswers, CompQuestions, Passed, Kicked]
