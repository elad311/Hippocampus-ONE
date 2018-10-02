#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, random, math, os, sqlite3
import sizegrip as sg

class Example(QMainWindow):
    toolbaropen = 0

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)

        self.initUI()
        self.setMouseTracking(True)
        self.nodes = []
        self.node_count = 1
        self.node_to_connect = None
        self.at_least_one_connection = False
        self.mode_handler = None
        self.node_to_move = None
        self.node_to_change = None
        self.UPPER_LIMIT = 45
        self.setContextMenuPolicy(Qt.NoContextMenu)   #PREVENTS CONTEXT MENU
        self.pressedDownButton = [QPushButton()]
        self.nodeUnderEdit = []
        self.mode('none')

    def initFormatbar(self, x, y, node):

        self.fontSize = QSpinBox(self)
        # Will display " pt" after each value
        self.fontSize.setSuffix(" pt")
        self.fontSize.setValue(14)
        # fontSize.valueChanged.connect(lambda size: self.setFontPointSize(size))

        # fontColor = QAction(QIcon(":/font-color.png"), "Change font color", self)
        # fontColor.triggered.connect(self.font_Color_Changed)

        self.boldAction = QAction(QIcon("bold.png"), "Bold", self)
        self.boldAction.triggered.connect(node.bold)
        self.boldAction.triggered.connect(lambda: self.returnFocusToTextAfterToolbarClick(node))

        #self.boldAction2 = QPushButton()                #------ how to get icon into a button
        #self.boldAction2.setIcon(QIcon(QPixmap("bold.png")))
        #self.boldAction2.setIconSize(QPixmap("bold.png").rect().size())
        #self.boldAction2.clicked.connect(node.bold)

        self.enlargeButton = QPushButton("enlarge")
        self.enlargeButton.clicked.connect(lambda: node.resize(node.width() +30, node.height()))

        print(node)
        # self.italicAction = QAction(QIcon("icons/italic.png"), "Italic", self)
        # italicAction.triggered.connect(self.italic)

        # self.underlAction = QAction(QIcon("icons/underline.png"), "Underline", self)
        # underlAction.triggered.connect(self.underline)

        # self.strikeAction = QAction(QIcon("icons/strike.png"), "Strike-out", self)
        # strikeAction.triggered.connect(self.strike)

        # self.superAction = QAction(QIcon("icons/superscript.png"), "Superscript", self)
        # superAction.triggered.connect(self.superScript)

        # self.subAction = QAction(QIcon("icons/subscript.png"), "Subscript", self)
        # subAction.triggered.connect(self.subScript)

        # self.alignLeft = QAction(QIcon("icons/align-left.png"), "Align left", self)
        # alignLeft.triggered.connect(self.alignLeft)

        # self.alignCenter = QAction(QIcon("icons/align-center.png"), "Align center", self)
        # alignCenter.triggered.connect(self.alignCenter)

        # self.alignRight = QAction(QIcon("icons/align-right.png"), "Align right", self)
        # alignRight.triggered.connect(self.alignRight)

        # self.alignJustify = QAction(QIcon("icons/align-justify.png"), "Align justify", self)
        # alignJustify.triggered.connect(self.alignJustify)

        # self.indentAction = QAction(QIcon("icons/indent.png"), "Indent Area", self)
        # indentAction.setShortcut("Ctrl+Tab")
        # indentAction.triggered.connect(self.indent)

        # self.dedentAction = QAction(QIcon("icons/dedent.png"), "Dedent Area", self)
        # dedentAction.setShortcut("Shift+Tab")
        # dedentAction.triggered.connect(self.dedent)

        # self.backColor = QAction(QIcon("icons/highlight.png"), "Change background color", self)
        # backColor.triggered.connect(self.highlight)

        self.formatbar = self.addToolBar('Format')
        self.formatbar.setMovable(True)

        self.formatbar.addWidget(self.fontSize)
        #self.formatbar.addAction(fontColor)
        self.formatbar.addAction(self.boldAction)
        self.formatbar.addWidget(self.enlargeButton)

        self.formatbar.show()
        # self.formatbar.addSeparator()

        # self.formatbar.addAction(self.fontColor)
        # self.formatbar.addAction(self.backColor)

        # self.formatbar.addSeparator()

        # self.formatbar.addAction(self.boldAction)
        # self.formatbar.addAction(self.italicAction)
        # self.formatbar.addAction(self.underlAction)
        # --------------------------------------------------------------------------------------------------------------
        # doesn't work well
        # self.formatbar.addAction(self.strikeAction)
        # self.formatbar.addAction(self.superAction)
        # self.formatbar.addAction(self.subAction)
        # --------------------------------------------------------------------------------------------------------------

        # self.formatbar.addSeparator()

        # self.formatbar.addAction(self.alignLeft)
        # self.formatbar.addAction(self.alignCenter)
        # self.formatbar.addAction(self.alignRight)
        # self.formatbar.addAction(self.alignJustify)

        # self.formatbar.addSeparator()

        # self.formatbar.addAction(self.indentAction)
        # self.formatbar.addAction(self.dedentAction)
        self.formatbar.setAllowedAreas(Qt.NoToolBarArea)
        self.formatbar.setFloatable(True)
        self.formatbar.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint)
        self.formatbar.adjustSize()
        self.formatbar.move(x, y)

        self.statusbar = self.statusBar()


    def fakeFormatbar(self):
        self.fontBox = QFontComboBox(self)
        # fontBox.currentFontChanged.connect(lambda font: self.setCurrentFont(font))

        self.fontSize = QSpinBox(self)
        # Will display " pt" after each value
        self.fontSize.setSuffix(" pt")
        self.fontSize.setValue(14)

        self.formatbar = self.addToolBar('Format')
        self.formatbar.setMovable(True)

        self.formatbar.addWidget(self.fontBox)
        self.formatbar.addWidget(self.fontSize)

        self.formatbar.show()
        self.statusbar = self.statusBar()

    def initMainbar(self):

        self.makeNode = QPushButton("Node  ()")
        self.makeNode.clicked.connect(lambda: self.mode('Regular'))
        self.makeNode.clicked.connect(lambda: self.setButtonDown_releaseOthers(self.makeNode))

        self.makeArrows = QPushButton("Arrows  ()")
        self.makeArrows.clicked.connect(lambda: self.mode('Arrows'))
        self.makeArrows.clicked.connect(lambda: self.setButtonDown_releaseOthers(self.makeArrows))


        #---------------  spacer
        self.mainbar_spacer = QWidget()
        self.mainbar_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #---------------------  Save & Load

        self.saveCanvas = QPushButton("Save")
        self.saveCanvas.clicked.connect(self.save_canvas)
        self.loadCanvas = QPushButton("Load")
        self.loadCanvas.clicked.connect(self.load_canvas)


        self.mainbar = self.addToolBar('Main')
        self.mainbar.addWidget(self.makeNode)
        self.mainbar.addSeparator()
        self.mainbar.addWidget(self.makeArrows)
        self.mainbar.addSeparator()
        #spacer
        self.mainbar.addWidget(self.mainbar_spacer)
        #spacer
        self.mainbar.addWidget(self.saveCanvas)
        self.mainbar.addSeparator()
        self.mainbar.addWidget(self.loadCanvas)
        self.mainbar.show()

    def setButtonDown_releaseOthers(self, button):
        if button is False:
            self.pressedDownButton[0].setDown(False)
        else:
            self.pressedDownButton[0].setDown(False)
            self.pressedDownButton.clear()
            button.setDown(True)
            self.pressedDownButton.append(button)

    def initUI(self):
        windowWidth = 1800
        windowHeight = 900
        screenCenter = QDesktopWidget().availableGeometry().center()
        self.setGeometry(screenCenter.x() - (windowWidth/2), screenCenter.y() - (windowHeight/2), windowWidth, windowHeight)
        self.setWindowTitle('Hippocampus ONE')
        # self.label = QLabel(self)

        menubar = self.menuBar()

        file_menu = menubar.addMenu('File')

        clear_action = QAction('Clear', self)
        clear_action.triggered.connect(self.clear_canvas)

        file_menu.addAction(clear_action)

        self.fakeFormatbar()
        self.removeToolBar(self.formatbar)
        self.initMainbar()

        self.show()
        self.node_to_draw_points = None

    def mousePressEvent(self, event): #allows deletion if dragging away using MIDDLE BUTTON
        if event.buttons() == Qt.MidButton and self.mode_handler in ['Regular', 'Special']:
            for node in self.nodes:
                x1, x2, y1, y2 = self.coords(node)
                if x1 - 10 < event.pos().x() < x2 + 10 and y1 - 10 < event.pos().y() < y2 + 10 and node.hasFocus() and self.node_to_change is None:
                    for nod in self.nodes:
                        if node in nod.connected_to:
                            nod.connected_to.remove(node)
                    self.nodes.remove(node)
                    node.setParent(None)
                    node.close()
                    del node
                    self.statusbar.showMessage('')
                    return
        if event.buttons() == Qt.RightButton and self.mode_handler in ['Regular', 'Special', 'Arrows']: #add modes FROM MAINBAR here to cancel on right click
            self.mode('none')
            self.setButtonDown_releaseOthers(False)

    def mouseMoveEvent(self, event):
        if self.mode_handler in ['Regular', 'Special', 'none']:
            if self.node_to_move is None:
                for node in self.nodes:
                    x1, x2, y1, y2 = self.coords(node)
                    cursorSensitivity = 28
                    if x1 - cursorSensitivity < event.pos().x() < x2 + cursorSensitivity and y1 - cursorSensitivity < event.pos().y() < y2 + cursorSensitivity and node.hasFocus() and self.node_to_change is None:
                        self.setCursor(Qt.SizeAllCursor)
                        if event.buttons() == Qt.LeftButton:
                            self.node_to_move = (
                                node, event.pos().x(), event.pos().y())
                        return
            if self.node_to_move is not None:   #allows moving NODE
                x1, x2, y1, y2 = self.coords(self.node_to_move[0])
                width = x2 - x1
                height = y2 - y1
                if y1 + event.pos().y() - self.node_to_move[2] > self.UPPER_LIMIT:
                    self.node_to_move[0].setGeometry(x1 + event.pos().x() - self.node_to_move[1],
                                                     y1 + event.pos().y() - self.node_to_move[2], width, height)
                else:
                    self.node_to_move[0].setGeometry(x1 + event.pos().x() - self.node_to_move[1], self.UPPER_LIMIT, width, height)
                self.node_to_move = (self.node_to_move[0], event.pos().x(), event.pos().y())
                return
            elif event.buttons() == Qt.LeftButton:
                if self.node_to_change is None:
                    self.node_to_change = (
                        Node(self), event.pos().x(), event.pos().y())
                    self.node_to_change[0].setGeometry(event.pos().x(),
                                                       event.pos().y(), 0, 0)
                    self.node_to_change[0].show()
                elif self.node_to_change is not None and self.node_to_move is None:
                    self.node_to_change[0].handle.move(self.node_to_change[0].width() - 20,
                                                       self.node_to_change[0].height() - 20) #hold sizegrip in corner
                    if event.pos().x() - self.node_to_change[1] > 0:
                        x1 = self.node_to_change[1]
                    else:
                        x1 = event.pos().x()
                    if event.pos().y() - self.node_to_change[2] > 0:
                        y1 = self.node_to_change[2]
                    else:
                        y1 = event.pos().y()
                    if y1 > self.UPPER_LIMIT:
                        self.node_to_change[0].setGeometry(x1, y1, math.fabs(event.pos().x() - self.node_to_change[1]),
                                                           math.fabs(event.pos().y() - self.node_to_change[2]))
                    else:
                        self.node_to_change[0].setGeometry(x1, self.UPPER_LIMIT, math.fabs(event.pos().x() - self.node_to_change[1]),
                                                           self.node_to_change[0].height())

            self.setCursor(Qt.ArrowCursor)

    def mouseReleaseEvent(self, event):     #contains loops for printing NODES info
        if self.node_to_change is not None:
            self.nodes.append(self.node_to_change[0])
            self.node_to_change[0].index = self.node_count
            self.node_to_change[0].handle.move(self.node_to_change[0].width() -20, self.node_to_change[0].height() -20)
            for node in self.nodes:
                print(node)
                for nod in node.connected_to:
                    print(nod)
            self.node_to_change = None
            self.node_count += 1

        if self.node_to_move is not None:
            self.node_to_move = None

    # ---------------------------------------------------------------------------------------------- new
    def paintEvent(self, event):  #allows drawing lines
        # if self.at_least_one_connection:  # if connections exist, draw them
        qp = QPainter(self)
        qp.setRenderHint(QPainter.HighQualityAntialiasing)
        qp.setPen(QPen(QBrush(Qt.black), 12))
        for node in self.nodes:
            for to in node.connected_to:
                qp.drawLine(node.x() + node.width() / 2, node.y() + node.height() / 2, to.x() + to.width() / 2,
                            to.y() + to.height() / 2)
        self.update()

    def coords(self, node):
        return node.x(), node.x() + node.width(), node.y(), node.y() + node.height()

    def mode(self, new_mode):  # sets current mode based off buttons  # , info
        self.mode_handler = new_mode
        self.removeToolBar(self.formatbar)
        self.toolbaropen = 0
        self.node_to_connect = None
        self.statusbar.showMessage(str(new_mode))

    def bold(self, node):    #UNUSED
        if node.hasFocus():
            if node.fontWeight() == QFont.Bold:
                node.setFontWeight(QFont.Normal)
            else:
                node.setFontWeight(QFont.Bold)

    def returnFocusToTextAfterToolbarClick(self, node):
        print('oy')
        self.removeToolBar(self.formatbar)
        self.initFormatbar(self.x() + node.x(), self.y() + node.y() - 5, node)

    def save_canvas(self):
        if os.path.exists('canvas_new.db'):
            os.remove('canvas_new.db')
        conn = sqlite3.connect('canvas_new.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE nodes (x1, x2, y1, y2, type, name)''')
        c.execute('''CREATE TABLE arrows (start, end)''')
        for node in self.nodes:
            print(str(self.coords(node)))
            c.execute("INSERT INTO nodes VALUES(?,?,?,?,?,?)", (
            self.coords(node)[0], self.coords(node)[1], self.coords(node)[2], self.coords(node)[3], node.toHtml(), str(node))) # , [x[0].get_name() for x in rect.get_arrow_butts()]))
            for arrow in node.connected_to:
                c.execute("INSERT INTO arrows VALUES(?,?)", (str(node), str(arrow)))
        conn.commit()
        conn.close()
        print('saved successfully')

    def load_canvas(self):
        self.node_count = 1
        global rects_to_connect, rect_count
        conn = sqlite3.connect('canvas_new.db')
        c = conn.cursor()
        for row in c.execute('SELECT * FROM nodes'):
            a = Node(self)
            a.setGeometry(row[0], row[2], row[1] - row[0], row[3] - row[2]) #NOTICE DIFFERENT ORDER of variables!
            a.index = self.node_count
            self.node_count += 1
            self.nodes.append(a)
            a.setHtml(row[4])
            a.show()
            a.handle.move(a.width() - 20, a.height() - 20) #move handle ON LOAD
            print(str(self.coords(a)))
            """
        for node in rec_list:
            for row in c.execute('SELECT * FROM arrows' + str(node.get_name())):
                for rect in rec_list:
                    if int(rect.get_name()) == int(row[0]):
                        rects_to_connect = [rec_list[counter], rect]
                        connect_nodes()
            counter += 1
        for row in c.execute('SELECT * FROM rect_count'):
            rect_count = row[0]
            """
        print('loaded successfully')

    def clear_canvas(self):
        counter = 0
        for node in self.nodes:
            node.setParent(None)
            counter += 1
            node.deleteLater()
        print(str(self.nodes))
        self.nodes.clear()  #-------------------------CHECK for GARBAGE COLLECTION!
        del self.nodes
        self.nodes = []
        self.statusbar.showMessage('cleared everything')
        print('cleared everything')

