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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QDialog, QActionGroup
from PyQt5.QtCore import Qt
from pathlib import Path
from pytranscriber.model.transcription_parameters import Transcription_Parameters
from pytranscriber.util.util import MyUtil
from pytranscriber.control.thread_exec_autosub import Thread_Exec_Autosub
from pytranscriber.control.thread_exec_whisper import Thread_Exec_Whisper
from pytranscriber.control.thread_cancel_autosub import Thread_Cancel_Autosub
from pytranscriber.gui.main.window_main import Ui_window
from pytranscriber.gui.message_util import MessageUtil
from pytranscriber.model.google_speech import Google_Speech
from pytranscriber.model.whisper import Whisper
from pathlib import Path
from platformdirs import user_desktop_dir

import os
import sys
from pathlib import PurePath


class ViewMain:

    def __init__(self, ctr_main):
        self.ctr_main = ctr_main

        self.app = QtWidgets.QApplication(sys.argv)
        window = QtWidgets.QMainWindow()
        self.window = window
        self.objGUI = Ui_window()
        self.objGUI.setupUi(window)
        self.__initGUI(window)

        window.setFixedSize(window.size())

    def show(self):
        self.window.show()
        self.app.exec_()

    def __initGUI(self, window):

        self.__create_list_whisper_model_options()
        self.__listenerSwitchEngine()
        self.__listenerProgress("", 0)

        # Get the user's Desktop directory
        desktop_path = Path(user_desktop_dir())

        # Define the output folder path
        pathOutputFolder = desktop_path / 'pyTranscriber'

        # Ensure the output folder exists
        pathOutputFolder.mkdir(parents=True, exist_ok=True)

        self.objGUI.qleOutputFolder.setText(str(pathOutputFolder))

        self.objGUI.bRemoveFile.setEnabled(False)

        self.objGUI.bCancel.hide()

        # button listeners
        self.objGUI.bConvert.clicked.connect(self.__listenerBExec)
        self.objGUI.bCancel.clicked.connect(self.__listenerBCancel)
        self.objGUI.bRemoveFile.clicked.connect(self.__listenerBRemove)
        self.objGUI.bSelectOutputFolder.clicked.connect(self.__listenerBSelectOuputFolder)
        self.objGUI.bOpenOutputFolder.clicked.connect(self.__listenerBOpenOutputFolder)
        self.objGUI.bSelectMedia.clicked.connect(self.__listenerBSelectMedia)
        self.objGUI.rbGoogleEngine.clicked.connect(self.__listenerSwitchEngine)
        self.objGUI.rbWhisper.clicked.connect(self.__listenerSwitchEngine)

        self.objGUI.actionProxy.triggered.connect(self.__listenerBProxySettings)
        self.objGUI.actionLicense.triggered.connect(self.__listenerBLicense)
        self.objGUI.actionDonation.triggered.connect(self.__listenerBDonation)
        self.objGUI.actionAbout_pyTranscriber.triggered.connect(self.__listenerBAboutpyTranscriber)

        self.__initLanguageMenu(window)
        self.objGUI.action_group.triggered.connect(self.__listenerChangeLanguage)

    def __initLanguageMenu(self, window):
        self.objGUI.actionEnglish.setCheckable(True)
        self.objGUI.actionEnglish.setChecked(True)
        self.objGUI.actionChineseTraditional.setCheckable(True)
        self.objGUI.actionChineseSimplified.setCheckable(True)
        self.objGUI.actionPortuguese.setCheckable(True)

        # set up of the actiongroup
        self.objGUI.action_group = QActionGroup(window)
        self.objGUI.action_group.addAction(self.objGUI.actionEnglish)
        self.objGUI.action_group.addAction(self.objGUI.actionChineseTraditional)
        self.objGUI.action_group.addAction(self.objGUI.actionChineseSimplified)
        self.objGUI.action_group.addAction(self.objGUI.actionPortuguese)

        self.objGUI.trans = QtCore.QTranslator(window)
        self.objGUI.mainWindow = window

        # listener change language selected

    def __listenerChangeLanguage(self, event):
        # get the label of the selected language
        currentLang = event.text()
        self.set_gui_language(currentLang)
        self.ctr_main.save_last_language(currentLang)

    def set_gui_language(self, currentLang):
        if currentLang:
            self.set_language_selector(currentLang)
            currentDir = PurePath(__file__).parent.parent.parent.parent
            pathLangFile = currentDir.joinpath('pytranscriber').joinpath('gui').joinpath(currentLang)
            self.objGUI.trans.load(str(pathLangFile))

            QtWidgets.QApplication.instance().installTranslator(self.objGUI.trans)
        else:
            QtWidgets.QApplication.instance().removeTranslator(self.objGUI.trans)

        # refresh UI with translation
        self.objGUI.retranslateUi(self.objGUI.mainWindow)

    def set_language_selector(self, currentLang):
        if currentLang == "繁體中文 - Chinese Traditional":
            self.objGUI.actionChineseTraditional.setChecked(True)
        elif currentLang == "简体中文 - Chinese Simplified":
            self.objGUI.actionChineseSimplified.setChecked(True)
        elif currentLang == "Português":
            self.objGUI.actionPortuguese.setChecked(True)
        else:
            self.objGUI.actionEnglish.setChecked(True)

    def __resetGUIAfterSuccess(self):
        self.__resetGUIAfterCancel()

        self.objGUI.qlwListFilesSelected.clear()
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)

    def __resetGUIAfterCancel(self):

        self.__resetProgressBar()

        self.objGUI.bSelectMedia.setEnabled(True)
        self.objGUI.bSelectOutputFolder.setEnabled(True)
        self.objGUI.cbSelectLang.setEnabled(True)
        self.objGUI.chbxOpenOutputFilesAuto.setEnabled(True)

        self.objGUI.bCancel.hide()
        self.objGUI.bConvert.setEnabled(True)
        self.objGUI.bRemoveFile.setEnabled(True)

    def __lockButtonsDuringOperation(self):
        self.objGUI.bConvert.setEnabled(False)
        self.objGUI.bRemoveFile.setEnabled(False)
        self.objGUI.bSelectMedia.setEnabled(False)
        self.objGUI.bSelectOutputFolder.setEnabled(False)
        self.objGUI.cbSelectLang.setEnabled(False)
        self.objGUI.chbxOpenOutputFilesAuto.setEnabled(False)
        QtCore.QCoreApplication.processEvents()

    def __listenerProgress(self, str, percent):
        self.objGUI.labelCurrentOperation.setText(str)
        self.objGUI.progressBar.setProperty("value", percent)
        QtCore.QCoreApplication.processEvents()

    def __setProgressBarIndefinite(self):
        self.objGUI.progressBar.setMinimum(0)
        self.objGUI.progressBar.setMaximum(0)
        self.objGUI.progressBar.setValue(0)

    def __resetProgressBar(self):
        self.objGUI.progressBar.setMinimum(0)
        self.objGUI.progressBar.setMaximum(100)
        self.objGUI.progressBar.setValue(0)
        self.__listenerProgress("", 0)

    def __updateProgressFileYofN(self, str):
        self.objGUI.labelProgressFileIndex.setText(str)
        QtCore.QCoreApplication.processEvents()

    def __listenerBSelectOuputFolder(self):
        fSelectDir = QFileDialog.getExistingDirectory(self.objGUI.centralwidget)
        if fSelectDir:
            self.objGUI.qleOutputFolder.setText(fSelectDir)

    def __create_list_whisper_model_options(self):
        self.whisper_model_options = list()
        self.whisper_model_options.append(self.objGUI.rbModelBase)
        self.whisper_model_options.append(self.objGUI.rbModelTiny)
        self.whisper_model_options.append(self.objGUI.rbModelMedium)
        self.whisper_model_options.append(self.objGUI.rbModelLarge)
        self.whisper_model_options.append(self.objGUI.rbModelSmall)


    def hide_whisper_models(self):
        self.objGUI.lModels.hide()
        for rb in self.whisper_model_options:
            rb.hide()
    def show_whisper_models(self):
        self.objGUI.lModels.show()
        for rb in self.whisper_model_options:
            rb.show()

    def get_whisper_model_selected(self):
       if self.objGUI.rbWhisper.isChecked():
            for rb in self.whisper_model_options:
                if rb.isChecked():
                    return rb.text().lower()


    def __listenerSwitchEngine(self):
        self.objGUI.cbSelectLang.clear()
        if self.objGUI.rbWhisper.isChecked():
            self.objGUI.cbSelectLang.addItems(Whisper.get_supported_languages())
            self.show_whisper_models()
        else:
            self.objGUI.cbSelectLang.addItems(Google_Speech.get_supported_languages())
            self.hide_whisper_models()


    def __listenerBSelectMedia(self):
        # options = QFileDialog.Options()
        options = QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self.objGUI.centralwidget, "Select media", "",
                                                "All Media Files (*.mp3 *.mp4 *.wav *.m4a *.wma *.ogg *.ogv *.mkv *.webm *.ts)")

        if files:
            self.objGUI.qlwListFilesSelected.addItems(files)

            # enable the convert button only if list of files is not empty
            self.objGUI.bConvert.setEnabled(True)
            self.objGUI.bRemoveFile.setEnabled(True)

    def __listenerBExec(self):
        # extracts the two letter lang_code from the string on language selection
        selectedLanguage = self.objGUI.cbSelectLang.currentText()
        indexSpace = selectedLanguage.index(" ")
        langCode = selectedLanguage[:indexSpace]

        listFiles = []
        for i in range(self.objGUI.qlwListFilesSelected.count()):
            listFiles.append(str(self.objGUI.qlwListFilesSelected.item(i).text()))

        outputFolder = self.objGUI.qleOutputFolder.text()

        if self.objGUI.chbxOpenOutputFilesAuto.checkState() == Qt.Checked:
            boolOpenOutputFilesAuto = True
        else:
            boolOpenOutputFilesAuto = False

        obj_transcription_parameters = Transcription_Parameters(listFiles, outputFolder, langCode,
                                                                boolOpenOutputFilesAuto, self.ctr_main.ctrProxy.get_proxy_setting())

        if self.objGUI.rbGoogleEngine.isChecked():
            self.__transcribe_google_engine(obj_transcription_parameters)
        else:
            model_whisper = self.get_whisper_model_selected()
            obj_transcription_parameters.set_model_whisper(model_whisper)
            self.__transcribe_whisper(obj_transcription_parameters)

    def __transcribe_google_engine(self, obj_transcription_parameters):
        if not MyUtil.is_internet_connected(self.ctr_main.ctrProxy.get_proxy_setting()):
            MessageUtil.show_error_message(
                "\n\n1) Please make sure you are connected to the internet. \n" +
                "2) If you are in China or other place that blocks access to Google servers: " +
                "please install and enable a desktop-wide VPN app like Windscribe before trying to use pyTranscriber!",
                "Error! Cannot reach Google Speech Servers. " )
            return

        self.__set_progress_bar_classic_mode()

        # execute the main process in separate thread to avoid gui lock
        self.thread_exec = Thread_Exec_Autosub(obj_transcription_parameters)

        # connect signals from work thread to gui controls
        self.thread_exec.signalLockGUI.connect(self.__lockButtonsDuringOperation)
        self.thread_exec.signalResetGUIAfterSuccess.connect(self.__resetGUIAfterSuccess)
        self.thread_exec.signalResetGUIAfterCancel.connect(self.__resetGUIAfterCancel)
        self.thread_exec.signalProgress.connect(self.__listenerProgress)
        self.thread_exec.signalProgressFileYofN.connect(self.__updateProgressFileYofN)
        self.thread_exec.signalErrorMsg.connect(MessageUtil.show_error_message)
        self.thread_exec.start()

        self.__show_cancel_button()


    def __transcribe_whisper(self, obj_transcription_parameters):
        self.__set_progress_bar_pulse_mode()

        # execute the main process in separate thread to avoid gui lock
        self.thread_exec = Thread_Exec_Whisper(obj_transcription_parameters)
        self.thread_exec.signalResetGUIAfterSuccess.connect(self.__resetGUIAfterSuccess)
        self.thread_exec.signalResetGUIAfterCancel.connect(self.__resetGUIAfterCancel)
        self.thread_exec.signalProgressFileYofN.connect(self.__updateProgressFileYofN)
        self.thread_exec.signalErrorMsg.connect(MessageUtil.show_error_message)

        self.thread_exec.start()

        self.__show_cancel_button()

    def __set_progress_bar_pulse_mode(self):
        self.objGUI.progressBar.setRange(0, 0)

    def __set_progress_bar_classic_mode(self):
        self.objGUI.progressBar.setRange(0, 100)

    def __show_cancel_button(self):
        self.objGUI.bCancel.show()
        self.objGUI.bCancel.setEnabled(True)

    def __listenerBCancel(self):
        self.objGUI.bCancel.setEnabled(False)
        self.thread_cancel = Thread_Cancel_Autosub(self.thread_exec)

        # Only if worker thread is running
        if self.thread_exec and self.thread_exec.isRunning():
            # reset progress indicator
            self.__listenerProgress("Cancelling", 0)
            self.__setProgressBarIndefinite()
            self.__updateProgressFileYofN("")

            # connect the terminate signal to resetGUI
            self.thread_cancel.signalTerminated.connect(self.__resetGUIAfterCancel)
            # run the cancel autosub operation in new thread
            # to avoid progressbar freezing
            self.thread_cancel.start()
            self.thread_exec = None

    def __listenerBRemove(self):
        indexSelected = self.objGUI.qlwListFilesSelected.currentRow()
        if indexSelected >= 0:
            self.objGUI.qlwListFilesSelected.takeItem(indexSelected)

        # if no items left disables the remove and convert button
        if self.objGUI.qlwListFilesSelected.count() == 0:
            self.objGUI.bRemoveFile.setEnabled(False)
            self.objGUI.bConvert.setEnabled(False)

    def __listenerBOpenOutputFolder(self):
        pathOutputFolder = Path(self.objGUI.qleOutputFolder.text())

        # if folder exists and is valid directory
        if os.path.exists(pathOutputFolder) and os.path.isdir(pathOutputFolder):
            MyUtil.open_file(pathOutputFolder)
        else:
            MessageUtil.show_error_message("Error! Invalid output folder.")

    def __listenerBProxySettings(self):
        self.ctr_main.ctrProxy.show()

    def __listenerBLicense(self):
        MessageUtil.show_info_message(
            "<html><body><a href=\"https://www.gnu.org/licenses/gpl-3.0.html\">GPL License</a><br><br>"
            + "Copyright (C) 2019 Raryel C. Souza <raryel.costa at gmail.com><br>"
            + "<br>This program is free software: you can redistribute it and/or modify<br>"
            + "it under the terms of the GNU General Public License as published by<br>"
            + "the Free Software Foundation, either version 3 of the License, or<br>"
            + " any later version<br>"
            + "<br>"
            + "This program is distributed in the hope that it will be useful,<br>"
            + "but WITHOUT ANY WARRANTY; without even the implied warranty of<br>"
            + "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the<br>"
            + "GNU General Public License for more details.<br>"
            + "<br>"
            + "You should have received a copy of the GNU General Public License<br>"
            + "along with this program.  If not, see <a href=\"https://www.gnu.org/licenses\">www.gnu.org/licenses</a>."
            + "</body></html>", "License")

    def __listenerBDonation(self):
        MessageUtil.show_info_message("<html><body>"
                                      + "pyTranscriber is developed as a hobby, so donations of any value are welcomed."
                                      + "<br><br>If you feel that this software has been useful and would like to contribute for it to continue improving and have more and bugfixes and features like support to other Speech Recognition Engines (like Vosk and Mozilla Deep Speech) you can either join our <a href=\"https://github.com/sponsors/raryelcostasouza\">funding campaign at Github Sponsors</a> or make a <a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=YHB854YHPJCU8&item_name=Donation+pyTranscriber&currency_code=BRL\">Paypal donation</a>."
                                      + "<br><br>Thanks in advance!"
                                      + "</body></html>", "Funding")

    def __listenerBAboutpyTranscriber(self):
        MessageUtil.show_info_message("<html><body>"
                                      + "<a href=\"https://github.com/raryelcostasouza/pyTranscriber\">pyTranscriber</a> is an application that can be used "
                                      + "to generate <b>automatic transcription / automatic subtitles </b>"
                                      + "for audio/video files through a friendly graphical user interface. "
                                      + "<br><br>"
                                      + "The hard work of speech recognition is made by the <a href=\"https://cloud.google.com/speech/\">Google Speech Recognition API</a> "
                                      + "using <a href=\"https://github.com/agermanidis/autosub\">Autosub</a>"
                                      + "<br><br>pyTranscriber is developed as a hobby, so donations of any value are welcomed."
                                      + "<br><br>If you feel that this software has been useful and would like to contribute for it to continue improving and have more and bugfixes and features like support to other Speech Recognition Engines (like Vosk and Mozilla Deep Speech) you can either join our <a href=\"https://github.com/sponsors/raryelcostasouza\">funding campaign at Github Sponsors</a> or make a <a href=\"https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=YHB854YHPJCU8&item_name=Donation+pyTranscriber&currency_code=BRL\">Paypal donation</a>."
                                      + "<br><br>Thanks in advance!"
                                      + "</body></html>", "About pyTranscriber")
