# main.py

from src.screen_capture import capture_screen
from src.image_processing import process_image
from src.decision_engine import analyze_game_state


def main():
    # Захват экрана
    img = capture_screen()

    # Обработка изображения (распознавание карт и других элементов)
    recognized_text = process_image(img)

    # Логика принятия решений (для теста пока просто выводим)
    decision = analyze_game_state([], [], 0, [])

    print(f"Распознанный текст: {recognized_text}")
    print(f"Рекомендация: {decision}")


if __name__ == "__main__":
    main()
