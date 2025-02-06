import glob
import os
import random
from datetime import datetime

from models.FileObject import FileObject
from models.Leaderboard import Leaderboard


class Model:

    def __init__(self):
        self.__image_files = [] # tühi list piltide jaoks
        self.load_images('images')
        self.__file_object = FileObject('databases', 'words.txt')
        self.__categories = self.__file_object.get_unique_categories() # Unikaalsed kategooriad
        self.__scoreboard = Leaderboard()
        # print(self.__file_object.get_random_word ('Hoone')) # Kontrolli, et ei tagastaks suvalisi sõnu
        self.titles = ['Poomismäng 2025', 'Kas jäid magama', 'Ma ootan su käiku', 'Sisesta juba see täht', 'Zzzzzz....']


        #mängu muutujad
        self.__new_word = None # Juhuslik sõna mängu jaoks. Sõna mida ära arvata
        self.__user_word = [] # Kõik kasutaja leitud tähed (visuaal)
        self.__counter = 0 # Vigade loendur
        self.__all_user_chars = [] # Kõik valesti sisestatud tähed

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

        self.__new_word = self.__file_object.get_random_word(category) # Juhuslik sõna
        self.__user_word = [] # Algseis
        self.__counter = 0  # Algseis
        self.__all_user_chars = [] # Algseis

        # Asenda sõnas kõik tähed allkriibsuga M A J A => _ _ _ _
        for x in range(len(self.__new_word)):
            self.__user_word.append('_')
        #print(self.__new_word, self.__user_word) # Saad kontrollida kas kas kõik on õige ja töötab

    def get_user_input(self, user_input):
        # User_input on sisestuskasti kirjutatud värk
        if user_input:
            user_char = user_input[:1] # Esimene märk sisestuses
            if user_char.lower() in self.__new_word.lower():
                self.change_user_input(user_char) # Leiti täht täpselt nii nagu kasutaja kirjutas
            else: # Ei leitud tähte
                self.__counter += 1
                self.__all_user_chars.append(user_char.upper())


    def change_user_input(self, user_char):
        # Asenda kõik _ leitud tähega
        current_word = self.char_to_list(self.__new_word)
        x = 0
        for c in current_word:
            if c.lower() == user_char.lower():
                self.__user_word[x] = user_char.upper()
            x += 1

    @staticmethod
    def char_to_list(word):
        # string to list test => ['t', 'e', 's', 't']
        chars = []
        chars[:0] = word
        return chars

    def get_all_user_chars(self):
        return ', '.join(self.__all_user_chars) # List tehakse komaga eraldatud stringiks

    def save_player_score(self, name, seconds):
        today = datetime.now().strftime('%Y-%m-%d %T') # Hetke kuupäev ja kell 2025-02-06 14:12:29

        if not name.strip(): #Nime ei ole
            name = random.choice(['Teadmata', 'Tundmatu', 'Unknown'])

        with open(self.__scoreboard.file_path, 'a', encoding='utf-8') as f:
            line = ';'.join([name.strip(), self.__new_word, self.get_all_user_chars(), str(seconds), today])
            f.write(line + '\n')

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
        """tagastab kasutaja leitud tähed"""
        return self.__user_word

    @property
    def counter(self):
        """Tagastab vigade arvu"""
        return self.__counter