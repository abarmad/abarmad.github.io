from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'Monopoly_Quantity_Game'
    PLAYERS_PER_GROUP = 5

    # ---- Part 1: fixed number of rounds, groups reshuffled randomly every round
    NUM_ROUNDS_P1 = 10
    # ---- Part 2: random number of rounds, same group throughout, with chat
    CONTINUE_PROB = 0.9        # 90% chance of continuing, 10% chance this round is the last
    MAX_ROUNDS_P2 = 50         # safety cap (P(reaching it) = 0.9^49, about 0.6%)
    # oTree needs a fixed upper bound on rounds. Rounds after the random stop are skipped.
    NUM_ROUNDS = NUM_ROUNDS_P1 + MAX_ROUNDS_P2

    TIMEOUT_P1 = 120           # seconds
    TIMEOUT_P2 = 180           # seconds (a bit longer, since players can chat)

    # The PDF says Part 1 feedback = choice, profit, cumulative profit (no L/H counts).
    # Set to True if you also want the L/H counts shown in Part 1.
    SHOW_OTHERS_IN_PART1 = False

    # Payoff matrix [Your Choice][Number of OTHER participants choosing LOW]
    PAYOFF_MATRIX = {
        'Low': {4: 10, 3: 8, 2: 6, 1: 4, 0: 2},
        'High': {4: 12, 3: 11, 2: 9, 1: 7, 0: 5}
    }


# --- HELPERS ---

P2_START = C.NUM_ROUNDS_P1 + 1


def get_part(round_number):
    return 1 if round_number <= C.NUM_ROUNDS_P1 else 2


def part_start(round_number):
    return 1 if round_number <= C.NUM_ROUNDS_P1 else P2_START


def last_round(session):
    """Last round actually played in the experiment (Part 2 length is drawn at random)."""
    return C.NUM_ROUNDS_P1 + session.vars['part2_rounds']


def is_active(player):
    return player.round_number <= last_round(player.session)


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session

    # Draw the length of Part 2 once (round 1 runs first).
    if subsession.round_number == 1:
        override = session.config.get('part2_num_rounds')  # optional, handy for testing
        if override:
            n = min(int(override), C.MAX_ROUNDS_P2)
        else:
            n = 1
            while n < C.MAX_ROUNDS_P2 and random.random() < C.CONTINUE_PROB:
                n += 1
        session.vars['part2_rounds'] = n

    # Matching
    if subsession.round_number <= P2_START:
        # Part 1: new random groups every round.
        # Round P2_START: random groups that stay fixed for all of Part 2.
        subsession.group_randomly()
    else:
        subsession.group_like_round(P2_START)


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


def chat_vars(player: Player):
    """Chat is only used in Part 2. The channel is tied to the (fixed) Part 2 group,
    so the chat history persists across rounds."""
    if get_part(player.round_number) != 2:
        return {}
    g = player.in_round(P2_START).group
    return {
        'chat_channel': f"{player.session.code}_part2_group_{g.id_in_subsession}",
        'chat_nickname': f"Player {player.id_in_group}",
    }


# --- PAGES ---

class Instructions(Page):
    """Part 1 instructions + name entry."""
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
            'numRounds': C.NUM_ROUNDS_P1,
            'numPlayers': C.PLAYERS_PER_GROUP
        }


class Part2Instructions(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == P2_START

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'numPlayers': C.PLAYERS_PER_GROUP,
            'stopPct': round((1 - C.CONTINUE_PROB) * 100),
            'continuePct': round(C.CONTINUE_PROB * 100),
        }


class Submission(Page):
    form_model = 'player'
    form_fields = ['choice']

    @staticmethod
    def is_displayed(player: Player):
        return is_active(player)

    @staticmethod
    def get_timeout_seconds(player: Player):
        return C.TIMEOUT_P1 if get_part(player.round_number) == 1 else C.TIMEOUT_P2

    @staticmethod
    def vars_for_template(player: Player):
        part = get_part(player.round_number)
        d = {
            'part': part,
            'roundNum': player.round_number - part_start(player.round_number) + 1,
            'numRoundsP1': C.NUM_ROUNDS_P1,
        }
        d.update(chat_vars(player))
        return d


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs

    @staticmethod
    def is_displayed(player: Player):
        return is_active(player)


class Results(Page):
    form_model = 'player'

    @staticmethod
    def is_displayed(player: Player):
        return is_active(player)

    @staticmethod
    def get_form_fields(player: Player):
        return ['justification'] if player.round_number == 1 else []

    @staticmethod
    def justification_error_message(player, value):
        if not value or not value.strip():
            return "Please provide a valid explanation. Your response cannot be empty or just spaces."

    @staticmethod
    def vars_for_template(player: Player):
        part = get_part(player.round_number)
        start = part_start(player.round_number)
        # Cumulative profit within the current part
        cumulative_profit = sum([p.payoff for p in player.in_rounds(start, player.round_number)])
        d = {
            'part': part,
            'roundNum': player.round_number - start + 1,
            'numRoundsP1': C.NUM_ROUNDS_P1,
            'cumulative_profit': cumulative_profit,
            'show_others': part == 2 or C.SHOW_OTHERS_IN_PART1,
        }
        d.update(chat_vars(player))
        return d


def build_history(player: Player, first, last, show_others):
    history = []
    cumulative = 0
    for p in player.in_rounds(first, last):
        cumulative += p.payoff
        history.append({
            'round': p.round_number - first + 1,
            'choice': p.choice,
            'others_low': p.others_low if show_others else None,
            'others_high': p.others_high if show_others else None,
            'profit': p.payoff,
            'cumulative': cumulative
        })
    return history


class Summary(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == last_round(player.session)

    @staticmethod
    def vars_for_template(player: Player):
        final = last_round(player.session)
        group = player.group  # in the final round this is the fixed Part 2 group
        members = group.get_players()

        # 1. Leaderboard (Part 2 group; Part 1 + Part 2 profits)
        leaderboard = []
        for p in members:
            name = p.in_round(1).field_maybe_none('player_name') or f"Player {p.id_in_group}"
            p1 = sum([x.payoff for x in p.in_rounds(1, C.NUM_ROUNDS_P1)])
            p2 = sum([x.payoff for x in p.in_rounds(P2_START, final)])
            leaderboard.append({
                'name': name,
                'p1_profit': p1,
                'p2_profit': p2,
                'total_profit': p1 + p2,
                'is_me': p.id_in_group == player.id_in_group
            })
        leaderboard.sort(key=lambda x: x['total_profit'], reverse=True)

        # 2. Round history for this player, per part
        history_p1 = build_history(player, 1, C.NUM_ROUNDS_P1, C.SHOW_OTHERS_IN_PART1)
        history_p2 = build_history(player, P2_START, final, True)

        # 3. Aggregate group profit per round in Part 2 (fixed group)
        group_rounds = []
        aggregate_profits = []
        for r in range(P2_START, final + 1):
            group_rounds.append(r - P2_START + 1)
            aggregate_profits.append(sum([m.in_round(r).payoff for m in members]))

        return {
            'leaderboard': leaderboard,
            'history_p1': history_p1,
            'history_p2': history_p2,
            'show_others_p1': C.SHOW_OTHERS_IN_PART1,
            'group_rounds': group_rounds,
            'aggregate_profits': aggregate_profits,
        }


page_sequence = [Instructions, Part2Instructions, Submission, ResultsWaitPage, Results, Summary]
