from otree.api import *
import random

doc = """
Uniform-Price Double Auction Experiment.
"""

class C(BaseConstants):
    NAME_IN_URL = 'uniform_double_auction'
    PLAYERS_PER_GROUP = None  # Flexible number of players
    NUM_ROUNDS = 10 # Total rounds
    BUYER_VAL_RANGE = [30, 80] 
    SELLER_COST_RANGE = [10, 50]

class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    market_price = models.FloatField()
    quantity = models.IntegerField()

class Player(BasePlayer):
    is_buyer = models.BooleanField()
    value = models.IntegerField()
    cost = models.IntegerField()
    bid = models.FloatField(min=0)
    ask = models.FloatField(min=0)
    is_trader = models.BooleanField(initial=False)
    justification = models.LongStringField()
    player_name = models.StringField(label="Please enter your player name:")

# --- LOGIC ---

def creating_session(subsession: Subsession):
    if subsession.round_number == 1:
        # Initial random role assignment
        for g in subsession.get_groups():
            players = g.get_players()
            random.shuffle(players)
            for i, p in enumerate(players):
                p.participant.is_buyer = i < len(players) / 2
    
    for p in subsession.get_players():
        # Switch roles after 5 rounds 
        if subsession.round_number <= 5:
            p.is_buyer = p.participant.is_buyer
        else:
            p.is_buyer = not p.participant.is_buyer
            
        # Assign private parameters
        # Note: Ensure no two players have same values 
        if p.is_buyer:
            p.value = random.randint(*C.BUYER_VAL_RANGE)
            p.ask = 0 # Placeholder
        else:
            p.cost = random.randint(*C.SELLER_COST_RANGE)
            p.bid = 0 # Placeholder

    for g in subsession.get_groups():
        players = g.get_players()
        buyers = [p for p in players if p.is_buyer]
        sellers = [p for p in players if not p.is_buyer]

        if buyers:
            buyers[-1].value = 5  # Too low to trade
        if sellers:
            sellers[-1].cost = 95

def set_payoffs(group: Group):
    players = group.get_players()
    # Sort bids descending, asks ascending
    bids_players = sorted([p for p in players if p.is_buyer], key=lambda p: p.bid, reverse=True)
    asks_players = sorted([p for p in players if not p.is_buyer], key=lambda p: p.ask)
    
    bids = [p.bid for p in bids_players]
    asks = [p.ask for p in asks_players]
    
    # Calculate Q*
    q_star = 0
    for b, a in zip(bids, asks):
        if b >= a:
            q_star += 1
        else:
            break
    
    group.quantity = q_star
    
    if q_star > 0:
        # Market Price P* = (b_Q* + a_Q*) / 2 
        group.market_price = (bids[q_star-1] + asks[q_star-1]) / 2
        
        # Assign trading status and payoffs
        for i, p in enumerate(bids_players):
            if i < q_star:
                p.is_trader = True
                p.payoff = p.value - group.market_price
            else:
                p.payoff = 0
                
        for i, p in enumerate(asks_players):
            if i < q_star:
                p.is_trader = True
                p.payoff = group.market_price - p.cost
            else:
                p.payoff = 0
    else:
        group.market_price = 0
        group.quantity = 0
        for p in players:
            p.payoff = 0

# --- PAGES ---

class Instructions(Page):
    form_model = 'player'
    form_fields = ['player_name']

    def is_displayed(player: Player):
        return player.round_number == 1

    def vars_for_template(player: Player):
        return {
            'numRounds': C.NUM_ROUNDS
        }

class Submission(Page):
    form_model = 'player'
    def get_form_fields(player):
        return ['bid'] if player.is_buyer else ['ask']

    def vars_for_template(player: Player):
        return {
            'roundNum': player.round_number,
            'is_last_round_of_role': player.round_number == 5
        }

class ResultsWaitPage(WaitPage):
    after_all_players_arrive = set_payoffs


class Results(Page):
    form_model = 'player'

    def get_form_fields(player):
        if player.round_number == 1:
            return ['justification']
        return []

    def vars_for_template(player: Player):
        group = player.group
        all_players = group.get_players()

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
            'term': term
        }

class Summary(Page):
    # Only show this on the very last round
    def is_displayed(player: Player):
        return player.round_number == C.NUM_ROUNDS

    def vars_for_template(player: Player):
        group = player.group
        # 1. Calculate Total Profits for the Leaderboard
        all_players = group.get_players()
        leaderboard = []

        for p in all_players:
            name_to_display = p.in_round(1).player_name
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
            players = g.get_players()
            vals = sorted([p.value for p in players if p.is_buyer], reverse=True)
            costs = sorted([p.cost for p in players if not p.is_buyer])
            bids = sorted([p.bid for p in players if p.is_buyer], reverse=True)
            asks = sorted([p.ask for p in players if not p.is_buyer])

            theo_q = 0
            for v, c in zip(vals, costs):
                if v >= c:
                    theo_q += 1
                else:
                    break
            theo_p = (vals[theo_q - 1] + costs[theo_q - 1]) / 2 if theo_q > 0 else 0

            group_history.append({
                'round': g.round_number,
                'theo_p': theo_p, 'theo_q': theo_q,
                'actual_bids': bids, 'actual_asks': asks,
                'actual_p': g.market_price, 'actual_q': g.quantity,
                'theo_vals': vals, 'theo_costs': costs,
            })

        return {
            'leaderboard': leaderboard,
            'history': group_history
        }

page_sequence = [Instructions, Submission, ResultsWaitPage, Results, Summary]
