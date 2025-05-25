from PyQt5.QtWidgets import QDialog
from pytranscriber.gui.proxy.window_proxy import Ui_Dialog
from pytranscriber.gui.message_util import MessageUtil


class ViewProxy:

    def __init__(self, ctr_proxy):
        self.ctr_proxy = ctr_proxy
        self.proxy_dialog = QDialog()
        loaded_proxy_dialog = Ui_Dialog()
        loaded_proxy_dialog.setupUi(self.proxy_dialog)

        self.radioButtonNone = loaded_proxy_dialog.radioButtonNone
        self.radioButtonHTTP = loaded_proxy_dialog.radioButtonHTTP
        self.radioButtonNone.clicked.connect(self.__listener_rbOnClicked)
        self.lineEditHttpProxy = loaded_proxy_dialog.lineEditHttpProxy
        self.lineEditHttpProxy.textChanged.connect(self.__listenerLineEditInput)
        self.pushButtonTest = loaded_proxy_dialog.pushButtonTest
        self.bSave = loaded_proxy_dialog.bSave

        self.pushButtonTest.clicked.connect(self.__listener_test)
        self.bSave.clicked.connect(self.__listener_save)
        self.__clear_proxy_settings()

    def show(self):
        self.ctr_proxy.load_data()
        self.proxy_dialog.exec_()

    def __clear_proxy_settings(self):
        self.radioButtonNone.setChecked(True)
        self.lineEditHttpProxy.setEnabled(False)
        self.pushButtonTest.setEnabled(False)

    def refresh_gui(self, proxy_address=None):
        if not proxy_address:
            self.__clear_proxy_settings()
        else:
            self.radioButtonHTTP.setChecked(True)
            self.lineEditHttpProxy.setEnabled(True)
            self.pushButtonTest.setEnabled(True)
            self.lineEditHttpProxy.setText(str(proxy_address))

    def __listener_test(self):
        proxy_input = self.lineEditHttpProxy.text()

        if proxy_input and self.radioButtonHTTP.isChecked():
            self.ctr_proxy.test_proxy_setting(proxy_input)

    def __listener_save(self):
        proxy_input = self.lineEditHttpProxy.text()

        if proxy_input and self.radioButtonHTTP.isChecked():
            self.ctr_proxy.set_proxy_setting(proxy_input, True)
        elif self.radioButtonNone.isChecked():
            self.ctr_proxy.set_proxy_setting('',True)

    def __listener_rbOnClicked(self):
        if self.radioButtonNone.isChecked():
            self.lineEditHttpProxy.setText('')

    def __listenerLineEditInput(self):
        if self.lineEditHttpProxy.text():
            self.pushButtonTest.setEnabled(True)
        else:
            self.pushButtonTest.setEnabled(False)

