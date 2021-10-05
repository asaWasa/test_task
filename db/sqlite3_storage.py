import sqlite3
from settings import DB_SETTINGS
from db.db_emails_struct import DbEmailsStruct
from errors import DBError


class Sqlite3Storage:
    def __init__(self):
        self.db = DB_SETTINGS.NAME
        self.emails_struct = DbEmailsStruct()
        self.__init_db()

    def __init_db(self):
        self.__create_table_emails()

    def __create_table_emails(self):
        try:
            query = f'''CREATE TABLE IF NOT EXISTS 
            emails ( 
            {self.emails_struct.id} INTEGER PRIMARY KEY,
            {self.emails_struct.subject} TEXT,
            {self.emails_struct.email_from} TEXT,
            {self.emails_struct.date} TEXT,
            {self.emails_struct.body} TEXT
            );
            '''
            self.__make_query(query)
        except Exception as error:
            raise DBError(error)

    def __make_query(self, query, is_insert=False):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute(query)
            if is_insert:
                conn.commit()
                result = cursor.lastrowid
            else:
                result = cursor.fetchall()
            cursor.close()
            return result
        except sqlite3.Error as error:
            raise DBError(error)

    def get_list(self):
        query = f'SELECT * FROM {self.emails_struct.table};'
        result = self.__make_query(query)
        return result

    def get_item(self, _id):
        try:
            query = f'SELECT * FROM {self.emails_struct.table} WHERE id={_id};'
            result = self.__make_query(query)
            return result[0]
        except Exception as error:
            raise DBError(error)

    def save_item(self, data):
        try:
            query = f'''INSERT INTO 
            emails (
                {self.emails_struct.id},
                {self.emails_struct.subject},
                {self.emails_struct.email_from},
                {self.emails_struct.date},
                {self.emails_struct.body}
                )
            VALUES (
                 {data.id},
                "{data.subject}",
                "{data.email_from}",
                "{data.date}",
                "{data.body}"
                );
                '''
            # query = query.format(data)
            result = self.__make_query(query, is_insert=True)
            return result
        except Exception as error:
            raise DBError(error)
