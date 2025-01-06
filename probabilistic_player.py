from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 10000

class ProbabilisticPlayer(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        pot = round_state['pot']['main']['amount']
        to_call = valid_actions[1]['amount'] if valid_actions[1]['action'] == 'call' else 0

        if len(community_card) == 0:  # Préflop
            action = self.preflop_decision(valid_actions, hole_card, to_call)
        else:  # Postflop (Flop, Turn, River)
            action = self.postflop_decision(valid_actions, hole_card, community_card, pot, to_call)

        return action['action'], action.get('amount', 0)

    def preflop_decision(self, valid_actions, hole_card, to_call):
        # Simplified hand strength evaluation (pairs, high cards)
        strong_hands = ["AA", "KK", "QQ", "JJ", "TT", "AKs", "AQs", "KQs"]  # Add more as needed
        hand = "".join(sorted([c[1] for c in hole_card]))  # Extract ranks (e.g., "AK")
        suited = hole_card[0][0] == hole_card[1][0]  # Check if suited

        if hand in strong_hands or (hand == "AK" and suited):
            action = valid_actions[2]  # raise
            min_raise = action['amount']['min']
            max_raise = action['amount']['max']
            action['amount'] = min(int(min_raise * 2.5), max_raise)
        elif to_call > 0:  # Call only if the cost is low
            action = valid_actions[1] if to_call <= 0.1 * self.stack else valid_actions[0]
        else:
            action = valid_actions[1]  # call/check

        return action

    def postflop_decision(self, valid_actions, hole_card, community_card, pot, to_call):
        # Calculate win rate
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )

        # Calculate pot odds
        pot_odds = to_call / (pot + to_call) if to_call > 0 else 0

        # Decision-making
        if to_call > 0 and win_rate < pot_odds:
            action = valid_actions[0]  # fold
        elif win_rate > 0.75:
            action = valid_actions[2]  # raise
            min_raise = action['amount']['min']
            max_raise = action['amount']['max']
            action['amount'] = min(int(min_raise * 2.5), max_raise)
        else:
            action = valid_actions[1]  # call/check

        return action

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']
        self.stack = game_info['rule']['initial_stack']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass