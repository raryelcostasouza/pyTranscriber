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

from PyQt5.QtCore import QThread
from PyQt5.QtCore import pyqtSignal


class Thread_Cancel_Autosub(QThread):
    signalTerminated = pyqtSignal()

    def __init__(self, pObjWT):
        self.objWT = pObjWT
        QThread.__init__(self)

    def run(self):
        self.objWT.cancel()
        self.signalTerminated.emit()
