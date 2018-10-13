from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

class new_canvas_dialog(QDialog):
    NumGridRows = 1
    NumButtons = 4

    def __init__(self, parent=None):
        super(new_canvas_dialog, self).__init__()

        self.parent = parent
        self.new_canvas_form()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.search_file)
        buttonBox.rejected.connect(self.clicked_exit)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Create new canvas")


    def new_canvas_form(self):
        self.name_lineedit = QLineEdit()
        self.name_lineedit.setStyleSheet("border: 1px solid black")
        self.name_lineedit.setCompleter(self.parent.completer)
        self.formGroupBox = QGroupBox("New Canvas")
        self.errormessage = QLabel('')
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.name_lineedit)
        layout.addRow(self.errormessage)
        self.formGroupBox.setLayout(layout)

    def clicked_exit(self):
        self.closeEvent(QCloseEvent)

    def clicked_ok(self):
        self.parent.new_canvas(self.name_lineedit.text())
        self.closeEvent(QCloseEvent)

    def showEvent(self, QShowEvent):
        print('opened new canvas dialog')
        self.parent.refresh_completion_list()

    def closeEvent(self, QCloseEvent):
        self.name_lineedit.setStyleSheet("border: 1px solid black")
        self.errormessage.setText('')
        self.name_lineedit.clear()
        self.close()

    def search_file(self): #makes sure the file doesn't already exist
        filename = str(self.name_lineedit.text() + '.db')
        cur_dir = os.getcwd() #current path

        if filename in os.listdir(cur_dir): #searches in list of all files in current directory
            print('already exists')
            self.name_lineedit.setStyleSheet("border: 2px solid red")
            self.name_lineedit.setText('')
            self.errormessage.setText('Already exists')
            return
        else:
            self.clicked_ok()
            self.closeEvent(QCloseEvent)

class link_node_dialog(QDialog):
    NumGridRows = 1
    NumButtons = 4

    def __init__(self, parent=None, node=None):
        super(link_node_dialog, self).__init__()

        self.parent = parent
        self.new_canvas_form()

        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttonBox.accepted.connect(self.search_file)
        buttonBox.rejected.connect(self.clicked_exit)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.formGroupBox)
        mainLayout.addWidget(buttonBox)
        self.setLayout(mainLayout)

        self.setWindowTitle("Linking")


    def new_canvas_form(self):
        self.name_lineedit = QLineEdit()
        self.name_lineedit.setCompleter(self.parent.completer)
        self.formGroupBox = QGroupBox("Link this node")
        layout = QFormLayout()
        layout.addRow(QLabel("Name:"), self.name_lineedit)
        self.formGroupBox.setLayout(layout)

    def showEvent(self, QShowEvent):
        print('opened linking dialog')
        self.node = self.parent.temporaryNode
        if self.node.link is not None:
            self.name_lineedit.setText(str(self.node.link))
        self.parent.refresh_completion_list()

    def closeEvent(self, QCloseEvent):
        self.name_lineedit.clear()
        self.close()

    def clicked_exit(self):
        self.closeEvent(QCloseEvent)

    def clicked_ok(self):
        #self.parent.new_canvas(self.name_lineedit.text())
        if self.name_lineedit.text() == '':
            self.node.got_delinked()
            self.parent.enlargeButton.setText('Link')
        else:
            self.node.got_linked(str(self.name_lineedit.text()))
            self.parent.enlargeButton.setText(str(self.node.link))  ##changing link button on toolbar to linked name
            print("linked node to: " + self.node.link)
        self.closeEvent(QCloseEvent)

    def search_file(self): #makes sure the file doesn't already exist
        filename = str(self.name_lineedit.text() + '.db')
        cur_dir = os.getcwd() #current path

        if filename not in os.listdir(cur_dir) and self.name_lineedit != None: #searches in list of all files in current directory
            print('does not exist, creating new canvas: ' + self.name_lineedit.text())
            self.parent.new_canvas(self.name_lineedit.text())
            self.clicked_ok()
            return
        else:
            self.clicked_ok()
