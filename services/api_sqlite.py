import sqlite3
import os


def dict_factory(cursor, row):
    save_dict = dict()
    for index, column in enumerate(cursor.description):
        save_dict[column[0]] = row[index]
    return save_dict


class Users:
    def __init__(self):
        self.database = sqlite3.connect(os.path.join('data', 'database (2) (2).db'))
        self.database.row_factory = dict_factory
        self.cursor = self.database.cursor()
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS users(
        #                         id INTEGER PRIMARY KEY AUTOINCREMENT,
        #                         chat_id INTEGER,
        #                         user_name TEXT,
        #                         balance REAL DEFAULT 0,
        #                         investments REAL DEFAULT 0,
        #                         is_banned INTEGER DEFAULT 0,
        #                         is_ref INTEGER DEFAULT 0,
        #                         data_create DATE DEFAULT (DATE('now'))
        #
        # )''')
        # self.database.commit()

    def add_user(self, username, chat_id, is_ref=0):
        self.cursor.execute('INSERT INTO users (username, chat_id, is_ref) VALUES(?,?,?)',
                                                             (username, chat_id, is_ref))
        self.database.commit()

    def get_user(self, chat_id):
        self.cursor.execute('SELECT * FROM users WHERE chat_id = ?', (chat_id,))
        return self.cursor.fetchone()

    def get_count_ref(self, chat_id):
        return int(self.cursor.execute('SELECT COUNT(*) FROM users WHERE is_ref = ?', (chat_id,)).fetchone()
                                                                                                 ['COUNT(*)'])

    def change_balance(self, chat_id, balance):
        self.cursor.execute('UPDATE users SET balance = ?  WHERE chat_id = ?', (balance, chat_id))
        self.database.commit()

    def change_investments(self, chat_id, investments):
        self.cursor.execute('UPDATE users SET investments = ? WHERE chat_id = ?', (investments, chat_id))
        self.database.commit()

    def change_is_banned(self, chat_id, is_banned):
        self.cursor.execute('UPDATE users SET is_banned = ? WHERE chat_id = ?', (is_banned, chat_id))
        self.database.commit()

    def __iter__(self):
        return iter(self.database.execute('SELECT * FROM users').fetchall())


class Config:
    def __init__(self):
        self.database = sqlite3.connect(os.path.join('data', 'database (2) (2).db'))
        self.cursor = self.database.cursor()
        # self.cursor.execute('''CREATE TABLE IF NOT EXISTS config (
        #                                     percent_investments REAL,
        #                                     count_users INTEGER
        #                                     )''')

    def change_percent(self, percent):
        self.cursor.execute("UPDATE config SET percent_investments = ?", (percent,))
        self.database.commit()

    def change_count_users(self, count):
        self.cursor.execute("UPDATE config SET count_users = ?", (count,))
        self.database.commit()

    def get_percent(self):
        return float(self.cursor.execute("SELECT percent_investments FROM config").fetchone()[0])

    def get_count_users(self):
        return int(self.cursor.execute("SELECT count_users FROM config").fetchone()[0])
