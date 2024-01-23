import os
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
