from PyQt5.QtWidgets import QMessageBox


class MessageUtil:

    @staticmethod
    def show_info_message(info_msg, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)

        msg.setWindowTitle(title)
        msg.setText(info_msg)
        msg.exec()

    @staticmethod
    def show_error_message(error_msg, title):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)

        msg.setWindowTitle(title)
        msg.setText(error_msg)
        msg.exec()
