from pprint import pprint

class SimzDB:
    def __init__(self) -> None:
        self.conn = None
        self.inmemlog = []

    def append_log(self, log):
        self.inmemlog.append(log)

    def show_log_term(self):
        pprint(self.inmemlog)
