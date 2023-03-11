from otree.api import *
import random

doc = """  """


def select_game():
    g = random.randint(1, 8)
    return g


class C(BaseConstants):
    NAME_IN_URL = 'experiment1'
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 1
    PLAYER_ID_DICT = {1: "A", 2: "B", 3: "C"}
    COALITION_SUMS = {1: {"ABC": 100, "AB": 100, "AC": 100, "BC": 0, "A": 0, "B": 0, "C": 0},
                      2: {"ABC": 100, "AB": 100, "AC": 70, "BC": 30, "A": 0, "B": 0, "C": 0},
                      3: {"ABC": 100, "AB": 90, "AC": 70, "BC": 40, "A": 0, "B": 0, "C": 0},
                      4: {"ABC": 100, "AB": 90, "AC": 50, "BC": 20, "A": 0, "B": 0, "C": 0},
                      5: {"ABC": 100, "AB": 90, "AC": 70, "BC": 40, "A": 60, "B": 0, "C": 0},
                      6: {"ABC": 100, "AB": 60, "AC": 40, "BC": 10, "A": 0, "B": 0, "C": 0},
                      7: {"ABC": 100, "AB": 60, "AC": 40, "BC": 10, "A": 20, "B": 20, "C": 20},
                      8: {"ABC": 100, "AB": 60, "AC": 60, "BC": 60, "A": 0, "B": 0, "C": 0}}


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    # which game treatment was played
    game = models.IntegerField(initial=select_game())

    # group data field for whether an agreement was reached
    merger_formed = models.BooleanField(initial=False)

    # group data fields for results
    merger_result = models.StringField(initial=None)
    A_result = models.IntegerField(initial=0)
    B_result = models.IntegerField(initial=0)
    C_result = models.IntegerField(initial=0)

    # group data fields for individual player acceptances
    ABC_A_accepted = models.BooleanField(initial=False)
    ABC_B_accepted = models.BooleanField(initial=False)
    ABC_C_accepted = models.BooleanField(initial=False)
    AB_A_accepted = models.BooleanField(initial=False)
    AB_B_accepted = models.BooleanField(initial=False)
    AC_A_accepted = models.BooleanField(initial=False)
    AC_C_accepted = models.BooleanField(initial=False)
    BC_B_accepted = models.BooleanField(initial=False)
    BC_C_accepted = models.BooleanField(initial=False)

    # group data fields for all merger shares
    ABC_A = models.IntegerField(initial=0)
    ABC_B = models.IntegerField(initial=0)
    ABC_C = models.IntegerField(initial=0)
    AB_A = models.IntegerField(initial=0)
    AB_B = models.IntegerField(initial=0)
    AC_A = models.IntegerField(initial=0)
    AC_C = models.IntegerField(initial=0)
    BC_B = models.IntegerField(initial=0)
    BC_C = models.IntegerField(initial=0)


class Player(BasePlayer):
    pass


# PAGES
class ArrivalPage(WaitPage):
    group_by_arrival_time = True
    title_text = "Please wait"
    body_text = "The game will start once all players in the group are ready"

    # randomly select game for the group to play
    @staticmethod
    def after_all_players_arrive(group: Group):
        group.game = select_game()


