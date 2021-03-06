# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
#####################################################################

# FrenchMasterSword, Cryptix, 2018
#####################################################################

import json
from PySide2.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QAction,
    QGroupBox, QHBoxLayout, QComboBox, QPushButton, QGridLayout, QTextEdit,
    QLineEdit, QDialog, QLabel, QApplication, QMessageBox, QFileDialog)
from PySide2.QtGui import QIcon, QPixmap, QKeySequence
from PySide2.QtCore import QFile, QTextStream, Qt, QTranslator, QLocale

import encrypt

with open('settings.json', 'r') as file:
    settingsDict = json.load(file)

algoDict = {
    'Simple': encrypt.simple,
    'Wolseley': encrypt.wolseley,
    'Caesar': encrypt.caesar,
    'Affine': encrypt.affine,
    'Polybius': encrypt.polybius,
    'ADFGVX': encrypt.adfgvx,
    'Vigenere': encrypt.vigenere,
    'Gronsfeld': encrypt.gronsfeld,
    'Beaufort': encrypt.beaufort,
    'Collon': encrypt.collon,
    'Morse': encrypt.morse,
}

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        widget = QWidget()
        self.setCentralWidget(widget)

        self.create_actions()
        self.create_menus()
        self.create_status_bar()
        self.create_algo_box()
        self.create_crypto_box()

        mainLayout = QVBoxLayout()
        mainLayout.setSpacing(10)

        mainLayout.addWidget(self.algoBox)
        mainLayout.addWidget(self.cryptoBox)

        self.resize(900, 800)
        self.setWindowTitle('Cryptix')
        self.setWindowIcon(QIcon('lock.png'))

        widget.setLayout(mainLayout)

    def create_actions(self):
        self.openAct = QAction('&Open file', self,
            shortcut=QKeySequence.Open,
            statusTip="Open an existing file",
            triggered=self.open)

        self.guideAct = QAction('&Guide', self,
            shortcut='Ctrl+H',
            statusTip="Displays a quick How-To",
            triggered=self.guide)

        self.aboutAct = QAction('&About', self,
            statusTip="Displays info about this software",
            triggered=self.about)

        self.aboutQtAct = QAction('About &Qt', self,
            statusTip="Show the Qt library's About box",
            triggered=self.aboutQt)

    def create_menus(self):

        self.fileMenu = self.menuBar().addMenu('&File')
        self.fileMenu.addAction(self.openAct)

        self.helpMenu = self.menuBar().addMenu('&Help')
        self.helpMenu.addAction(self.guideAct)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.aboutAct)
        self.helpMenu.addAction(self.aboutQtAct)

        self.settingsMenu = self.menuBar().addMenu('&Settings')
        # self.settingsMenu.addAction()

    def create_status_bar(self):
        self.statusBar().showMessage("Ready")

    def create_algo_box(self):
        self.algoBox = QGroupBox('Cipher')
        layout = QHBoxLayout()

        self.algoCombo = QComboBox()
        self.algoCombo.addItems([*algoDict])
        self.algoCombo.activated.connect(self.change_keys)

        self.algoHelp = QPushButton('&Reminder',
        shortcut='Ctrl+R', clicked=self.reminder)

        layout.addWidget(self.algoCombo)
        layout.addWidget(self.algoHelp)

        self.algoBox.setLayout(layout)

    def create_crypto_box(self):
        self.cryptoBox = QGroupBox()
        layout = QGridLayout()

        self.encryptEdit = QTextEdit()
        self.encryptEdit.setPlaceholderText('Encrypt text')

        self.decryptEdit = QTextEdit()
        self.decryptEdit.setPlaceholderText('Decrypt text')

        self.keyEdit = QLineEdit()
        self.keyEdit.setPlaceholderText('Key if needed')

        self.keyEdit2 = QLineEdit()
        self.keyEdit2.setPlaceholderText('Second key if needed')
        self.keyEdit2.setEnabled(False) # The first cipher needs one key

        self.encryptBtn = QPushButton('&Encrypt',
        shortcut='Ctrl+E', clicked=lambda: self.process(True))

        self.decryptBtn = QPushButton('&Decrypt',
        shortcut='Ctrl+D', clicked=lambda: self.process(False))

        layout.addWidget(self.encryptEdit, 0, 0)
        layout.addWidget(self.decryptEdit, 0, 1)
        layout.addWidget(self.keyEdit, 1, 0, 1, 2)
        layout.addWidget(self.keyEdit2, 2, 0, 2, 2)
        layout.addWidget(self.encryptBtn, 4, 0)
        layout.addWidget(self.decryptBtn, 4, 1)

        self.cryptoBox.setLayout(layout)

    def open(self):
        fileName, _ = QFileDialog.getOpenFileName(self)
        if fileName:
            self.load_file(fileName)

    def guide(self):
        QMessageBox.information(self, "How to use Cryptix",
                "To encrypt or decrypt text : paste it respectively"
                " in the first and second text block, and press"
                " the according button.\n\n"

                "To change the current cipher, use the popup list"
                " on the left.\n\n"

                "Depending of ciphers, you might change specific settings.\n\n"

                "A quick reminder for the current cipher is"
                " accessible with the button next to the list.")

    def about(self):
        QMessageBox.about(self, "About Cryptix",
                '<b>Cryptix</b> is a small tool for quick encrypting and'
                ' decrypting of small texts, using known basic methods.'
                ' It is developed by FrenchMasterSword and available on'
                ' <a href="https://github.com/FrenchMasterSword/Cryptix">github</a>')

    def aboutQt(self):
        QMessageBox.aboutQt(self, "About Qt")

    def reminder(self):
        box = QDialog(self)

        algo = self.algoCombo.currentText()

        pixmap = QPixmap(f'images/{algo.lower()}.png')
        labelImage = QLabel()
        labelImage.setPixmap(pixmap)
        labelImage.setAlignment(Qt.AlignHCenter)

        labelText = QLabel(algoDict[algo].__doc__)
        labelText.setAlignment(Qt.AlignJustify)

        box.setWindowTitle(f"{algo} reminder")

        layout = QVBoxLayout()
        layout.addWidget(labelImage)
        layout.addWidget(labelText)

        box.setLayout(layout)
        box.show()

    def process(self, encrypt: bool):
        args = [self, encrypt]
        if encrypt:
            args.append(self.encryptEdit.toPlainText())
        else:
            args.append(self.decryptEdit.toPlainText())

        algo = self.algoCombo.currentText()
        if self.keyEdit.isEnabled():
            args.append(self.keyEdit.text())
        if self.keyEdit2.isEnabled():
            args.append(self.keyEdit2.text())

        result = algoDict[algo][0](*args)

        if type(result) == str:
            # Avoid erasing input if incorrect
            if encrypt:
                self.decryptEdit.setPlainText(result)
            else:
                self.encryptEdit.setPlainText(result)

    def change_keys(self):
        if 'key' in algoDict[self.algoCombo.currentText()].__annotations__:
        # qand not self.keyEdit.isEnabled()
            self.keyEdit.setEnabled(True)
        else:
            self.keyEdit.setEnabled(False)
        if 'key2' in algoDict[self.algoCombo.currentText()].__annotations__:
            self.keyEdit2.setEnabled(True)
        else:
            self.keyEdit2.setEnabled(False)

    def load_file(self, fileName):
        file = QFile(fileName)
        if not file.open(QFile.ReadOnly | QFile.Text):
            QMessageBox.warning(self, "Cryptix",
            f"Cannot read {fileName} :\n{file.errorString()}")
            return

        stream = QTextStream(file)
        self.encryptEdit.setPlainText(stream.readAll())

        self.statusBar().showMessage("File loaded", 2000)

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)

    french = QTranslator()

    if french.load("fr_fr", "translations"):
        app.installTranslator(french)

    main = MainWindow()
    main.show()
    # wid = QComboBox()
    # for method in dir(wid):
    #     if '__' not in method: print(method)
    # print(title)
    # print("Cryptix Version 0.3.0")
    # print("----------------------------------------\n")
    sys.exit(app.exec_())
