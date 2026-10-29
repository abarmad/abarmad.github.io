from otree.api import *
import random

class C(BaseConstants):
    NAME_IN_URL = 'public_goods'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 5
    ENDOWMENT = 10
    MULTIPLIER = 3
    PUNISHMENT_ENDOWMENT = 2
    PUNISHMENT_COST = 1
    PUNISHMENT_REDUCTION = 3
    MAX_REDUCTION_PER_PLAYER = 6


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    total_contribution = models.IntegerField()
    average_contribution = models.FloatField()
    individual_share = models.FloatField()


class Player(BasePlayer):
    treatment = models.StringField(initial="")
    player_name = models.StringField(label="Please enter your player name:")
    shuffled_id = models.IntegerField()
    contribution = models.IntegerField(
        min_value=0, max_value=C.ENDOWMENT,
        label="How many points do you want to contribute (0-10)?"
    )
    punishment_sent = models.IntegerField(initial=0)
    punishment_received = models.IntegerField(initial=0)
    justification = models.LongStringField(label="Can you explain your reasoning behind your first contribution decision?")
    nextContribution = models.LongStringField(label="Will you change your contribution for the next round? If so, why?")

def creating_session(subsession: Subsession):
    # Get the treatment from settings.py
    treatment = subsession.session.config.get('treatment', 'PG')
    for p in subsession.get_players():
        p.treatment = treatment

    for ss in subsession.in_all_rounds():
        for group in ss.get_groups():
            players = group.get_players()
            ids = list(range(1, len(players) + 1))
            random.shuffle(ids)

            for i, p in enumerate(players):
                p.treatment = treatment
                p.shuffled_id = ids[i]

def punishment_field(recipient_id):
    return models.IntegerField(
        min_value=0,
        max_value=C.MAX_REDUCTION_PER_PLAYER // C.PUNISHMENT_REDUCTION,
        initial=0,
        label=f"Punish Player {recipient_id}"
    )

def set_payoffs(group: Group):
    players = group.get_players()
    contributions = [p.contribution for p in players]
    group.total_contribution = sum(contributions)
    group.average_contribution = round(group.total_contribution / len(players), 2)
    group.individual_share = round((group.total_contribution * C.MULTIPLIER) / len(players), 2)

    for p in players:
        p.payoff = (C.ENDOWMENT - p.contribution) + group.individual_share


def set_final_punishment(group: Group):
    players = group.get_players()
    treatment = group.session.config.get('treatment')

    if treatment == 'PG_P':
        for p in players:
            sent_this_round = 0
            received_this_round = 0

            # Sum up what this player sent to others
            for other in p.get_others_in_group():
                # We retrieve the dynamic form value: 'punish_p{id}'
                field_name = f'punish_p{other.id_in_group}'
                units = getattr(p, field_name)
                sent_this_round += units
                # Add reduction to the target
                other.punishment_received += (units * C.PUNISHMENT_REDUCTION)

            p.punishment_sent = sent_this_round * C.PUNISHMENT_COST

        # Update final payoff for PG_P
        for p in players:
            p.payoff += C.PUNISHMENT_ENDOWMENT - p.punishment_sent - p.punishment_received

# --- PAGES ---

class Instructions(Page):
    form_model = 'player'
    form_fields = ['player_name']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    # CUSTOM VALIDATION HERE
    @staticmethod
    def player_name_error_message(player, value):
        # strip() removes leading/trailing whitespace
        if not value or value.strip() == "":
            return "Your name cannot be empty or consist only of spaces."

    def vars_for_template(player: Player):
        return {
            'is_pg_p': player.treatment == 'PG_P'
        }

    def before_next_page(player: Player, timeout_happened):
        player.participant.name = player.player_name

class Submission(Page):
    form_model = 'player'
    form_fields = ['contribution']


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

class Results(Page):
    form_model = 'player'

    def get_form_fields(player):
        fields = []
        if player.round_number == 1:
            fields += ['justification', 'nextContribution']
        if player.treatment == 'PG_P':
            fields += [f'punish_p{other.id_in_group}' for other in player.get_others_in_group()]
        return fields

    def error_message(player, values):
        if player.treatment == 'PG_P':
            punishment_values = [
                val for field, val in values.items()
                if field.startswith('punish_p') and val is not None
            ]

            total_punishment_cost = sum(punishment_values)

            if total_punishment_cost > C.PUNISHMENT_ENDOWMENT:
                return f"You only have {C.PUNISHMENT_ENDOWMENT} points to spend on reductions. " \
                       f"You tried to spend {total_punishment_cost} points."


    def vars_for_template(player: Player):
        others_data = []
        for other in player.get_others_in_group():
            round_1_player = other.in_round(1)
            actual_name = round_1_player.field_maybe_none('player_name') or f"Player {other.id_in_group}"

            others_data.append({
                'id_in_group': other.id_in_group,
                'player_name': other.shuffled_id if other.shuffled_id is not None else other.id_in_group,
                'nickname': actual_name,
                'contribution': other.contribution,
            })



        others_data.sort(key=lambda x: x['player_name'])

        return {
            'is_pg_p': player.treatment == 'PG_P',
            'others': others_data,
            'total_earnings': sum([p.payoff for p in player.in_all_rounds()]),
            'numPlayers': len(others_data)+1,
            'my_id': player.shuffled_id if player.shuffled_id is not None else player.id_in_group
        }

class PunishmentWaitPage(WaitPage):
    @staticmethod
    def is_displayed(player): return player.treatment == 'PG_P'
    after_all_players_arrive = set_final_punishment

class FinalResults(Page):
    @staticmethod
    def is_displayed(player):
        return player.treatment == 'PG_P'

    def vars_for_template(player: Player):
        # Calculate Base Profit: (10 - Contrib + Share)
        # This reverses the payoff calculation to show the intermediate step
        base_profit = (C.ENDOWMENT - player.contribution) + player.group.individual_share

        return {
            'base_profit': base_profit,
            'punishment_endowment': C.PUNISHMENT_ENDOWMENT,
        }

class Summary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        # Access the first group's history (assuming one group for the session)
        group = player.group

        # 1. Create a list of average contributions per round for the Y-axis
        avg_contrib_history = [
            round(g.average_contribution, 2)
            for g in group.in_all_rounds()
        ]

        # 2. Leaderboard logic
        all_players = group.get_players()
        leaderboard = []
        for p in all_players:
            leaderboard.append({
                'name': p.in_round(1).field_maybe_none('player_name') or "Anonymous",
                'total_profit': float(sum([prev_p.payoff for prev_p in p.in_all_rounds()])),
                'is_me': p.id_in_group == player.id_in_group
            })
        leaderboard.sort(key=lambda x: x['total_profit'], reverse=True)

        return {
            'leaderboard': leaderboard,
            'avg_contrib_history': avg_contrib_history,
            'rounds': list(range(1, C.NUM_ROUNDS + 1))
        }

for i in range(1, 100):
    setattr(Player, f'punish_p{i}', punishment_field(i))

page_sequence = [Instructions, Submission, ResultsWaitPage, Results, PunishmentWaitPage, FinalResults, Summary]
