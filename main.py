#!/usr/bin/env python
from mailer import Mailer
from db.sqlite3_storage import Sqlite3Storage
from errors import DBError, MailerError, MailEmpty


class Manager:
    def __init__(self, _storage=None, _mailer=None):
        self.storage = _storage
        self.mailer = _mailer

    def run(self):
        try:
            ids = self.mailer.receive_ids()
            if ids:
                if not self.__find_id_in_base(ids[-1]):
                    data = self.__get_data(ids[-1])
                    self.storage.save_item(data)
                last_mail = self.storage.get_item(ids[-1])
                self.print_email(last_mail)
            else:
                print('Empty Mail')
                self.__print_all_mails()
        except DBError as error:
            print(f'Database Error - {error}')
        except MailerError as error:
            print(f'Mailer Error - {error}')
        except MailEmpty:
            print('Empty Mail')
        except Exception as error:
            print(f'Unknown error - {error}')

    def __print_all_mails(self):
        print('-' * 32)
        print('Emails from database:')
        last_mails = self.storage.get_list()
        if last_mails:
            for mail in last_mails:
                self.print_email(mail)

    def __find_id_in_base(self, _id):
        try:
            self.storage.get_item(_id)
            return True
        except:
            return False

    def __get_data(self, _id):
        raw_mail = self.mailer.receive_by_id(_id)
        data = self.mailer.parse_email(_id, raw_mail)
        return data

    def print_email(self, mail):
        print('-' * 32)
        print('[%s]: %s' % (mail[3], mail[2]))
        print(mail[1])
        print('-' * 32)
        print(mail[4])
        print('-' * 32)


if __name__ == '__main__':
    storage = Sqlite3Storage()
    mailer = Mailer()
    manager = Manager(storage, mailer)
    manager.run()
