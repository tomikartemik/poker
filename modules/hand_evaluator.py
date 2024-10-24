from poker import Card, Evaluator

class HandStrengthEvaluator:
    def __init__(self):
        self.evaluator = Evaluator()
        
    def evaluate_hand(self, player_cards, community_cards):
        if not community_cards:  # Префлоп
            return self._evaluate_preflop(player_cards)
            
        hand = [Card.new(card) for card in player_cards]
        board = [Card.new(card) for card in community_cards]
        
        score = self.evaluator.evaluate(hand, board)
        return 1 - (score / 7462)  # Нормализация от 0 до 1
        
    def _evaluate_preflop(self, cards):
        # Оценка префлоп руки
        card1, card2 = cards
        rank1, suit1 = card1[0], card1[1]
        rank2, suit2 = card2[0], card2[1]
        
        # Базовая оценка для пар
        if rank1 == rank2:
            return self._pair_strength(rank1)
            
        # Одномастные карты
        suited = suit1 == suit2
        return self._unpaired_strength(rank1, rank2, suited)
