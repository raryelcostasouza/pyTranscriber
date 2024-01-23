from pytranscriber.gui.message_util import MessageUtil
import sqlite3


class CtrDB:
    conn = None
    DB_ERROR = "DB Error"

    def connect(self):
        if self.conn:
            return self.conn.cursor()
        else:
            try:
                self.conn = sqlite3.connect('pytranscriber.sqlite')
                cur = self.conn.cursor()
                return cur
            except Exception as ex:
                MessageUtil.show_error_message(str(ex), self.DB_ERROR)
                return None

    def close(self):
        self.conn.close()
        self.conn = None

    def _load_one_row(self, table_name):
        cur = self.connect()
        try:
            cur.execute('SELECT * FROM ' + table_name)
            return cur.fetchone()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e), self.DB_ERROR)
            return None

    def _save_single_column(self, query, value):
        cur = self.connect()
        try:
            cur.execute(query,(value,))
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e), self.DB_ERROR)
        self.close()

    def _truncate_table(self, table_name):
        cur = self.connect()
        try:
            cur.execute('DELETE FROM ' + table_name)
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e), self.DB_ERROR)
        self.close()

    def load_last_language(self):
        return self._load_one_row('Language')

    def clear_last_language(self):
        self._truncate_table('Language')

    def save_last_language(self, language):
        cur = self.connect()
        try:
            cur.execute('INSERT INTO Language (last_language) VALUES (?)',
                        (language,))
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e), self.DB_ERROR)
        self.close()