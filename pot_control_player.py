from pypokerengine.players import BasePokerPlayer
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate

NB_SIMULATION = 10000

class PotControlPlayer(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
            nb_simulation=NB_SIMULATION,
            nb_player=self.nb_player,
            hole_card=gen_cards(hole_card),
            community_card=gen_cards(community_card)
        )
        pot = round_state['pot']['main']['amount']
        to_call = valid_actions[1]['amount'] if valid_actions[1]['action'] == 'call' else 0

        if win_rate > 0.8:  # Push aggressively with strong hands
            action = valid_actions[2]  # raise
            min_raise = action['amount']['min']
            max_raise = action['amount']['max']
            action['amount'] = min(int(min_raise * 3), max_raise)
        elif 0.4 < win_rate <= 0.8:  # Keep pot small with marginal hands
            action = valid_actions[1] if to_call <= 0.1 * pot else valid_actions[0]  # call or fold
        else:  # Fold weak hands
            action = valid_actions[0]

        return action['action'], action.get('amount', 0)

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass