from pytranscriber.gui.message_util import MessageUtil
import sqlite3


class CtrDB:
    conn = None

    def connect(self):
        if self.conn:
            return self.conn.cursor()
        else:
            try:
                self.conn = sqlite3.connect('pytranscriber.sqlite')
                cur = self.conn.cursor()
                return cur
            except Exception as ex:
                MessageUtil.show_error_message(str(ex))
                return None

    def close(self):
        self.conn.close()
        self.conn = None

    def save_license_data(self, license_data):
        cur = self.connect()
        try:
            cur.execute('INSERT INTO License (expiry,plan,key) VALUES (?, ?, ?)',
                        (license_data.expiry, license_data.plan, license_data.key))
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e))
        self.close()

    def clear_license_data(self):
        cur = self.connect()
        try:
            cur.execute('DELETE FROM License')
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e))
        self.close()

    def load_license_data(self):
        cur = self.connect()
        try:
            cur.execute('SELECT * FROM License')
            return cur.fetchone()
        except sqlite3.Error as e:
            MessageUtil.show_error_message(str(e))
            return None
