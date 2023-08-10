'''
   (C) 2019 Raryel C. Souza
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

from pytranscriber.control.ctr_license import Ctr_License
from pytranscriber.control.ctr_proxy import Ctr_Proxy
from pytranscriber.control.ctr_db import CtrDB
from pytranscriber.gui.main.view_main import ViewMain


class Ctr_Main():

    def __init__(self):
        self.ctrDB = CtrDB()
        self.ctrLicense = Ctr_License(self)
        self.ctrProxy = Ctr_Proxy(self)

        self.last_language = None

        self.viewMain = ViewMain(self)

        self.ctrLicense.load_license_data()
        self._load_last_language()
        self.viewMain.show()

    def save_last_language(self, language):
        self.ctrDB.clear_last_language()
        self.ctrDB.save_last_language(language)

    def _load_last_language(self):
        data = self.ctrDB.load_last_language()
        if data is not None:

            self.last_language = data[1]
            self.viewMain.set_gui_language(self.last_language)


