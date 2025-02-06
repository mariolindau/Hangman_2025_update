import random
from tkinter import simpledialog, messagebox, Toplevel
from tkinter.constants import DISABLED, NORMAL

from models.Leaderboard import Leaderboard
from models.Stopwatch import Stopwatch
from models.Timer import Timer


class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.stopwatch = Stopwatch(self.view.lbl_time)

        # Ajasti loomine (TODO Sellega on mingi jama)
        self.timer = Timer(
            scheduled_callback=self.view.after,
            cancel_callback=self.view.after_cancel,
            interval=5000, # 5sek
            callback=self.change_title,
        )

        # Nuppude callback seaded
        self.btn_new_callback()
        self.btn_cancel_callback()
        self.btn_send_callback()
        self.btn_scoreboard_callback()
        self.view.set_timer_reset_callback(self.reset_timer) # Ajasti värk


        # Enter klahvi funktsionaalsus (Enter toob mängu aknal kohe nime akna ette)
        self.view.bind('<Return>', lambda event: self.btn_send_click())

    def buttons_for_game(self):
        """Nupud mängu hetkel, mis klikitavad jms"""
        self.view.btn_new['state'] = DISABLED # disabled tähendab, et ei saa pärast mängu alustamist uut mängu alustada
        self.view.btn_send['state'] = NORMAL
        self.view.btn_cancel['state'] = NORMAL
        self.view.char_input['state'] = NORMAL
        self.view.char_input.focus()
        self.view.cmb_category['state'] = DISABLED

    def buttons_for_not_game(self):
        """Kui vajutatakse katkestamise nuppu"""
        self.view.btn_new['state'] = NORMAL
        self.view.btn_send['state'] = DISABLED
        self.view.btn_cancel['state'] = DISABLED
        self.view.char_input.delete(0, 'end') # Tühjenda sisestuskast
        self.view.char_input['state'] = DISABLED
        self.view.cmb_category['state'] = NORMAL

    def btn_new_callback(self):
        self.view.set_btn_new_callback(self.btn_new_click) #Meetod ilma sulgudeta

    def btn_cancel_callback(self):
        self.view.set_btn_cancel_callback(self.btn_cancel_click)

    def btn_send_callback(self):
        self.view.set_btn_send_callback(self.btn_send_click)

    def btn_scoreboard_callback(self):
        self.view.set_btn_scoreboard_callback(self.btn_scoreboard_click) # Nupumajandus


    def btn_cancel_click(self):
        self.buttons_for_not_game()
        self.stopwatch.stop()
        self.timer.stop() # Peata title juhuslikkus (5 sek)
        self.view.lbl_result.config(text=self.model.user_word)
        self.view.title(self.model.titles[0])  # Esimene element title listist

    def btn_send_click(self):
        self.model.get_user_input(self.view.char_input.get().strip()) # saada sisestus
        self.view.lbl_result.config(text=self.model.user_word) # uuenda tulemust
        self.view.lbl_error.config(text=f'Vigased tähed: {self.model.get_all_user_chars()}')
        self.view.char_input.delete(0, 'end')   # Tühjendada sisestuskast
        if self.model.counter > 0:
            self.view.lbl_error.config(fg='red') # Muuda vigane tekst punaseks
            self.view.change_image(self.model.counter) # Muda pilti

        self.is_game_over()

    def btn_new_click(self):
        self.buttons_for_game()
        # Seadistab juhuslikku sõna kategooria järgi ja asendab tähed _
        self.model.start_new_game(self.view.cmb_category.current(), self.view.cmb_category.get()) # ID, sõna
        #Näita "sõna" kasutajale
        self.view.lbl_result.config(text=self.model.user_word)
        # Vigaste tähtede resettimine
        self.view.lbl_error.config(text='Vigased tähed', fg='black')
        #Muuda pilti
        self.view.change_image(self.model.counter) # Sulgudes võib kasutada väärtusena ka "0" lihtsalt
        self.timer.start() # Käivita title juhuslikkus (5 sek)
        self.stopwatch.reset() # Eelmine mäng
        self.stopwatch.start() # Käivitab aja

    def btn_scoreboard_click(self):
        lb = Leaderboard()
        data = lb.read_leaderboard()
        popup_window = self.view.create_popup_window()
        self.view.generate_scoreboard(popup_window, data)



    def is_game_over(self):
        if self.model.counter >= 11 or '_' not in self.model.user_word:
            self.stopwatch.stop() #Peata stopper
            self.timer.stop()
            self.buttons_for_not_game() # Nupu majandus
            player_name = simpledialog.askstring('mäng on läbi', 'Kuidas on mängija nimi?', parent=self.view)
            #messagebox.showinfo('Teade', 'Oled lisatud edetabelisse')
            self.model.save_player_score(player_name, self.stopwatch.seconds)
            self.view.title(self.model.titles[0]) # Esimene element title listist

    def change_title(self):
        new_title = random.choice(self.model.titles)
        self.view.title(new_title)

    def reset_timer(self):
        self.timer.start()