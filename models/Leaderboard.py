import sqlite3
import os.path

from models.Score import Score


class Leaderboard:
    def __init__(self):
        self.__file_path = os.path.join('databases', 'leaderboard.txt')
        self.check_file()  # Kontrolli faili olemasolu ja kui pole, siis tee

    def check_file(self):
        """Kontrollib, kas fail eksisteerib. Kui ei, siis loob selle."""
        if not os.path.exists(self.__file_path):
            self.create_leaderboard()

    def create_leaderboard(self):
        """Loob edetabeli faili koos päisega."""
        header = ['name', 'word', 'letters', 'game length', 'game time']
        with open(self.__file_path, 'a', encoding='utf-8') as f:
            f.write(';'.join(header) + '\n')

    def read_leaderboard(self):
        """Loeb edetabeli andmed tekstifailist."""
        leaderboard = []
        with open(self.__file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            if not lines:
                return []  # Kui fail on tühi, tagastatakse tühi list

            for line in lines[1:]:
                line = line.strip()  # Korrasta read
                name, word, letters, game_length, game_time = line.split(';')
                leaderboard.append(Score(name, word, letters, int(game_length), game_time))

            leaderboard = sorted(leaderboard, key=lambda x: (x.game_length, len(x.letters.split(', '))))  # Sorteeri kestvuse järgi

        return leaderboard

    def add_entry(self, name, word, letters, game_length, game_time):
        """Lisab kirje edetabelisse nii andmebaasi kui ka faili."""
        # Andmebaasi uuendamine
        with sqlite3.connect('databases/hangman_2025.db') as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES (?, ?, ?, ?, ?)",
                (name, word, letters, game_length, game_time)
            )
            conn.commit()

        # Faili uuendamine
        with open(self.__file_path, 'a', encoding='utf-8') as f:
            f.write(f"{name};{word};{letters};{game_length};{game_time}\n")

    # Getter
    @property
    def file_path(self):
        return self.__file_path
