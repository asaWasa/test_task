class DBError(Exception):
    def __init__(self, text=None):
        self.text = text


class MailerError(Exception):
    def __init__(self, text=None):
        self.text = text


class MailEmpty(Exception):
    def __init__(self, text=None):
        self.text = text