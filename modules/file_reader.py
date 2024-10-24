# modules/file_reader.py

import json
import time
import os

class FileReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.last_position = 0

    def read_updates(self):
        if not os.path.exists(self.filepath):
            return []

        with open(self.filepath, 'r') as file:
            # Пропускаем уже прочитанные данные
            file.seek(self.last_position)
            new_data = file.read()
            self.last_position = file.tell()

        if new_data.strip():
            try:
                return json.loads(new_data)
            except json.JSONDecodeError:
                print("Ошибка разбора JSON")
                return []

        return []

# Пример использования
if __name__ == "__main__":
    filepath = "game_updates.json"
    file_reader = FileReader(filepath)

    while True:
        updates = file_reader.read_updates()
        if updates:
            print("Новые действия:", updates)
        time.sleep(1)  # Пауза между проверками
