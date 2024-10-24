# main.py

from file_reader import FileReader
from game_analysis import GameState
import time

def process_game_updates(filepath):
    game_state = GameState()
    file_reader = FileReader(filepath)

    while True:
        updates = file_reader.read_updates()
        if updates:
            game_state.update_game_state(updates)  # Обновляем состояние игры
            print(game_state.get_summary())  # Выводим текущее состояние игры

            strategy_analysis = game_state.analyze_strategy()  # Анализируем стратегию
            print("Рекомендация:", strategy_analysis)
        time.sleep(1)  # Пауза между проверками

if __name__ == "__main__":
    filepath = "game_updates.json"
    process_game_updates(filepath)
