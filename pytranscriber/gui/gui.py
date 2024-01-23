# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pytranscriber/gui/gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_window(object):
    def setupUi(self, window):
        window.setObjectName("window")
        window.resize(1045, 487)
        self.centralwidget = QtWidgets.QWidget(window)
        self.centralwidget.setObjectName("centralwidget")
        self.bSelectMedia = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectMedia.setGeometry(QtCore.QRect(10, 10, 141, 34))
        self.bSelectMedia.setObjectName("bSelectMedia")
        self.bConvert = QtWidgets.QPushButton(self.centralwidget)
        self.bConvert.setEnabled(False)
        self.bConvert.setGeometry(QtCore.QRect(200, 290, 341, 34))
        self.bConvert.setObjectName("bConvert")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(20, 340, 1021, 23))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")
        self.labelCurrentOperation = QtWidgets.QLabel(self.centralwidget)
        self.labelCurrentOperation.setGeometry(QtCore.QRect(170, 350, 871, 41))
        self.labelCurrentOperation.setText("")
        self.labelCurrentOperation.setObjectName("labelCurrentOperation")
        self.bOpenOutputFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bOpenOutputFolder.setGeometry(QtCore.QRect(550, 290, 241, 34))
        self.bOpenOutputFolder.setObjectName("bOpenOutputFolder")
        self.bSelectOutputFolder = QtWidgets.QPushButton(self.centralwidget)
        self.bSelectOutputFolder.setGeometry(QtCore.QRect(10, 180, 141, 34))
        self.bSelectOutputFolder.setObjectName("bSelectOutputFolder")
        self.qleOutputFolder = QtWidgets.QLineEdit(self.centralwidget)
        self.qleOutputFolder.setGeometry(QtCore.QRect(160, 180, 861, 32))
        self.qleOutputFolder.setText("")
        self.qleOutputFolder.setReadOnly(True)
        self.qleOutputFolder.setObjectName("qleOutputFolder")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(160, 10, 871, 161))
        self.groupBox.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.groupBox.setFlat(False)
        self.groupBox.setCheckable(False)
        self.groupBox.setObjectName("groupBox")
        self.qlwListFilesSelected = QtWidgets.QListWidget(self.groupBox)
        self.qlwListFilesSelected.setGeometry(QtCore.QRect(10, 30, 851, 121))
        self.qlwListFilesSelected.setObjectName("qlwListFilesSelected")
        self.bRemoveFile = QtWidgets.QPushButton(self.centralwidget)
        self.bRemoveFile.setGeometry(QtCore.QRect(10, 50, 141, 34))
        self.bRemoveFile.setObjectName("bRemoveFile")
        self.labelProgressFileIndex = QtWidgets.QLabel(self.centralwidget)
        self.labelProgressFileIndex.setGeometry(QtCore.QRect(30, 350, 131, 41))
        self.labelProgressFileIndex.setText("")
        self.labelProgressFileIndex.setObjectName("labelProgressFileIndex")
        self.bCancel = QtWidgets.QPushButton(self.centralwidget)
        self.bCancel.setGeometry(QtCore.QRect(470, 390, 108, 36))
        self.bCancel.setObjectName("bCancel")
        self.chbxOpenOutputFilesAuto = QtWidgets.QCheckBox(self.centralwidget)
        self.chbxOpenOutputFilesAuto.setGeometry(QtCore.QRect(10, 220, 291, 32))
        self.chbxOpenOutputFilesAuto.setChecked(True)
        self.chbxOpenOutputFilesAuto.setObjectName("chbxOpenOutputFilesAuto")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(200, 250, 591, 38))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.labelSelectLang = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.labelSelectLang.setObjectName("labelSelectLang")
        self.horizontalLayout_5.addWidget(self.labelSelectLang)
        self.cbSelectLang = QtWidgets.QComboBox(self.horizontalLayoutWidget)
        self.cbSelectLang.setSizeAdjustPolicy(QtWidgets.QComboBox.AdjustToContents)
        self.cbSelectLang.setObjectName("cbSelectLang")
        self.horizontalLayout_5.addWidget(self.cbSelectLang)
        window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1045, 27))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        self.menuProxy = QtWidgets.QMenu(self.menubar)
        self.menuProxy.setObjectName("menuProxy")
        self.menuLanguage = QtWidgets.QMenu(self.menubar)
        self.menuLanguage.setObjectName("menuLanguage")
        window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(window)
        self.statusbar.setObjectName("statusbar")
        window.setStatusBar(self.statusbar)
        self.actionLicense = QtWidgets.QAction(window)
        self.actionLicense.setObjectName("actionLicense")
        self.actionDonation = QtWidgets.QAction(window)
        self.actionDonation.setObjectName("actionDonation")
        self.actionAbout_pyTranscriber = QtWidgets.QAction(window)
        self.actionAbout_pyTranscriber.setObjectName("actionAbout_pyTranscriber")
        self.actionProxy = QtWidgets.QAction(window)
        self.actionProxy.setObjectName("actionProxy")
        self.actionEnglish = QtWidgets.QAction(window)
        self.actionEnglish.setObjectName("actionEnglish")
        self.actionChineseTraditional = QtWidgets.QAction(window)
        self.actionChineseTraditional.setObjectName("actionChineseTraditional")
        self.actionChineseSimplified = QtWidgets.QAction(window)
        self.actionChineseSimplified.setObjectName("actionChineseSimplified")
        self.actionPortuguese = QtWidgets.QAction(window)
        self.actionPortuguese.setObjectName("actionPortuguese")
        self.menuAbout.addAction(self.actionLicense)
        self.menuAbout.addAction(self.actionDonation)
        self.menuAbout.addAction(self.actionAbout_pyTranscriber)
        self.menuProxy.addAction(self.actionProxy)
        self.menuLanguage.addAction(self.actionEnglish)
        self.menuLanguage.addAction(self.actionChineseTraditional)
        self.menuLanguage.addAction(self.actionChineseSimplified)
        self.menuLanguage.addAction(self.actionPortuguese)
        self.menubar.addAction(self.menuProxy.menuAction())
        self.menubar.addAction(self.menuLanguage.menuAction())
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(window)
        QtCore.QMetaObject.connectSlotsByName(window)

    def retranslateUi(self, window):
        _translate = QtCore.QCoreApplication.translate
        window.setWindowTitle(_translate("window", "pyTranscriber v2.0 BETA - 23/01/2024"))
        self.bSelectMedia.setText(_translate("window", "Select file(s)"))
        self.bConvert.setText(_translate("window", "Transcribe Audio / Generate Subtitles"))
        self.bOpenOutputFolder.setText(_translate("window", "Open Output Folder"))
        self.bSelectOutputFolder.setText(_translate("window", "Output Location"))
        self.groupBox.setTitle(_translate("window", "List of files to generate transcribe audio / generate subtitles"))
        self.bRemoveFile.setText(_translate("window", "Remove file(s)"))
        self.bCancel.setText(_translate("window", "Cancel"))
        self.chbxOpenOutputFilesAuto.setText(_translate("window", "Open output files automatically"))
        self.labelSelectLang.setText(_translate("window", "Audio Language:"))
        self.menuAbout.setTitle(_translate("window", "Abo&ut"))
        self.menuProxy.setTitle(_translate("window", "&Settings"))
        self.menuLanguage.setTitle(_translate("window", "&Language"))
        self.actionLicense.setText(_translate("window", "&License"))
        self.actionDonation.setText(_translate("window", "&Funding at Github Sponsors"))
        self.actionAbout_pyTranscriber.setText(_translate("window", "&About pyTranscriber"))
        self.actionProxy.setText(_translate("window", "&Proxy"))
        self.actionProxy.setToolTip(_translate("window", "Proxy setting"))
        self.actionEnglish.setText(_translate("window", "English"))
        self.actionChineseTraditional.setText(_translate("window", "繁體中文 - Chinese Traditional"))
        self.actionChineseSimplified.setText(_translate("window", "简体中文 - Chinese Simplified"))
        self.actionPortuguese.setText(_translate("window", "Português"))
