import os
import random


class FileObject:

    def __init__(self, folder, filename):
        path = os.path.join(folder, filename) # databases/words.txt
        self.__data = self._read_file(path) #Faili sisu {}

    @staticmethod
    def _read_file(path):
        if not os.path.exists(path):
            raise FileNotFoundError(f'Faili {path} ei leitud')

        data = {} # Dictionary või Dict

        with open(path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            if not lines:
                raise ValueError(f'Fail {path} on tühi.')

            #Esimene rida on päis
            header = lines[0].strip().split(';') # ['word', 'category']
            if len(header) != 2:
                raise ValueError('Faili formaat on vale.')

            # loe ülejäänud read
            for line in lines[1:]:
                word, category = line.strip().split(';')
                if category not in data:
                    data[category] = [] # Lisa kategooria tühi dict {}
                data[category].append(word) # Lisa sõna kategooriasse

        return  data # Tagasta faili sisu {'hoone': ['suvila', 'kasvuhoone'], 'amet': ['lasteaiakasvataja', 'bussijuht']}

    def get_unique_categories(self):
        # print(self.__data)
        categories = list(self.__data.keys()) #Võtmetest tehakse list
        categories.sort() # Sorteeri list
        #Lisa "Vali kategooria" listi esimeseks elemendiks
        categories.insert(0, 'Vali kategooria')

        return [category.capitalize() for category in categories] # Tagasta kategooriate nimede list

    def get_random_word(self, category):
        if category is None: # Kategooriat ei ole (Kõik sõnad on lubatud)
            all_words = [word for words in self.__data.values() for word in words]
            return random.choice(all_words) if all_words else None

        category = category.lower() # Argument tehakse väikse tähega!!
        if category in self.__data:
            return random.choice(self.__data[category]) if self.__data[category] else None

        # Kui kategooriat ei leitud
        return None