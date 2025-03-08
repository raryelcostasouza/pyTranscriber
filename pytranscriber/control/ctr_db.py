'''
   (C) 2025 Raryel C. Souza
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.
    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

from pathlib import PurePath

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
                local_program_path = PurePath(__file__).parent.parent.parent.joinpath('pytranscriber.sqlite')
                str_local_program_path = str(local_program_path)



                self.conn = sqlite3.connect(str_local_program_path)
                cur = self.conn.cursor()

                return cur
            except Exception as ex:
                MessageUtil.show_error_message("ConnectDB" + str(ex), self.DB_ERROR)
                exit(1)

    def close(self):
        self.conn.close()
        self.conn = None

    def _load_one_row(self, table_name):
        cur = self.connect()
        if cur is None:
            exit(1)

        try:
            cur.execute('SELECT * FROM ' + table_name)
            return cur.fetchone()
        except sqlite3.Error as e:
            MessageUtil.show_error_message("LoadOneRow " + str(e), self.DB_ERROR)
            return None

    def _save_single_column(self, query, value):
        cur = self.connect()
        try:
            cur.execute(query,(value,))
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message("SaveSingleColumn " + str(e), self.DB_ERROR)
        self.close()

    def _truncate_table(self, table_name):
        cur = self.connect()
        try:
            cur.execute('DELETE FROM ' + table_name)
            self.conn.commit()
        except sqlite3.Error as e:
            MessageUtil.show_error_message("TruncateTable " + str(e), self.DB_ERROR)
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
            MessageUtil.show_error_message("SaveLastLanguage " + str(e), self.DB_ERROR)
        self.close()

    def load_proxy(self):
        return self._load_one_row('Proxy')

    def clear_proxy(self):
        self._truncate_table('Proxy')

    def save_proxy(self, proxy):
        cur = self.connect()
        try:
            cur.execute('INSERT INTO Proxy (proxy_address) VALUES (?)',
                        (proxy['https'],))
            self.conn.commit()
            MessageUtil.show_info_message('Proxy address saved successfully', 'Proxy settings saved')
        except sqlite3.Error as e:
            MessageUtil.show_error_message("SaveProxy " + str(e), self.DB_ERROR)
        self.close()
