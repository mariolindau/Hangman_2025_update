class Timer:

    def __init__(self, scheduled_callback, cancel_callback, interval, callback):
        """ Ajasti mis käivitab funktsiooni intervalli tagant
        :param scheduled_callback: funktsioon mis planeerib uue ajastuse
        :param cancel_callback: funktsioon mis tühistab ajastuse
        :param interval: intervall millisekundites
        :param callback: Funktsioon mis kustutatakse pärast intervalli
        """
        self.scheduled_callback = scheduled_callback
        self.cancel_callback = cancel_callback
        self.interval = interval
        self.callback = callback
        self.timer_id = None

    def start(self):
        """Käivitab ajasti"""
        self.stop()
        self.timer_id = self.scheduled_callback(self.interval, self.run)

    def stop(self):
        """Peatab ajasti"""
        if self.timer_id:
            self.cancel_callback(self.timer_id)
            self.timer_id = None

    def run(self):
        """Käivitab callbacki ja jätkab ajastamist"""
        self.callback()
        self.start()