class Interaction(Page):
    timeout_seconds = 600


    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.group.merger_result = "No coalition formed"
            player.group.A_result = C.COALITION_SUMS[player.group.game]["A"]
            player.group.B_result = C.COALITION_SUMS[player.group.game]["B"]
            player.group.C_result = C.COALITION_SUMS[player.group.game]["C"]

    # variables to pass to page template
    @staticmethod
    def vars_for_template(player):
        abc_channel = "ABC" + str(player.group.id)
        ab_channel = "AB" + str(player.group.id)
        ac_channel = "AC" + str(player.group.id)
        bc_channel = "BC" + str(player.group.id)
        chat_id = "Rep " + str(C.PLAYER_ID_DICT[player.id_in_group])
        return dict(
            ABC=abc_channel,
            AB=ab_channel,
            AC=ac_channel,
            BC=bc_channel,
            ABC_A=player.group.ABC_A,
            ABC_B=player.group.ABC_B,
            ABC_C=player.group.ABC_C,
            AB_A=player.group.AB_A,
            AB_B=player.group.AB_B,
            AC_A=player.group.AC_A,
            AC_C=player.group.AC_C,
            BC_B=player.group.BC_B,
            BC_C=player.group.BC_C,
            chat_id=chat_id,
        )

    @staticmethod
    def live_method(player, data):

        # recieved data is from an error
        if data['type'] == 'error':
            return {0: data['exception']}

        # recieved data is an offer
        elif data['type'] == 'offer':
            data['from_ID'] = player.id_in_group
            data['from_letter'] = C.PLAYER_ID_DICT[player.id_in_group]

            # recieved data is for the ABC merger
            if data['merger'] == 'ABC':
                player.group.ABC_A = data['ABC_A_val']
                player.group.ABC_A_accepted = False
                player.group.ABC_B = data['ABC_B_val']
                player.group.ABC_B_accepted = False
                player.group.ABC_C = data['ABC_C_val']
                player.group.ABC_C_accepted = False
                data.update({'new_offer': 'ABC', 'remove_checks': [
                            'ABC_A_accepted', 'ABC_B_accepted', 'ABC_C_accepted']})
                return {0: data}

            # recieved data is for the AB merger
            if data['merger'] == 'AB':
                player.group.AB_A = data['AB_A_val']
                player.group.AB_A_accepted = False
                player.group.AB_B = data['AB_B_val']
                player.group.AB_B_accepted = False
                data.update({'new_offer': 'AB', 'remove_checks': [
                            'AB_A_accepted', 'AB_B_accepted']})
                return {0: data}

            # recieved data is for the AC merger
            if data['merger'] == 'AC':
                player.group.AC_A = data['AC_A_val']
                player.group.AC_A_accepted = False
                player.group.AC_C = data['AC_C_val']
                player.group.AC_C_accepted = False
                data.update({'new_offer': 'AC', 'remove_checks': [
                            'AC_A_accepted', 'AC_C_accepted']})
                return {0: data}

            # recieved data is for the BC merger
            if data['merger'] == 'BC':
                player.group.BC_B = data['BC_B_val']
                player.group.BC_B_accepted = False
                player.group.BC_C = data['BC_C_val']
                player.group.BC_C_accepted = False
                data.update({'new_offer': 'BC', 'remove_checks': [
                            'BC_B_accepted', 'BC_C_accepted']})
                return {0: data}

        # the recieved data is an offer acception
        elif data['type'] == 'accept':

            # recieved offer acception is for the ABC merger
            if data['merger'] == 'ABC':
                if data['accepted_by'] == 1:
                    player.group.ABC_A_accepted = True
                if data['accepted_by'] == 2:
                    player.group.ABC_B_accepted = True
                if data['accepted_by'] == 3:
                    player.group.ABC_C_accepted = True

                # all players in coalition agree to offer
                if player.group.ABC_A_accepted and player.group.ABC_B_accepted and player.group.ABC_C_accepted:
                    player.group.merger_result = "ABC"
                    player.group.A_result = player.group.ABC_A
                    player.group.B_result = player.group.ABC_B
                    player.group.C_result = player.group.ABC_C
                    player.group.merger_formed = True
                    return {0: {'game_over': True}}
                else:
                    return {0: {'accepted': 'ABC_'+C.PLAYER_ID_DICT[player.id_in_group]+'_accepted'}}

            # recieved offer acception is for the AB merger
            if data['merger'] == 'AB':
                if data['accepted_by'] == 1:
                    player.group.AB_A_accepted = True
                if data['accepted_by'] == 2:
                    player.group.AB_B_accepted = True

                # all players in coalition agree to offer
                if player.group.AB_A_accepted and player.group.AB_B_accepted:
                    player.group.merger_result = "AB"
                    player.group.A_result = player.group.AB_A
                    player.group.B_result = player.group.AB_B
                    player.group.merger_formed = True
                    return {0: {'game_over': True}}
                else:
                    return {0: {'accepted': 'AB_'+C.PLAYER_ID_DICT[player.id_in_group]+'_accepted'}}

            # recieved offer acception is for the AC merger
            if data['merger'] == 'AC':
                if data['accepted_by'] == 1:
                    player.group.AC_A_accepted = True
                if data['accepted_by'] == 3:
                    player.group.AC_C_accepted = True

                # all players in coalition agree to offer
                if player.group.AC_A_accepted and player.group.AC_C_accepted:
                    player.group.merger_result = "AC"
                    player.group.A_result = player.group.AC_A
                    player.group.C_result = player.group.AC_C
                    player.group.merger_formed = True
                    return {0: {'game_over': True}}
                else:
                    return {0: {'accepted': 'AC_'+C.PLAYER_ID_DICT[player.id_in_group]+'_accepted'}}

            # recieved offer acception is for the BC merger
            if data['merger'] == 'BC':
                if data['accepted_by'] == 2:
                    player.group.BC_B_accepted = True
                if data['accepted_by'] == 3:
                    player.group.BC_C_accepted = True

                # all players in coalition agree to offer
                if player.group.BC_B_accepted and player.group.BC_C_accepted:
                    player.group.merger_result = "BC"
                    player.group.B_result = player.group.BC_B
                    player.group.C_result = player.group.BC_C
                    player.group.merger_formed = True
                    return {0: {'game_over': True}}
                else:
                    return {0: {'accepted': 'BC_'+C.PLAYER_ID_DICT[player.id_in_group]+'_accepted'}}


class Results(Page):
    def before_next_page(player, timeout_happened):
        treatment = random.randint(1, 4)
        player.participant.treatment = treatment

        if player.id_in_group == 1:
            player.participant.payoff += player.group.A_result / 10
        elif player.id_in_group == 2:
            player.participant.payoff += player.group.B_result / 10
        elif player.id_in_group == 3:
            player.participant.payoff += player.group.C_result / 10


class StartGame(WaitPage):
    pass

class Welcome(Page):
    def vars_for_template(player):
        return dict(
            ABC=C.COALITION_SUMS[player.group.game]["ABC"],
            AB=C.COALITION_SUMS[player.group.game]["AB"],
            AC=C.COALITION_SUMS[player.group.game]["AC"],
            BC=C.COALITION_SUMS[player.group.game]["BC"],
            A=C.COALITION_SUMS[player.group.game]["A"],
            B=C.COALITION_SUMS[player.group.game]["B"],
            C=C.COALITION_SUMS[player.group.game]["C"]
        )

page_sequence = [ArrivalPage, Welcome, StartGame, Interaction, Results]
