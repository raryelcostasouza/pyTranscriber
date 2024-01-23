from pytranscriber.control.ctr_engine import CtrEngine
from pytranscriber.util.util import MyUtil
import whisper


class CtrWhisper(CtrEngine):

    @staticmethod
    def generate_subtitles(
            source_path,
            src_language,
            output=None
        ):

        model = whisper.load_model("base")
        result = model.transcribe(source_path, verbose=True)

        if CtrWhisper.cancel:
            return -1

        content_srt = CtrWhisper.generate_srt_file_content(result["segments"])
        content_txt = CtrWhisper.generate_txt_file_content(result["segments"])

        CtrWhisper.save_output_file(output, content_srt)
        CtrWhisper.save_output_file(output, content_txt)

        return output

    @staticmethod
    def generate_srt_file_content(transcribed_segments):
        content = ""
        for s in transcribed_segments:
            content = content + str(s["start"]) + " ----- " + str(s["end"]) + " : "+ str(s["text"]) + "\n"
        return content

    @staticmethod
    def generate_txt_file_content(transcribed_segments):
        content = ""
        for s in transcribed_segments:
            content = content + str(s["text"])
        return content