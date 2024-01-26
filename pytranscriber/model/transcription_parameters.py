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

class Transcription_Parameters():

    def __init__(self, listFiles, outputFolder, langCode,
                boolOpenOutputFilesAuto, proxies=None):
        self.listFiles = listFiles
        self.outputFolder = outputFolder
        self.langCode = langCode
        self.boolOpenOutputFilesAuto = boolOpenOutputFilesAuto
        self.proxies = proxies
        self.model_whisper = None

    def set_model_whisper(self, model):
        self.model_whisper = model

    def get_model_whisper(self):
        return self.model_whisper