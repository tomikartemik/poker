class DecisionMaker:
    def __init__(self, ml_analyzer, hand_evaluator):
        self.ml_analyzer = ml_analyzer
        self.hand_evaluator = hand_evaluator
        
    def make_decision(self, game_state):
        hand_strength = self.hand_evaluator.evaluate_hand(
            game_state.player_hand,
            game_state.community_cards
        )
        
        opponent_profiles = {
            player_id: self.ml_analyzer.analyze_opponent(player_id, actions)
            for player_id, actions in game_state.players_actions.items()
        }
        
        win_probability = self.ml_analyzer.predict_win_probability(
            game_state,
            hand_strength,
            opponent_profiles
        )
        
        return self._calculate_optimal_action(
            win_probability,
            game_state.pot_size,
            game_state.stack_size,
            game_state.current_bet
        )
