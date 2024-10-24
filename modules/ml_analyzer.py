import numpy as np
from sklearn.ensemble import RandomForestClassifier
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import joblib

class PokerMLAnalyzer:
    def __init__(self):
        self.rf_model = self._load_or_create_rf_model()
        self.nn_model = self._load_or_create_nn_model()
        self.data_processor = PokerDataProcessor()
        
    def _load_or_create_rf_model(self):
        try:
            return joblib.load('models/rf_model.joblib')
        except:
            return RandomForestClassifier(n_estimators=100)
            
    def _load_or_create_nn_model(self):
        try:
            return keras.models.load_model('models/nn_model.h5')
        except:
            return self._create_nn_model()
            
    def train_models(self, training_data):
        X, y = self.data_processor.prepare_training_data(training_data)
        
        # Обучение Random Forest
        self.rf_model.fit(X, y)
        
        # Обучение нейронной сети
        self.nn_model.fit(X, y, epochs=50, batch_size=32, validation_split=0.2)
        
        # Сохранение моделей
        joblib.dump(self.rf_model, 'models/rf_model.joblib')
        self.nn_model.save('models/nn_model.h5')
        
    def analyze_opponent(self, player_id, actions_history):
        features = self.data_processor.extract_features(actions_history)
        
        return {
            'aggression_score': self._calculate_aggression_score(features),
            'bluff_probability': self._estimate_bluff_probability(features),
            'betting_patterns': self._analyze_betting_patterns(features)
        }
        
    def recommend_action(self, game_state, opponent_profiles):
        current_features = self._create_game_state_features(game_state)
        win_probability = self.nn_model.predict([current_features])[0][0]
        
        if win_probability > 0.7:
            bet_size = self._calculate_optimal_bet(game_state, win_probability)
            return f"Рекомендуется повысить на {bet_size}"
        elif win_probability > 0.4:
            return f"Рекомендуется уравнять {game_state.current_bet}"
        else:
            return "Рекомендуется сбросить карты"