class Node(QTextEdit):
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        #self.setFontFamily(ex.fontBox.currentFont().family())
        self.setFontPointSize(ex.fontSize.value())
        self.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'""" + ex.fontBox.currentFont().family() + """'; font-size:""" + str(ex.fontSize.value()) + """pt;"><br /></p></body></html>""")
        #ex.fontBox.currentFontChanged.connect(lambda font: self.setFontFamily(font.family()))
        #ex.fontBox.currentFontChanged.connect(self.text_change)
        ex.fontSize.valueChanged.connect(lambda size: self.setFontPointSize(size))
        ex.fontSize.valueChanged.connect(self.text_change)
        self.parent = parent
        # ex.fontColor.triggered.connect(self.font_color_changed)
        # ex.backColor.triggered.connect(self.highlight)
        # ex.boldAction.triggered.connect(self.bold)
        # ex.italicAction.triggered.connect(self.italic)
        # ex.underlAction.triggered.connect(self.underline)
        # --------------------------------------------------------------------------------------------------------------
        # doesn't work well
        # ex.strikeAction.triggered.connect(self.strike)
        # ex.superAction.triggered.connect(self.superScript)
        # ex.subAction.triggered.connect(self.subScript)
        # --------------------------------------------------------------------------------------------------------------
        # ex.alignLeft.triggered.connect(self.alignLeft)
        # ex.alignCenter.triggered.connect(self.alignCenter)
        # ex.alignRight.triggered.connect(self.alignRight)
        # ex.alignJustify.triggered.connect(self.alignJustify)
        # ex.indentAction.triggered.connect(self.indent)
        # ex.dedentAction.triggered.connect(self.dedent)
        self.index = None
        self.connected_to = []  #array for storing connections on EACH NODE
        self.textChanged.connect(self.text_change)
        self.selectionChanged.connect(self.cursor_change)
        self.cursorPositionChanged.connect(self.cursor_change)
        # currently not in use
        self.set_html = False
        #self.setStyleSheet("border: 2px solid red; border-radius: 10px; border-style: outset; padding: 2px")
        self.setWindowFlags(Qt.SubWindow)  #important for controlling only the node!
        self.handle = sg.sizegrip(self)

    """
    def initFormatbar(self, x, y):

        ex.fontBox = QFontComboBox(ex)
        # fontBox.currentFontChanged.connect(lambda font: self.setCurrentFont(font))

        ex.fontSize = QSpinBox(ex)
        # Will display " pt" after each value
        ex.fontSize.setSuffix(" pt")
        ex.fontSize.setValue(14)
        # fontSize.valueChanged.connect(lambda size: self.setFontPointSize(size))

        boldAction = QAction(QIcon("icons/bold.png"), "Bold", self)

        self.formatbar = ex.addToolBar('Format')
        self.formatbar.setMovable(True)


        ex.formatbar.addWidget(ex.fontBox)
        ex.formatbar.addWidget(ex.fontSize)
        self.formatbar.addAction(ex.boldAction)
        boldAction.triggered.connect(self.bold)

        ex.formatbar.show()
        ex.formatbar.setAllowedAreas(Qt.NoToolBarArea)
        ex.formatbar.setFloatable(True)
        ex.formatbar.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.X11BypassWindowManagerHint)
        ex.formatbar.adjustSize()
        ex.formatbar.move(x, y)

        ex.statusbar = ex.statusBar()
        """


    def contextMenuEvent(self, event):
        # indentAction = QAction(QIcon("icons/indent.png"), "Indent Area")
        # dedentAction = QAction(QIcon("icons/dedent.png"), "Dedent Area")
        menu = self.createStandardContextMenu()

        format_menu = QMenu('Format')

        fontColor = QAction(QIcon("icons/font-color.png"), "Change font color")
        format_menu.addAction(fontColor)
        fontColor.triggered.connect(self.font_color_changed)

        backColor = QAction(QIcon("icons/highlight.png"), "Change background color")
        format_menu.addAction(backColor)
        backColor.triggered.connect(self.highlight)

        boldAction = QAction(QIcon("icons/bold.png"), "Bold")  #------------------------------
        format_menu.addAction(boldAction)
        boldAction.triggered.connect(self.bold)

        italicAction = QAction(QIcon("icons/italic.png"), "Italic")
        format_menu.addAction(italicAction)
        italicAction.triggered.connect(self.italic)

        underlAction = QAction(QIcon("icons/underline.png"), "Underline")
        format_menu.addAction(underlAction)
        underlAction.triggered.connect(self.underline)

        alignLeft = QAction(QIcon("icons/align-left.png"), "Align left")
        format_menu.addAction(alignLeft)
        alignLeft.triggered.connect(self.alignLeft)

        alignCenter = QAction(QIcon("icons/align-center.png"), "Align center")
        format_menu.addAction(alignCenter)
        alignCenter.triggered.connect(self.alignCenter)

        alignRight = QAction(QIcon("icons/align-right.png"), "Align right")
        format_menu.addAction(alignRight)
        alignRight.triggered.connect(self.alignRight)

        alignJustify = QAction(QIcon("icons/align-justify.png"), "Align justify")
        format_menu.addAction(alignJustify)
        alignJustify.triggered.connect(self.alignJustify)

        superScript = QAction(QIcon("icons/superScript.png"), "Super Script")
        format_menu.addAction(superScript)
        superScript.triggered.connect(self.superScript)

        subScript = QAction(QIcon("icons/subScript.png"), "Sub Script")
        format_menu.addAction(subScript)
        superScript.triggered.connect(self.subScript)

        def_actions = menu.actions()

        for action in def_actions:
            menu.removeAction(action)

        menu.addMenu(format_menu)

        menu.addSeparator()

        for action in def_actions:
            menu.addAction(action)

        menu.exec_(event.globalPos())

    def dropEvent(self, event):
        filename = event.mimeData().text()[8::]
        if filename[-3::] in ['png', 'jpg']:
            image = QImage(filename)
            cursor = self.textCursor()
            cursor.movePosition(QTextCursor.End, QTextCursor.MoveAnchor)
            cursor.insertImage(image, filename)

        else:
            cursor = self.textCursor()
            cursor.insertText(filename)

    def mousePressEvent(self, event):
        if ex.toolbaropen == 0:
            ex.initFormatbar(ex.x() + self.x(), ex.y() + self.y() - 5, self) #set coords for toolbar
            ex.toolbaropen = 1
            ex.nodeUnderEdit.append(self)
        ex.statusbar.showMessage('Node ' + str(self.index))
        if event.buttons() == Qt.LeftButton and self.parent.mode_handler == 'Arrows':
            if not self.parent.node_to_connect:  # saves node that will be connected
                self.parent.node_to_connect = self
            elif self not in ex.node_to_connect.connected_to and ex.node_to_connect not in self.connected_to:  # if such a node already exists, and the node that should be connected to it isn't already connected, connect
                self.parent.node_to_connect.connected_to.append(self)
                self.parent.node_to_connect = None
                self.parent.at_least_one_connection = True  # at least one connection was made, so the painter should paint the connections

            else:
                self.parent.node_to_connect = None
        else:
            QTextEdit.mousePressEvent(self, event)

    # --------------------------------------------------------------------------------
    def cursor_change(self):
        self.parent.fontSize.blockSignals(True)
        self.parent.fontBox.blockSignals(True)
        self.parent.fontSize.setValue(self.fontPointSize())
        self.parent.fontBox.setCurrentFont(QFont(self.fontFamily()))
        self.parent.fontSize.blockSignals(False)
        self.parent.fontBox.blockSignals(False)

    def text_change(self):
        if len(self.toPlainText()) == 0:
            self.textChanged.disconnect(self.text_change)
            self.setFontFamily(self.parent.fontBox.currentFont().family())
            self.setFontPointSize(self.parent.fontSize.value())
            self.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'""" + self.parent.fontBox.currentFont().family() + """'; font-size:""" + str(self.parent.fontSize.value()) + """pt;"><br /></p></body></html>""")
            #self.set_html = True
            self.textChanged.connect(self.text_change)

    def font_color_changed(self):
        if self.hasFocus():
            # Get a color from the text dialog
            color = QColorDialog.getColor()
            # Set it as the new text color
            if color.isValid():
                self.setTextColor(color)

    def highlight(self):
        if self.hasFocus():
            color = QColorDialog.getColor()

            self.setTextBackgroundColor(color)

    def bold(self):   #need to bring back focus to NODE AFTER PRESSING THE TOOLBAR
        #if self.hasFocus():
        print('made bold')
        if self.fontWeight() == QFont.Bold:
            self.setFontWeight(QFont.Normal)
        else:
            self.setFontWeight(QFont.Bold)


    def italic(self):
        if self.hasFocus():
            state = self.fontItalic()

            self.setFontItalic(not state)

    def underline(self):
        if self.hasFocus():
            state = self.fontUnderline()

            self.setFontUnderline(not state)

    def strike(self):
        if self.hasFocus():
            # Grab the text's format
            fmt = self.currentCharFormat()

            # Set the fontStrikeOut property to its opposite
            fmt.setFontStrikeOut(not fmt.fontStrikeOut())

            # And set the next char format
            self.setCurrentCharFormat(fmt)

    def superScript(self):
        if self.hasFocus():
            # Grab the current format
            fmt = self.currentCharFormat()

            # And get the vertical alignment property
            align = fmt.verticalAlignment()

            # Toggle the state
            if align == QTextCharFormat.AlignNormal:

                fmt.setVerticalAlignment(QTextCharFormat.AlignSuperScript)

            else:

                fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

            # Set the new format
            self.setCurrentCharFormat(fmt)

    def subScript(self):
        if self.hasFocus():
            # Grab the current format
            fmt = self.currentCharFormat()

            # And get the vertical alignment property
            align = fmt.verticalAlignment()

            # Toggle the state
            if align == QTextCharFormat.AlignNormal:

                fmt.setVerticalAlignment(QTextCharFormat.AlignSubScript)

            else:

                fmt.setVerticalAlignment(QTextCharFormat.AlignNormal)

            # Set the new format
            self.setCurrentCharFormat(fmt)

    def alignLeft(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignJustify)

if __name__ == '__main__':
    counter = 0
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
