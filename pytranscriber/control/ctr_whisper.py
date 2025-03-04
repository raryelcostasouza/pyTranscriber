from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QMessageBox
import os
import sys
import whisper
import datetime
import shutil
from pytranscriber.control.ctr_engine import CtrEngine


class CtrWhisper(CtrEngine, QObject):
    errorSignal = pyqtSignal(str)  # Define the signal

    def __init__(self):
        super().__init__()
        self.errorSignal.connect(self.show_error_message)  # Connect signal to slot

    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS  # Running in PyInstaller bundle
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))  # Running normally

    MODEL_DIR = os.path.join(base_path, "pytranscriber", "whisper_models")
    os.makedirs(MODEL_DIR, exist_ok=True)

    @staticmethod
    def generate_subtitles(source_path, src_language, outputSRT=None, outputTXT=None, model='base'):
        if getattr(sys, 'frozen', False):  # Running as a bundled executable
            ffmpeg_path = os.path.join(sys._MEIPASS, "ffmpeg")
        else:
            ffmpeg_path = shutil.which("ffmpeg")  # Use system-wide FFmpeg

        os.environ["FFMPEG_PATH"] = ffmpeg_path
        os.environ["PATH"] += os.pathsep + os.path.dirname(ffmpeg_path)

        # Monkey-patch shutil.which to always return our FFmpeg path
        original_which = shutil.which  # Backup original function

        def patched_which(cmd, *args, **kwargs):
            if cmd == "ffmpeg":
                return ffmpeg_path
            return original_which(cmd, *args, **kwargs)

        shutil.which = patched_which  # Apply patch

        model = whisper.load_model(model, download_root=CtrWhisper.MODEL_DIR)
        result = model.transcribe(source_path, verbose=True, language=src_language)

        if CtrWhisper.cancel:
            return -1

        content_srt = CtrWhisper.generate_srt_file_content(result["segments"])
        content_txt = CtrWhisper.generate_txt_file_content(result["segments"])

        CtrWhisper.save_output_file(outputSRT, content_srt)
        CtrWhisper.save_output_file(outputTXT, content_txt)

        return outputSRT

    @staticmethod
    def show_error_message(message):
        """Displays the error message in a PyQt5 QMessageBox."""
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(message)
        msg_box.exec_()

    @staticmethod
    def generate_srt_file_content(transcribed_segments):
        content = ""

        def format_timestamp(seconds):
            """Convert seconds to SRT-compliant timestamp (HH:MM:SS,MS)."""
            td = datetime.timedelta(seconds=seconds)
            millis = int((seconds - int(seconds)) * 1000)
            return f"{str(td)},{millis:03d}"

        for i, s in enumerate(transcribed_segments, start=1):
            start_time = format_timestamp(s["start"])
            end_time = format_timestamp(s["end"])

            content += f"{i}\n{start_time} --> {end_time}\n{s['text']}\n\n"

        return content

    @staticmethod
    def generate_txt_file_content(transcribed_segments):
        content = ""
        for s in transcribed_segments:
            content = content + str(s["text"])
        return content