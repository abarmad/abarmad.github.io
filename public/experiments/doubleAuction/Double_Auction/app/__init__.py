from otree.api import *
import random


class C(BaseConstants):
    NAME_IN_URL = 'uniform_double_auction'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 10
    BUYER_VAL_RANGE = [30, 80]
    SELLER_COST_RANGE = [10, 50]
    BONUS_POINTS = 10


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    market_price = models.FloatField()
    quantity = models.IntegerField()
    treatment = models.StringField()
    all_bought = models.BooleanField()
    theo_total_surplus = models.FloatField()
    theo_max_surplus = models.FloatField()
    actual_total_surplus = models.FloatField()


class Player(BasePlayer):
    treatment = models.StringField()
    is_buyer = models.BooleanField()
    value = models.IntegerField()
    cost = models.IntegerField()
    bid = models.FloatField(min=0)
    ask = models.FloatField(min=0)
    is_trader = models.BooleanField(initial=False)
    trading_profit = models.FloatField(initial=0)
    justification = models.LongStringField()
    player_name = models.StringField(label="Please enter your player name:")


def creating_session(subsession: Subsession):
    treatment = subsession.session.config.get('treatment', 'default')

    if subsession.round_number == 1:
        for g in subsession.get_groups():
            players = g.get_players()
            random.shuffle(players)
            for i, p in enumerate(players):
                p.participant.is_buyer = i < len(players) / 2

    for g in subsession.get_groups():
        g.treatment = treatment
        players = g.get_players()
        num_players = len(players)

        # Role Assignment
        for p in players:
            p.treatment = treatment
            if subsession.round_number <= (C.NUM_ROUNDS // 2):
                p.is_buyer = p.participant.is_buyer
            else:
                p.is_buyer = not p.participant.is_buyer

            if p.is_buyer:
                p.value = random.randint(C.BUYER_VAL_RANGE[0], C.BUYER_VAL_RANGE[1])
                p.ask = 0
            else:
                p.cost = random.randint(C.SELLER_COST_RANGE[0], C.SELLER_COST_RANGE[1])
                p.bid = 0

        # Parameter Balancing Logic
        buyers = sorted([p for p in players if p.is_buyer], key=lambda p: p.value, reverse=True)
        sellers = sorted([p for p in players if not p.is_buyer], key=lambda p: p.cost)

        # 1. Ensure Interior Equilibrium (0 < Q* < N_sellers)
        if buyers[0].value < sellers[0].cost:
            buyers[0].value = sellers[0].cost + 5
        if buyers[-1].value > sellers[-1].cost:
            sellers[-1].cost = buyers[-1].value + 5

        # 2. Competitive Treatment Constraint: Sum of negative surplus < Bonus * NumPlayers
        if treatment == 'competitive':
            total_potential_bonus = num_players * C.BONUS_POINTS
            sum_neg_surplus = 0
            for b, s in zip(buyers, sellers):
                surplus = b.value - s.cost
                if surplus < 0:
                    sum_neg_surplus += abs(surplus)

            # If negative surplus is too high, buff the values/costs to satisfy logic
            while sum_neg_surplus >= (total_potential_bonus - 5):
                # Buff the weakest buyer or reduce cost of weakest seller
                buyers[-1].value += 2
                sellers[-1].cost -= 2
                sum_neg_surplus = sum(abs(b.value - s.cost) for b, s in zip(buyers, sellers) if (b.value - s.cost) < 0)


def set_payoffs(group: Group):
    players = group.get_players()
    buyers = sorted([p for p in players if p.is_buyer], key=lambda p: p.bid, reverse=True)
    sellers = sorted([p for p in players if not p.is_buyer], key=lambda p: p.ask)

    # Calculate Market Clearing
    q_star = 0
    for b, s in zip(buyers, sellers):
        if b.bid >= s.ask:
            q_star += 1
        else:
            break

    group.quantity = q_star
    group.all_bought = (q_star == len(buyers)) and (len(buyers) > 0)
    bonus = C.BONUS_POINTS if (group.treatment == 'competitive' and group.all_bought) else 0

    if q_star > 0:
        group.market_price = (buyers[q_star - 1].bid + sellers[q_star - 1].ask) / 2
        for i, p in enumerate(buyers):
            if i < q_star:
                p.is_trader = True
                p.trading_profit = p.value - group.market_price
            else:
                p.trading_profit = 0

            p.payoff = p.trading_profit + bonus

        for i, p in enumerate(sellers):
            if i < q_star:
                p.is_trader = True
                p.trading_profit = group.market_price - p.cost

            else:
                p.trading_profit = 0
            p.payoff = p.trading_profit + bonus
    else:
        group.market_price = 0
        for p in players:
            p.trading_profit = 0
            p.payoff = bonus

    # --- Surplus Calculations for Summary ---
    # Theo Total Surplus (Private matches only)
    b_vals = sorted([p.value for p in players if p.is_buyer], reverse=True)
    s_costs = sorted([p.cost for p in players if not p.is_buyer])


    # Efficient competitive-equilibrium surplus:
    # only trades where buyer value >= seller cost
    efficient_surplus = sum(v - c for v, c in zip(b_vals, s_costs) if v >= c)
    group.theo_total_surplus = efficient_surplus

    # Maximum surplus depends on treatment
    if group.treatment == 'competitive':
        # In competitive treatment, everyone trading can trigger
        # the bonus, so calculate surplus from ALL trades + bonus.
        all_trade_surplus = sum(v - c for v, c in zip(b_vals, s_costs))
        bonus_pool = len(players) * C.BONUS_POINTS
        group.theo_max_surplus = all_trade_surplus + bonus_pool

    else:
        # Without the bonus, the efficient equilibrium IS
        # the maximum possible surplus.
        group.theo_max_surplus = efficient_surplus

    # Actual Surplus
    actual_priv_surplus = sum(b.value - s.cost for b, s in zip(buyers[:q_star], sellers[:q_star]))
    group.actual_total_surplus = actual_priv_surplus + (len(players) * bonus)

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
            'halfRound':(C.NUM_ROUNDS // 2)
        }

class RoleSwitch(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == ((C.NUM_ROUNDS // 2) + 1)

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'roundNum': player.round_number,
            'numRounds': C.NUM_ROUNDS,
            'halfRound': (C.NUM_ROUNDS // 2),
            'is_last_round_of_role': player.round_number == ((C.NUM_ROUNDS // 2) + 1)
        }


class Submission(Page):
    form_model = 'player'

    @staticmethod
    def get_form_fields(player):
        return ['bid'] if player.is_buyer else ['ask']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'roundNum': player.round_number,
            'is_last_round_of_role': player.round_number == ((C.NUM_ROUNDS // 2) + 1)
        }

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    form_model = 'player'

    def get_form_fields(player):
        return ['justification'] if player.round_number == 1 else []

    @staticmethod
    def justification_error_message(player, value):
        # value is the raw input from the form
        if not value or not value.strip():
            return "Please provide a valid explanation. Your response cannot be empty or just spaces."

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        all_players = group.get_players()

        bonus_triggered = group.treatment == 'competitive' and group.all_bought
        bonus_amount = C.BONUS_POINTS if bonus_triggered else 0

        # 1. Build Buyer Data List
        buyer_data = []
        for p in all_players:
            if p.is_buyer:
                buyer_data.append({
                    'val': p.bid,
                    'is_me': p.id_in_group == player.id_in_group,
                    'private': p.value,
                })
        sorted_buyers = sorted(buyer_data, key=lambda x: x['val'], reverse=True)

        # 2. Build Seller Data List
        seller_data = []
        for p in all_players:
            if not p.is_buyer:
                seller_data.append({
                    'val': p.ask,
                    'is_me': p.id_in_group == player.id_in_group,
                    'private': p.cost,
                })
        sorted_sellers = sorted(seller_data, key=lambda x: x['val'])

        # 3. Dynamic wording based on current role
        term = "bid" if player.is_buyer else "ask"
        dynamic_label = f"Can you please explain your reasoning for your {term} and explain if or how you would have changed your {term}?"

        # 4. Loss detection (Negative payoff only if they traded)
        is_loss = player.is_trader and player.payoff < 0

        return {
            'zipped_data': zip(sorted_buyers, sorted_sellers),
            'is_loss': is_loss,
            'dynamic_label': dynamic_label,
            'term': term,
            'bonus_triggered': bonus_triggered,
            'trading_profit': round(player.trading_profit,2),
            'bonus_amount': bonus_amount,
        }

class Summary(Page):
    # Only show this on the very last round
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    @staticmethod
    def vars_for_template(player: Player):
        group = player.group
        # 1. Calculate Total Profits for the Leaderboard
        all_players = group.get_players()
        leaderboard = []

        for p in all_players:
            name_to_display = p.in_round(1).field_maybe_none('player_name') or f"Player {p.id_in_group}"
            # Sum payoffs across all rounds for this specific participant
            total_payoff = sum([prev_p.payoff for prev_p in p.in_all_rounds()])
            leaderboard.append({
                'id': p.id_in_group,
                'name': name_to_display,
                'total_profit': total_payoff,
                'is_me': p.id_in_group == player.id_in_group
            })

        # Sort leaderboard by profit descending
        leaderboard.sort(key=lambda x: x['total_profit'], reverse=True)

        # 2. Existing Round History Logic
        group_history = []
        for g in player.group.in_all_rounds():
            # Define local variables needed for this loop
            round_players = g.get_players()
            num_players = len(round_players)  # FIXED: Definition of num_players

            vals = sorted([p.value for p in round_players if p.is_buyer], reverse=True)
            costs = sorted([p.cost for p in round_players if not p.is_buyer])
            bids = sorted([p.bid for p in round_players if p.is_buyer], reverse=True)
            asks = sorted([p.ask for p in round_players if not p.is_buyer])

            # Recalculate theoretical surplus for summary
            efficient_surplus = sum(
                v - c
                for v, c in zip(vals, costs)
                if v >= c
            )
            if g.treatment == 'competitive':
                all_trade_surplus = sum(
                    v - c
                    for v, c in zip(vals, costs)
                )
                max_surplus = all_trade_surplus + (num_players * C.BONUS_POINTS)
            else:
                max_surplus = efficient_surplus


            theo_q = 0
            for v, c in zip(vals, costs):
                if v >= c:
                    theo_q += 1
                else:
                    break

            theo_p = (vals[theo_q - 1] + costs[theo_q - 1]) / 2 if theo_q > 0 else 0

            group_history.append({
                'round': g.round_number,
                'treatment': g.treatment,
                'theo_p': theo_p,
                'theo_q': theo_q,
                'actual_bids': bids,
                'actual_asks': asks,
                'actual_p': g.market_price,
                'actual_q': g.quantity,
                'theo_total_surplus': round(efficient_surplus, 2),
                'theo_max_surplus': round(max_surplus, 2),
                'actual_total_surplus': round(g.actual_total_surplus, 2),
                'all_bought': g.all_bought,
                'bonus_pool': num_players * C.BONUS_POINTS,  # Now num_players is defined
                'theo_vals': vals,
                'theo_costs': costs,
            })

        return {
            'leaderboard': leaderboard,
            'history': group_history
        }

page_sequence = [Instructions, RoleSwitch, Submission, ResultsWaitPage, Results, Summary]