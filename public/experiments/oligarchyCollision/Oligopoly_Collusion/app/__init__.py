from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'Monopoly_Quantity_Game'
    PLAYERS_PER_GROUP = 5
    NUM_ROUNDS = 2
    TIMEOUT_SECONDS = 120  # 2 minutes timer for submission

    # Payoff matrix [Your Choice][Number of OTHER participants choosing LOW]
    PAYOFF_MATRIX = {
        'Low': {4: 10, 3: 8, 2: 6, 1: 4, 0: 2},
        'High': {4: 12, 3: 11, 2: 9, 1: 7, 0: 5}
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    total_low = models.IntegerField()
    total_high = models.IntegerField()


class Player(BasePlayer):
    player_name = models.StringField(label="Please enter your player name:")
    choice = models.StringField(
        choices=[
            ['Low', 'Low Quantity (L)'],
            ['High', 'High Quantity (H)']
        ],
        widget=widgets.RadioSelect,
        label="Select your production quantity:"
    )
    others_low = models.IntegerField()
    others_high = models.IntegerField()
    justification = models.LongStringField(
        label="Reflective Reasoning: Based on the outcome of this first round, please provide your thoughts on your strategy."
    )


def set_payoffs(group: Group):
    players = group.get_players()

    # Handle timeouts (assign random choice if they didn't submit in time)
    for p in players:
        if not p.field_maybe_none('choice'):
            p.choice = random.choice(['Low', 'High'])

    # Tally up choices
    group.total_low = sum([1 for p in players if p.choice == 'Low'])
    group.total_high = sum([1 for p in players if p.choice == 'High'])

    # Determine individual outcomes and payoffs
    for p in players:
        if p.choice == 'Low':
            p.others_low = group.total_low - 1
        else:
            p.others_low = group.total_low

        p.others_high = (C.PLAYERS_PER_GROUP - 1) - p.others_low

        # Calculate payoff from the matrix
        p.payoff = C.PAYOFF_MATRIX[p.choice][p.others_low]


# --- PAGES ---

class Instructions(Page):
    form_model = 'player'
    form_fields = ['player_name']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def player_name_error_message(player, value):
        stripped_value = value.strip()
        if not stripped_value:
            return "Name cannot be empty."
        if not stripped_value.replace(" ", "").isalnum():
            return "Names can only contain letters and numbers (no special characters)."

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'numRounds': C.NUM_ROUNDS,
            'numPlayers': C.PLAYERS_PER_GROUP
        }


class Submission(Page):
    form_model = 'player'
    form_fields = ['choice']
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'roundNum': player.round_number,
        }


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    form_model = 'player'

    def get_form_fields(player):
        return ['justification'] if player.round_number == 1 else []

    @staticmethod
    def justification_error_message(player, value):
        if not value or not value.strip():
            return "Please provide a valid explanation. Your response cannot be empty or just spaces."

    @staticmethod
    def vars_for_template(player: Player):
        cumulative_profit = sum([p.payoff for p in player.in_all_rounds()])
        return {
            'cumulative_profit': cumulative_profit
        }


class Summary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        all_players = group.get_players()
        leaderboard = []

        # 1. Build Leaderboard
        for p in all_players:
            name_to_display = p.in_round(1).field_maybe_none('player_name') or f"Player {p.id_in_group}"
            total_payoff = sum([prev_p.payoff for prev_p in p.in_all_rounds()])
            leaderboard.append({
                'id': p.id_in_group,
                'name': name_to_display,
                'total_profit': total_payoff,
                'is_me': p.id_in_group == player.id_in_group
            })

        leaderboard.sort(key=lambda x: x['total_profit'], reverse=True)

        # 2. Build Round History for this specific player
        history = []
        cumulative = 0
        for p in player.in_all_rounds():
            cumulative += p.payoff
            history.append({
                'round': p.round_number,
                'choice': p.choice,
                'others_low': p.others_low,
                'others_high': p.others_high,
                'profit': p.payoff,
                'cumulative': cumulative
            })

        # 3. Build Aggregate Profit Data for the Chart
        group_rounds = []
        aggregate_profits = []
        for g in group.in_all_rounds():
            group_rounds.append(g.round_number)
            # Sum the payoff of all players in this specific round
            total_profit = sum([p.payoff for p in g.get_players()])
            aggregate_profits.append(total_profit)

        return {
            'leaderboard': leaderboard,
            'history': history,
            'group_rounds': group_rounds,
            'aggregate_profits': aggregate_profits
        }

page_sequence = [Instructions, Submission, ResultsWaitPage, Results, Summary]