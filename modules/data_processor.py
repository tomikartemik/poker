import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

class PokerDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.feature_columns = [
            'position', 'pot_size', 'stack_size', 'bet_to_call',
            'previous_action', 'player_aggression', 'hand_strength'
        ]
        
    def prepare_training_data(self, raw_data):
        df = pd.DataFrame(raw_data)
        X = df[self.feature_columns]
        y = df['action_result']  # 1 для выигрыша, 0 для проигрыша
        
        X_scaled = self.scaler.fit_transform(X)
        return X_scaled, y
        
    def extract_features(self, game_state, player_id):
        return {
            'position': self._encode_position(game_state.position),
            'pot_size': game_state.pot_size / game_state.stack_size,
            'stack_size': game_state.stack_size,
            'bet_to_call': game_state.current_bet,
            'previous_action': self._encode_last_action(game_state, player_id),
            'player_aggression': self._calculate_aggression(game_state, player_id),
            'hand_strength': self._evaluate_hand_strength(game_state.player_hand, game_state.community_cards)
        }
