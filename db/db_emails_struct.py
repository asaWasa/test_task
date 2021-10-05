from settings import DB_SETTINGS


class DbEmailsStruct:
    def __init__(self):
        self.id = 'id'
        self.subject = 'subject'
        self.email_from = 'email_from'
        self.date = 'date'
        self.body = 'body'
        self.table = DB_SETTINGS.TABLE
