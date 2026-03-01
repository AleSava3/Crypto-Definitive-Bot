from datetime import date

class State:
    def __init__(self):
        self.today = date.today()
        self.signals_today = 0
        self.high_today = 0

    def reset_if_new_day(self):
        if date.today() != self.today:
            self.today = date.today()
            self.signals_today = 0
            self.high_today = 0

state = State()
