import imaplib
import email
from email.header import decode_header, make_header
from settings import EMAIL_SETTINGS
from datetime import datetime
from db.mail_item_struct import MailItem


class Mailer:
    def parse_email(self, id, raw_mail):
        msg = email.message_from_bytes(raw_mail)
        date = email.utils.parsedate(msg['Date'])
        date = datetime(*date[:7])
        date = date.strftime('%Y-%m-%d %H:%M:%S')
        body = ''
        if msg.is_multipart():
            payload = msg.get_payload()[0]
            if payload.get_content_maintype() == 'text':
                body += payload.get_payload(decode=True).decode('utf-8')
        else:
            body = msg.get_payload(decode=True).decode('utf-8')
        body = body.split('\n--')
        body = body[0].lstrip('\n')
        result = MailItem(id,
                          str(make_header(decode_header(msg['Subject']))),
                          email.utils.parseaddr(msg['From'])[1],
                          date,
                          str(body)
                          )

        return result

    def receive_by_id(self, id):
        mail = self.__connect()
        _, data = mail.search(None, "ALL")
        _, raw_mail = mail.fetch(str(id), '(RFC822)')
        msg = raw_mail[0][1]
        self.__disconnect(mail)
        return msg

    def __connect(self):
        mail = imaplib.IMAP4_SSL(EMAIL_SETTINGS.IMAP)
        mail.login(EMAIL_SETTINGS.EMAIL, EMAIL_SETTINGS.PASSWORD)
        mail.select('INBOX')
        return mail

    def __disconnect(self, mail):
        mail.logout()

    def receive_ids(self, *args):
        mail = self.__connect()
        status, data = mail.search(None, 'ALL')
        ids = data[0]
        ids = ids.split()
        ids = list(map(int, ids))
        self.__disconnect(mail)
        return ids
