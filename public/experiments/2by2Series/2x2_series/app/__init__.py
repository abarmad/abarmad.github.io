from otree.api import *
import random

doc = """
A sequence of four 2x2 games, 5 rounds each. 
Random rematching every round.
"""


class C(BaseConstants):
    NAME_IN_URL = 'matrix_games_sequence'
    PLAYERS_PER_GROUP = 2
    ROUNDS_PER_GAME = 5
    NUM_GAMES = 4  # Changed from 5 to 4
    NUM_ROUNDS = ROUNDS_PER_GAME * NUM_GAMES  # Automatically scales down to 20 rounds
    TIMEOUT_SECONDS = 60  # 1 minute max

    # Define the 4 remaining games. Matrices format: { (Row Choice, Col Choice): (Row Payoff, Col Payoff) }
    GAMES = [
        {
            'name': 'Game 1',
            'matrix': {('A', 'A'): (3, 3), ('A', 'B'): (0, 4), ('B', 'A'): (4, 0), ('B', 'B'): (1, 1)}
        },
        {
            'name': 'Game 2',
            'matrix': {('A', 'A'): (4, 4), ('A', 'B'): (0, 0), ('B', 'A'): (0, 0), ('B', 'B'): (2, 2)}
        },
        {
            'name': 'Game 3',
            'matrix': {('A', 'A'): (4, 2), ('A', 'B'): (0, 0), ('B', 'A'): (0, 0), ('B', 'B'): (2, 4)}
        },
        {
            'name': 'Game 4',
            'matrix': {('A', 'A'): (2, -2), ('A', 'B'): (-2, 2), ('B', 'A'): (-2, 2), ('B', 'B'): (2, -2)}
        }
    ]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    player_name = models.StringField(label="Please enter your player name:")
    choice = models.StringField(
        choices=[['A', 'Action A'], ['B', 'Action B']],
        widget=widgets.RadioSelectHorizontal,
        label="Select your action:"
    )
    is_row = models.BooleanField()
    opponent_choice = models.StringField()
    opponent_payoff = models.IntegerField()

    q1 = models.IntegerField(
        label="From 1 to 5, how useful were the experiments for you to understand economics concepts?",
        min=1, max=5
    )
    q2 = models.StringField(
        label="Have you participated before in experiments on decision making?",
        choices=[
            ['class', 'Yes, in class'],
            ['lab', 'Yes, in a lab'],
            ['never', 'No, never participated before this class']
        ],
        widget=widgets.RadioSelect
    )
    q3 = models.LongStringField(
        label="The Social Science Experimental Laboratory is currently seeking ways to promote the use of experiments in class. We would like to know how these experiments have benefited you in learning so that we can communicate to others the value of experimental methods for teaching economics."
    )

# --- FUNCTIONS ---

def creating_session(subsession: Subsession):
    # Randomly rematch players every single round
    subsession.group_randomly()

    # Assign Roles (1 = Row, 2 = Column)
    for p in subsession.get_players():
        p.is_row = (p.id_in_group == 1)


def set_payoffs(group: Group):
    p1 = group.get_player_by_id(1)  # Row
    p2 = group.get_player_by_id(2)  # Column

    # Fetch current values, defaulting to empty string if None
    p1_choice = p1.field_maybe_none('choice')
    p2_choice = p2.field_maybe_none('choice')

    # Fallback to random choice if the field is None OR empty string ''
    if p1_choice not in ['A', 'B']:
        p1.choice = random.choice(['A', 'B'])

    if p2_choice not in ['A', 'B']:
        p2.choice = random.choice(['A', 'B'])

    # Update the opponent choices with the finalized values
    p1.opponent_choice = p2.choice
    p2.opponent_choice = p1.choice

    # Determine which game we are currently playing (0-indexed)
    game_idx = (group.round_number - 1) // C.ROUNDS_PER_GAME
    matrix = C.GAMES[game_idx]['matrix']

    # Retrieve payoffs safely using the finalized choices
    p1_payoff, p2_payoff = matrix[(p1.choice, p2.choice)]

    p1.payoff = p1_payoff
    p1.opponent_payoff = p2_payoff

    p2.payoff = p2_payoff
    p2.opponent_payoff = p1_payoff


