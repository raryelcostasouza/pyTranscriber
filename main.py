# (C) 2019 Raryel C. Souza
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from pytranscriber.control.ctr_main import Ctr_Main
from pytranscriber.gui.message_util import MessageUtil
import multiprocessing
import sys

if __name__ == '__main__':
    multiprocessing.freeze_support()

    try:
        ctrMain = Ctr_Main()
        sys.exit(0)
    except Exception as ex:
        MessageUtil.show_error_message(str(ex), "Main Error")
        sys.exit(1)


