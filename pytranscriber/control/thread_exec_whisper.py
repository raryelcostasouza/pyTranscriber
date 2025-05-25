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

from pytranscriber.control.ctr_whisper import CtrWhisper
from pytranscriber.control.thread_exec_generic import ThreadExecGeneric
from pytranscriber.util.util import MyUtil
import traceback


class Thread_Exec_Whisper(ThreadExecGeneric):

    def run(self):
        CtrWhisper.init()
        super()._loopSelectedFiles()
        self.running = False

    def _run_engine_for_media(self, index, langCode):
        sourceFile = self.obj_transcription_parameters.listFiles[index]
        outputFiles = self._generatePathOutputFile(sourceFile)
        outputFileSRT = outputFiles[0]
        outputFileTXT = outputFiles[1]

        fOutput = None
        try:
            fOutput = CtrWhisper.generate_subtitles(source_path=sourceFile,
                                                              outputSRT=outputFileSRT,
                                                              outputTXT=outputFileTXT,
                                                              src_language=langCode,
                                                              model=self.obj_transcription_parameters.get_model_whisper())
        except Exception as e:
            error_msg = f"""Error! Unable to generate subtitles: {traceback.format_exc()}"""
            self.signalErrorMsg.emit(error_msg)  # Emit the full traceback

        #if nothing was returned
        if not fOutput:
            self.signalErrorMsg.emit("Error! Unable to generate subtitles for file " + sourceFile + ".")
        elif fOutput != -1:
            #if the operation was not canceled

            #updated the progress message
            self.listenerProgress("Finished", 100)

            if self.obj_transcription_parameters.boolOpenOutputFilesAuto:
                #open both SRT and TXT output files
                MyUtil.open_file(outputFileTXT)
                MyUtil.open_file(outputFileSRT)