# --- PAGES ---

class Instructions(Page):
    form_model = 'player'
    form_fields = ['player_name']

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'NUM_GAMES': C.NUM_GAMES,
            'ROUNDS_PER_GAME': C.ROUNDS_PER_GAME,
            'NUM_ROUNDS': C.NUM_ROUNDS,
        }


class Submission(Page):
    form_model = 'player'
    form_fields = ['choice']
    timeout_seconds = C.TIMEOUT_SECONDS

    @staticmethod
    def vars_for_template(player: Player):
        game_idx = (player.round_number - 1) // C.ROUNDS_PER_GAME
        current_game_round = ((player.round_number - 1) % C.ROUNDS_PER_GAME) + 1

        raw_matrix = C.GAMES[game_idx]['matrix']
        formatted_matrix = {}
        for (row_choice, col_choice), payoffs in raw_matrix.items():
            key = f"{row_choice}_{col_choice}"  # Creates keys like 'A_A', 'A_B'
            formatted_matrix[key] = f"{payoffs[0]}, {payoffs[1]}"

        return {
            'role': "Row (Player 1)" if player.is_row else "Column (Player 2)",
            'matrix': formatted_matrix,
            'game_round': current_game_round
        }


class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class RoundResults(Page):
    @staticmethod
    def vars_for_template(player: Player):
        current_game_round = ((player.round_number - 1) % C.ROUNDS_PER_GAME) + 1
        return {
            'my_payoff': int(player.payoff),
            'opponent_payoff': player.opponent_payoff,
            'game_round': current_game_round
        }


class ExperimenterPauseWaitPage(WaitPage):
    wait_for_all_groups = True

    @staticmethod
    def is_displayed(player: Player):
        # This forces ALL players to finish the 5 rounds before anyone can see the feedback layout
        return player.round_number % C.ROUNDS_PER_GAME == 0


