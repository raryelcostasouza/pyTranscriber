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

class CtrEngine:
    @staticmethod
    def init():
        CtrEngine.cancel = False

    @staticmethod
    def is_operation_canceled():
        return CtrEngine.cancel

    @staticmethod
    def cancel_operation():
        CtrEngine.cancel = True

    @staticmethod
    def save_output_file(output_path, file_content):
        f = open(output_path, 'wb')
        f.write(file_content.encode("utf-8"))
        f.close()
