import sqlite3
import os

# Andmebaasi asukoht
DB_FOLDER = "databases"
DB_NAME = "hangman_2025.db"
DATABASE_PATH = os.path.join(DB_FOLDER, DB_NAME)

# TXT-failide asukoht
WORDS_FILE = os.path.join(DB_FOLDER, "words.txt")
LEADERBOARD_FILE = os.path.join(DB_FOLDER, "leaderboard.txt")


class Database:
    def __init__(self):
        """Algatab andmebaasiühenduse ja tagab, et vajalikud tabelid on olemas."""
        self.create_database()

    def create_database(self):
        """Kontrollib, kas andmebaas eksisteerib. Kui ei, siis loob selle ja impordib andmed."""
        if not os.path.exists(DATABASE_PATH):
            print(f"Database '{DATABASE_PATH}' does not exist. Creating a new database.")
            os.makedirs(DB_FOLDER, exist_ok=True)
            self.create_tables()
            self.import_data()
        else:
            self.create_tables()

    def create_tables(self):
        """Loob vajalikud tabelid, kui neid ei eksisteeri."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            # Words tabel
            cursor.execute('''CREATE TABLE IF NOT EXISTS words (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                word TEXT NOT NULL,
                category TEXT NOT NULL
            )''')

            # Leaderboard tabel
            cursor.execute('''CREATE TABLE IF NOT EXISTS leaderboard (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                word TEXT NOT NULL,
                letters TEXT,
                game_length INTEGER NOT NULL,
                game_time TEXT NOT NULL
            )''')

            conn.commit()

    @staticmethod
    def import_data():
        """Impordib andmed words.txt ja leaderboard.txt failidest, kui need eksisteerivad."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()

            # Import words.txt
            if os.path.exists(WORDS_FILE):
                with open(WORDS_FILE, "r", encoding="utf-8") as file:
                    next(file)  # Jäta esimene rida vahele (päis)
                    for line in file:
                        parts = line.strip().split(";")
                        if len(parts) == 2:
                            word, category = parts
                            cursor.execute("INSERT INTO words (word, category) VALUES (?, ?)", (word, category))
                print("Words imported successfully.")

            # Import leaderboard.txt
            if os.path.exists(LEADERBOARD_FILE):
                with open(LEADERBOARD_FILE, "r", encoding="utf-8") as file:
                    next(file)  # Jäta esimene rida vahele (päis)
                    for line in file:
                        parts = line.strip().split(";")
                        if len(parts) == 5:
                            name, word, letters, game_length, game_time = parts
                            cursor.execute(
                                "INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES (?, ?, ?, ?, ?)",
                                (name, word, letters, int(game_length), game_time))
                print("Leaderboard imported successfully.")

            conn.commit()

    @staticmethod
    def get_random_word():
        """Tagastab juhusliku sõna koos kategooriaga."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT word, category FROM words ORDER BY RANDOM() LIMIT 1")
            return cursor.fetchone()

    @staticmethod
    def get_all_categories():
        """Tagastab kõik unikaalsed kategooriad."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT category FROM words")
            return [row[0] for row in cursor.fetchall()]

    @staticmethod
    def get_leaderboard():
        """Tagastab kogu edetabeli andmed."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name, word, letters, game_length, game_time FROM leaderboard ORDER BY game_time DESC")
            return cursor.fetchall()

    @staticmethod
    def add_leaderboard_entry(name, word, letters, game_length, game_time):
        """Lisab uue kirje edetabelisse."""
        with sqlite3.connect(DATABASE_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO leaderboard (name, word, letters, game_length, game_time) VALUES (?, ?, ?, ?, ?)",
                (name, word, letters, game_length, game_time))
            conn.commit()


# Kontrollime, kas andmebaas eksisteerib ja kas words tabel on tühi
def validate_database():
    if not os.path.exists(DATABASE_PATH):
        print("Database is missing. Application cannot start.")
        return False

    with sqlite3.connect(DATABASE_PATH) as conn:
        cursor = conn.cursor()

        # Kontrolli, kas tabelid eksisteerivad
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='words'")
        words_exists = cursor.fetchone()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='leaderboard'")
        leaderboard_exists = cursor.fetchone()

        if not words_exists or not leaderboard_exists:
            print("Required tables are missing. Application cannot start.")
            return False

        # Kontrolli, kas words tabelis on vähemalt üks kirje
        cursor.execute("SELECT COUNT(*) FROM words")
        word_count = cursor.fetchone()[0]

        if word_count == 0:
            print("Words table is empty. Application cannot start.")
            return False

    return True


# Algatame andmebaasi
db = Database()

# Kontrollime andmebaasi olekut
if not validate_database():
    exit("Exiting program due to missing database requirements.")