class GameFeedback(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number % C.ROUNDS_PER_GAME == 0

    @staticmethod
    def vars_for_template(player: Player):
        game_idx = (player.round_number - 1) // C.ROUNDS_PER_GAME
        start_round = game_idx * C.ROUNDS_PER_GAME + 1
        end_round = player.round_number

        # 1. Total points earned for this game type
        my_game_rounds = player.in_rounds(start_round, end_round)
        game_total_points = sum([p.payoff for p in my_game_rounds])

        # 2. Class stats by round (% of A and B)
        round_stats = []
        cell_counts = {('A', 'A'): 0, ('A', 'B'): 0, ('B', 'A'): 0, ('B', 'B'): 0}
        total_pairs_in_game = 0

        for r in range(start_round, end_round + 1):
            subs = player.subsession.in_round(r)
            all_ps = subs.get_players()

            num_A = sum([1 for p in all_ps if p.field_maybe_none('choice') == 'A'])
            total = len(all_ps)

            pct_A = round((num_A / total) * 100) if total else 0
            pct_B = 100 - pct_A if total else 0

            round_stats.append({
                'game_round': r - start_round + 1,
                'pct_A': pct_A,
                'pct_B': pct_B
            })

            # 3. Calculate matrix cell frequencies across all pairs
            for g in subs.get_groups():
                p1 = g.get_player_by_id(1)
                p2 = g.get_player_by_id(2)
                c1 = p1.field_maybe_none('choice')
                c2 = p2.field_maybe_none('choice')
                if c1 and c2:
                    cell_counts[(c1, c2)] += 1
                    total_pairs_in_game += 1

        raw_matrix = C.GAMES[game_idx]['matrix']

        def get_cell_data(row, col):
            payoffs = raw_matrix[(row, col)]
            count = cell_counts[(row, col)]
            pct = round((count / total_pairs_in_game) * 100) if total_pairs_in_game else 0
            return {
                'payoffs': f"{payoffs[0]}, {payoffs[1]}",
                'pct': pct
            }

        return {
            'game_name': C.GAMES[game_idx]['name'],
            'game_total_points': int(game_total_points),
            'round_stats': round_stats,
            'cell_AA': get_cell_data('A', 'A'),
            'cell_AB': get_cell_data('A', 'B'),
            'cell_BA': get_cell_data('B', 'A'),
            'cell_BB': get_cell_data('B', 'B'),
        }


class FinalSummary(Page):
    form_model = 'player'
    form_fields = ['q1', 'q2', 'q3']  # Tells oTree to expect and save these fields

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        # --- 1. GLOBAL LEADERBOARD ---
        all_players_current = player.subsession.get_players()
        leaderboard = []

        for p in all_players_current:
            total_payoff = sum([prev.payoff for prev in p.in_all_rounds()])
            name = p.in_round(1).field_maybe_none('player_name') or f"Player {p.id_in_subsession}"

            leaderboard.append({
                'name': name,
                'total_profit': int(total_payoff),
                'is_me': p.participant.id == player.participant.id
            })

        leaderboard.sort(key=lambda x: x['total_profit'], reverse=True)
        for index, p_data in enumerate(leaderboard):
            p_data['rank'] = index + 1

        # --- 2. BUNDLED ROW-BY-ROW GAME DATA ---
        games_rows = []

        for g_idx in range(C.NUM_GAMES):
            start_round = g_idx * C.ROUNDS_PER_GAME + 1
            end_round = start_round + C.ROUNDS_PER_GAME - 1

            # Storage structures for this game's history
            evolution_A = []
            evolution_B = []
            cell_counts = {('A', 'A'): 0, ('A', 'B'): 0, ('B', 'A'): 0, ('B', 'B'): 0}
            total_pairs_in_game = 0

            # Loop through the 5 specific history rounds for this game type
            for r in range(start_round, end_round + 1):
                historical_subsession = player.subsession.in_round(r)
                all_ps = historical_subsession.get_players()

                # Calculate strategies for evolution charts
                num_A = sum([1 for p in all_ps if p.field_maybe_none('choice') == 'A'])
                total = len(all_ps)
                pct_A = round((num_A / total) * 100) if total else 0
                evolution_A.append(pct_A)
                evolution_B.append(100 - pct_A)

                # Calculate cumulative historical matrix cell frequencies across all pairs
                for g in historical_subsession.get_groups():
                    p1 = g.get_player_by_id(1)
                    p2 = g.get_player_by_id(2)
                    c1 = p1.field_maybe_none('choice')
                    c2 = p2.field_maybe_none('choice')
                    if c1 and c2:
                        cell_counts[(c1, c2)] += 1
                        total_pairs_in_game += 1

            # Extract raw payoffs to stitch next to percentages
            raw_matrix = C.GAMES[g_idx]['matrix']

            def get_cell_metrics(row, col):
                payoffs = raw_matrix[(row, col)]
                count = cell_counts[(row, col)]
                pct = round((count / total_pairs_in_game) * 100) if total_pairs_in_game else 0
                return {'payoffs': f"{payoffs[0]}, {payoffs[1]}", 'pct': pct}

            # Package all analytical components for this specific game row
            games_rows.append({
                'game_number': g_idx + 1,
                'game_name': C.GAMES[g_idx]['name'],
                # Matrix data layout structure
                'cell_AA': get_cell_metrics('A', 'A'),
                'cell_AB': get_cell_metrics('A', 'B'),
                'cell_BA': get_cell_metrics('B', 'A'),
                'cell_BB': get_cell_metrics('B', 'B'),
                # Evolution chart lists
                'evolution_A': evolution_A,
                'evolution_B': evolution_B,
                'rounds_labels': [str(i) for i in range(1, C.ROUNDS_PER_GAME + 1)]
            })

        return {
            'leaderboard': leaderboard,
            'games_rows': games_rows
        }

class ThankYou(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

page_sequence = [
    Instructions,
    Submission,
    ResultsWaitPage,
    RoundResults,
    ExperimenterPauseWaitPage,
    GameFeedback,
    FinalSummary,
    ThankYou
]