from math_model import PokerMath
from ml_analyzer import PokerMLAnalyzer
from decision_maker import DecisionMaker
from hand_evaluator import HandStrengthEvaluator


class GameState:
    def __init__(self):
        self.players_actions = {}
        self.current_bet = 0
        self.pot_size = 0
        self.player_hand = []  # Карты игрока
        self.table_cards = []  # Карты на столе
        self.community_cards = []  # карты на столе
        self.stage = "preflop"  # текущая стадия игры
        self.math_model = PokerMath()
        self.stack_size = 1000  # Начальный стек
        self.ml_analyzer = PokerMLAnalyzer()
        self.hand_evaluator = HandStrengthEvaluator()
        self.decision_maker = DecisionMaker(self.ml_analyzer, self.hand_evaluator)
        
    def set_player_hand(self, cards):
        self.player_hand = cards

    def set_table_cards(self, cards):
        self.table_cards = cards

    def update_game_state(self, data):
        # Обновление стадии игры и карт на столе
        if "stage" in data:
            self.stage = data["stage"]

        if "community_cards" in data:
            self.community_cards = data["community_cards"]

        # Обновление действий игроков
        if "actions" in data:
            self.actions = data["actions"]

    def update_actions_from_chat(self, chat_data):
        for message in chat_data:
            player_id, action = self.parse_message(message)
            if player_id and action:
                self.update_actions(player_id, action)

    def parse_message(self, message):
        # Проверяем каждое сообщение на наличие действий из списка
        player_id = self.extract_player_id(message)
        if "делает фолд" in message:
            return player_id, 'fold'
        elif "делает чек" in message:
            return player_id, 'check'
        elif "уравнивает" in message and "и идет ва-банк" in message:
            return player_id, 'call_and_all_in'
        elif "уравнивает" in message:
            return player_id, 'call'
        elif "ставит малый блайнд" in message:
            return player_id, 'small_blind'
        elif "ставит большой блайнд" in message:
            return player_id, 'big_blind'
        elif "повышает на" in message:
            return player_id, 'raise'
        elif "идет ва-банк" in message:
            return player_id, 'all_in'
        elif "не показывает карты" in message:
            return player_id, 'no_show'
        elif "показывает комбинацию" in message:
            return player_id, 'show_combination'
        elif "использует резерв времени" in message:
            return player_id, 'time_bank'
        elif "выигрывает" in message and "из главного банка" in message:
            return player_id, 'win_pot'
        elif "получает обратно неуравненную ставку" in message:
            return player_id, 'return_unmatched_bet'
        elif "раздаются карты" in message:
            return player_id, 'deal_cards'
        elif "флоп" in message:
            return player_id, 'flop'
        elif "ривер" in message:
            return player_id, 'river'
        elif "тёрн" in message:
            return player_id, 'turn'
        elif "докупает" in message:
            return player_id, 'rebuy'
        return None, None

    def extract_player_id(self, message):
        return f"игрок {len(self.players_actions) + 1}"

    def update_actions(self, player_id, action):
        if player_id not in self.players_actions:
            self.players_actions[player_id] = {
                'fold': 0, 'check': 0, 'call': 0, 'raise': 0, 'all_in': 0,
                'small_blind': 0, 'big_blind': 0, 'no_show': 0, 'show_combination': 0,
                'time_bank': 0, 'win_pot': 0, 'return_unmatched_bet': 0, 
                'deal_cards': 0, 'flop': 0, 'river': 0, 'turn': 0, 'rebuy': 0
            }
        
        if action in self.players_actions[player_id]:
            self.players_actions[player_id][action] += 1

    def get_summary(self):
        return self.players_actions

    def analyze_strategy(self):
        decision = self.decision_maker.make_decision(self)
        return {
            'recommended_action': decision['action'],
            'bet_size': decision['bet_size'],
            'win_probability': decision['win_probability'],
            'opponent_analysis': decision['opponent_profiles']
        }
