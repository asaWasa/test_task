class MailItem:
    def __init__(self, id, subject, email_from, date, body):
        self._id = id
        self._subject = subject
        self._email_from = email_from
        self._date = date
        self._body = body

    @property
    def id(self):
        return self._id
    @property
    def subject(self):
        return self._subject

    @property
    def email_from(self):
        return self._email_from

    @property
    def date(self):
        return self._date

    @property
    def body(self):
        return self._body
