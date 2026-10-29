#  Rylee Rosenlieb
#  Social Science Experimental Laboratory
#  Trade Deal Experiment
#  Last Updated Date: 15 October, 2026

from otree.api import *
import time


doc = """
Your app description
"""


class C(BaseConstants):
    NAME_IN_URL = 'tradeDealGame'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    AUTARKY_UTILITY = 15


class Subsession(BaseSubsession):
    @staticmethod
    def group_by_arrival_time_method(subsession, waiting_players):
        #check that two players are waiting
        if len(waiting_players) >= 2:
            return waiting_players[:2]

        now = time.time()
        for p in waiting_players:
            arrival = p.participant.vars.get('arrival_time')

            if arrival and now - arrival > 120:
                p.timed_out = True
                return[p]

        return None


class Group(BaseGroup):
    #define group variables -> trade deal within the groups
    c1_clothes_export = models.IntegerField()
    c1_food_export = models.IntegerField()

    c2_clothes_export = models.IntegerField()
    c2_food_export = models.IntegerField()

    negotiation_start_time = models.FloatField(initial=0)

    def set_trade_outcome(self):
        p1 = next(p for p in self.get_players() if p.country == 1)
        p2 = next(p for p in self.get_players() if p.country == 2)

        self.c1_clothes_export = p1.clothes_export
        self.c1_food_export = p1.food_export

        self.c2_clothes_export = p2.clothes_export
        self.c2_food_export = p2.food_export

    def set_participation_point(self):
        p1 = next(p for p in self.get_players() if p.country == 1)
        p2 = next(p for p in self.get_players() if p.country == 2)

        p1_benefits = check_total_utility(p1)
        p2_benefits = check_total_utility(p2)

        if p1_benefits and p2_benefits:
            p1.participation_point = 1
            p2.participation_point = 1

    def get_trade_summary(self):

        def extract(export_clothes, export_food):
            exports = []
            if export_clothes > 0:
                exports.append(dict(good="clothes", qty=export_clothes))
            if export_food > 0:
                exports.append(dict(good="food", qty=export_food))

            for i, item in enumerate(exports):
                item['unit_word'] = 'unit' if item['qty'] == 1 else 'units'
                item['sep'] = ' and ' if i < len(exports) - 1 else ''
            return exports

        return dict(
            c1_exports=extract(self.c1_clothes_export, self.c1_food_export),
            c2_exports=extract(self.c2_clothes_export, self.c2_food_export),
        )



def get_production_plan(player):
    if player.country == 1:
        production_plan = {
        1:[10, 0],
        2:[8,1],
        3:[6, 2],
        4:[4,3],
        5:[2,4],
        6:[0,5]
        }
    else:
        production_plan = {
        1:[0,15],
        2:[1,12],
        3:[2,9],
        4:[3,6],
        5:[4,3],
        6:[5,0] 
        }
    return production_plan

def check_total_utility(player):
    trade_utility = 5 * min(player.total_clothes, player.total_food)
    autarky_utility = get_autarky_utility(player)

    return trade_utility > autarky_utility

def get_autarky_utility(player):
    plan = get_production_plan(player)

    best = 0
    for values in plan.values():
        clothes, food = values
        utility = 5 * min(clothes, food)
        best = max(best, utility)

    return best





# =========================================================
# PLAYER CLASS
# =========================================================
class Player(BasePlayer):
    player_name = models.StringField()
    email_address = models.StringField(blank=True) #for SSEL participant pool purposes
    country = models.IntegerField(choices=[1, 2]) #each player either represents country 1 or country 2
    participation_point = models.IntegerField(initial = 0) #participation point 
    autarky_plan = models.IntegerField(choises = [1,2,3,4,5,6])
    selected_plan = models.IntegerField(choices = [1,2,3,4,5,6])
    clothes_import = models.IntegerField(initial = 0)
    clothes_export = models.IntegerField(initial = 0)
    food_import = models.IntegerField(initial = 0)
    food_export = models.IntegerField(initial = 0)
    total_clothes = models.IntegerField()
    total_food = models.IntegerField()
    timed_out = models.BooleanField(initial=False)


    # =========================================================
    # SURVEY VARIABLES
    # =========================================================
    survey_q1 = models.IntegerField(
        choices=[1,2],
        blank=True,   # allow field to be blank in forms
        null=True     # allow field to be None in database
    )
    survey_q2 = models.IntegerField(
        choices=[1,2],
        blank=True,
        null=True
    )
    survey_q3 = models.IntegerField(
        choices=[1,2],
        blank=True,
        null=True
    )

# PAGES

class WaitForPartner(WaitPage):
    group_by_arrival_time = True
    body_text = "Waiting for another participant to join..."
    template_name = 'tradeDealGame/WaitForPartner.html'
    timeout_seconds = 90  # 2 minutes

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1  # only final round

    @staticmethod
    def vars_for_template(player):
        if 'arrival_time' not in player.participant.vars:
            player.participant.vars['arrival_time'] = time.time()

    @staticmethod
    def after_all_players_arrive(group: Group):
        for i, player in enumerate(group.get_players()):
            player.country = i + 1


