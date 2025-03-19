import glob
import os
import random
from datetime import datetime

from models.Database import Database  # Uus andmebaasi klass
from models.Leaderboard import Leaderboard

class Model:
    def __init__(self):
        self.__image_files = []  # tühi list piltide jaoks
        self.load_images('images')

        self.__database = Database()  # Kasutame Database klassi
        self.__categories = self.__database.get_all_categories()  # Unikaalsed kategooriad
        self.__scoreboard = Leaderboard()

        self.titles = ['Poomismäng 2025', 'Kas jäid magama', 'Ma ootan su käiku', 'Sisesta juba see täht', 'Zzzzzz....']

        # Mängu muutujad
        self.__new_word = None  # Juhuslik sõna mängu jaoks. Sõna mida ära arvata
        self.__user_word = []  # Kõik kasutaja leitud tähed (visuaal)
        self.__counter = 0  # Vigade loendur
        self.__all_user_chars = []  # Kõik valesti sisestatud tähed

    def load_images(self, folder):
        if not os.path.exists(folder):
            raise FileNotFoundError(f'Kausta {folder} ei ole.')

        images = glob.glob(os.path.join(folder, '*.png'))
        if not images:
            raise FileNotFoundError(f'Kaustas {folder} ei ole PNG laiendiga faile.')

        self.__image_files = images

    def start_new_game(self, category_id, category):
        if category_id == 0:
            category = None

        word_data = self.__database.get_random_word()  # Võtame SQL-ist juhusliku sõna

        if word_data:
            self.__new_word, word_category = word_data
        else:
            raise ValueError("Sõnu ei leitud! Kontrolli andmebaasi.")

        self.__user_word = ['_' for _ in self.__new_word]  # Algseis
        self.__counter = 0  # Algseis
        self.__all_user_chars = []  # Algseis

    def get_user_input(self, user_input):
        """Kasutaja sisendi töötlemine"""
        if user_input:
            user_char = user_input[:1]  # Esimene märk sisestuses
            if user_char.lower() in self.__new_word.lower():
                self.change_user_input(user_char)  # Leiti täht
            else:  # Ei leitud tähte
                self.__counter += 1
                self.__all_user_chars.append(user_char.upper())

    def change_user_input(self, user_char):
        """Asendab kõik _ leitud tähega"""
        current_word = self.char_to_list(self.__new_word)
        for i, c in enumerate(current_word):
            if c.lower() == user_char.lower():
                self.__user_word[i] = user_char.upper()

    @staticmethod
    def char_to_list(word):
        """Muutab stringi listiks ('test' -> ['t', 'e', 's', 't'])"""
        return list(word)

    def get_all_user_chars(self):
        """Tagastab kõik kasutaja sisestatud tähed (komaga eraldatult)"""
        return ', '.join(self.__all_user_chars)

    def save_player_score(self, name, seconds):
        """Salvestab mängija tulemuse andmebaasi"""
        today = datetime.now().strftime('%Y-%m-%d %T')

        if not name.strip():  # Kui nimi puudub
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])

        # Lisame kirje SQL andmebaasi
        self.__database.add_leaderboard_entry(name, self.__new_word, self.get_all_user_chars(), seconds, today)

    # GETTERS

    @property
    def image_files(self):
        """TAGASTAB PILTIDE LISTI"""
        return self.__image_files

    @property
    def categories(self):
        """Tagastab kategooriate listi"""
        return self.__categories

    @property
    def user_word(self):
        """Tagastab kasutaja leitud tähed"""
        return self.__user_word

    @property
    def counter(self):
        """Tagastab vigade arvu"""
        return self.__counter