class Pre_Introduction(Page):
    form_model = 'player'
    form_fields = ['email_address']

    @staticmethod
    def is_displayed(player):
        return player.round_number == 1 #only display this page to start


class CouldNotPair(Page):
    @staticmethod
    def is_displayed(player):
        # Only show if the player timed out waiting for a partner
        return player.timed_out


class Instructions(Page):
    form_model = 'player'
    form_fields = ['player_name']

    @staticmethod
    def error_message(player, values):
        name = values.get('player_name')

        if not name or name.strip() == "":
            return "Please enter your name before continuing."

class AutarkyDecision(Page):
    form_model = 'player'
    form_fields = ['autarky_plan']  # reuse or create autarky_plan

    @staticmethod
    def vars_for_template(player):
        raw_plan = get_production_plan(player)

        plan_table = []
        for plan_num, values in raw_plan.items():
            plan_table.append({
                'plan': plan_num,
                'clothes': values[0],
                'food': values[1]
            })

        return dict(
            country=player.country,
            plan_table=plan_table,
        )

    @staticmethod
    def live_method(player, data):
        selected_plan = int(data['autarky_plan'])

        plan = get_production_plan(player)
        clothes = plan[selected_plan][0]
        food = plan[selected_plan][1]

        utility = 5 * min(clothes, food)

        return {
            player.id_in_group: {
                'utility': utility
            }
        }

class WaitToStart(WaitPage):
    body_text = "Waiting for your partner to be ready..."

    @staticmethod
    def after_all_players_arrive(group: Group):
        group.negotiation_start_time = time.time()

class NegotiationPage(Page):
    form_model = 'player'
    form_fields = [
    'selected_plan',
    'clothes_export',
    'clothes_import',
    'food_export',
    'food_import']

    @staticmethod
    def vars_for_template(player):
        # Get the raw production plan dictionary
        raw_plan = get_production_plan(player)

        # Convert to a list of dictionaries for template rendering
        plan_table = []
        for plan_num, values in raw_plan.items():
            plan_table.append({
                'plan': plan_num,
                'clothes': values[0],
                'food': values[1]
            })

        # Optional: a nickname for chat
        nickname = f"Country {player.country}"

        duration = 300  # seconds
        deadline_ms = int((player.group.negotiation_start_time + duration) * 1000)

        return dict(
            country=player.country,
            plan_table=plan_table,
            nickname = nickname,
            deadline_ms=deadline_ms
        )

    @staticmethod
    def before_next_page(player, timeout_happened):
        plan = get_production_plan(player)
        selected = player.selected_plan

        clothes = plan[selected][0]
        food = plan[selected][1]

        player.total_clothes = clothes - player.clothes_export + player.clothes_import
        player.total_food = food - player.food_export + player.food_import

    @staticmethod
    def error_message(player, values):
        plan = get_production_plan(player)
        selected = int(values['selected_plan'])

        clothes_produced = plan[selected][0]
        food_produced = plan[selected][1]

        clothes_export = values['clothes_export']
        food_export = values['food_export']

        if clothes_export > clothes_produced:
            return f"You cannot export more clothes ({clothes_export}) than you produce ({clothes_produced})."

        if food_export > food_produced:
            return f"You cannot export more food ({food_export}) than you produce ({food_produced})."

    @staticmethod
    def live_method(player, data):
        selected_plan = int(data['selected_plan'])
        clothes_import = int(data['clothes_import'])
        clothes_export = int(data['clothes_export'])
        food_import = int(data['food_import'])
        food_export = int(data['food_export'])

        plan = get_production_plan(player)
        clothes = plan[selected_plan][0]
        food = plan[selected_plan][1]

        if clothes_export > clothes:
            return {player.id_in_group: {
                'error': f"Clothes export exceeds production ({clothes})"
            }}

        if food_export > food:
            return {player.id_in_group: {
                'error': f"Food export exceeds production ({food})"
            }}

        total_clothes = clothes - clothes_export + clothes_import
        total_food = food - food_export + food_import

        utility = 5 * min(total_clothes, total_food)

        return {player.id_in_group: {'utility': utility, 'error': None}}




class ResultsWaitPage(WaitPage):
    @staticmethod

#also compute autarky here within the groups
    def after_all_players_arrive(group: Group):
        group.set_trade_outcome()
        group.set_participation_point()




class TradeDeal(Page):
    @staticmethod
    def vars_for_template(player):
        g = player.group
        summary = g.get_trade_summary()

        def trade_utility(p):
            return 5 * min(p.total_clothes, p.total_food)

        def autarky_utility(p):
            return get_autarky_utility(p)

        players = g.get_players()

        both_benefit = all(
            trade_utility(p) > autarky_utility(p)
            for p in players
        )

        return dict(
            **summary,
            both_benefit=both_benefit
        )


class ThankYou(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS  # only final round


page_sequence = [
WaitForPartner,
Pre_Introduction,
CouldNotPair,
Instructions,
AutarkyDecision,
WaitToStart,
NegotiationPage,
ResultsWaitPage, 
TradeDeal, 
ThankYou]
