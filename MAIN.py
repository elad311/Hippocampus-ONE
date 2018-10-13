#!/usr/bin/python3
# -*- coding: utf-8 -*-
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QDesktopWidget
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sys, random, math, os, sqlite3
from nodes import *
from painter import *
from dialogs import *

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

        #Painter-Related
        self.Brush = False #painting on/off
        self.DrawingShapes = Shapes()
        self.shapeStorage = []
        self.IsPainting = False
        self.IsEraseing = False

        self.CurrentColour = Colour3(0,0,0)
        self.CurrentWidth = 10
        self.ShapeNum = 0
        self.IsMouseing = False

        self.MouseLoc = Point(0, 0)
        self.LastPos = Point(0, 0)

        self.IsPainting = False
        self.ShapeNum = 0

        #Selection-Tool
        self.selection = []

        self.refresh_completion_list()
        self.new_dialog = new_canvas_dialog(self)
        self.link_dialog = link_node_dialog(self)

    def initFormatbar(self, x, y, node):
        self.temporaryNode = node

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

        self.alignLeftAction = QAction(QIcon("align-left.png"), "AlignLeft", self)
        self.alignLeftAction.triggered.connect(node.alignLeft)
        self.alignLeftAction.triggered.connect(lambda: self.returnFocusToTextAfterToolbarClick(node))

        self.alignCenterAction = QAction(QIcon("align-center.png"), "AlignCenter", self)
        self.alignCenterAction.triggered.connect(node.alignCenter)
        self.alignCenterAction.triggered.connect(lambda: self.returnFocusToTextAfterToolbarClick(node))

        #self.boldAction2 = QPushButton()                #------ how to get icon into a button
        #self.boldAction2.setIcon(QIcon(QPixmap("bold.png")))
        #self.boldAction2.setIconSize(QPixmap("bold.png").rect().size())
        #self.boldAction2.clicked.connect(node.bold)

        self.enlargeButton = QPushButton("Link")
        self.enlargeButton.clicked.connect(lambda: self.link_dialog.show())
        if node.link is not None:
            self.enlargeButton.setText(str(node.link))

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
        self.formatbar.addAction(self.alignLeftAction)
        self.formatbar.addAction(self.alignCenterAction)
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

        self.makeSelection = QPushButton("Select  ()")
        self.makeSelection.clicked.connect(lambda: self.mode('Select'))
        self.makeSelection.clicked.connect(lambda: self.setButtonDown_releaseOthers(self.makeSelection))


        #---------------  spacer
        self.mainbar_spacer = QWidget()
        self.mainbar_spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.separateNode = QPushButton("Separate")
        self.separateNode.clicked.connect(lambda: self.mode('Regular'))
        self.separateNode.clicked.connect(lambda: self.setButtonDown_releaseOthers(self.separateNode))

        #---------------  spacer
        self.mainbar_spacer2 = QWidget()
        self.mainbar_spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        #---------------------  Save & Load

        self.newCanvas = QPushButton("New")
        self.newCanvas.clicked.connect(lambda: self.new_dialog.show())
        self.saveCanvas = QPushButton("Save")
        self.saveCanvas.clicked.connect(self.save_canvas)
        self.loadCanvas = QPushButton("Load")
        self.loadCanvas.clicked.connect(self.load_canvas)


        self.mainbar = self.addToolBar('Main')
        self.mainbar.addWidget(self.makeNode)
        self.mainbar.addSeparator()
        self.mainbar.addWidget(self.makeArrows)
        self.mainbar.addSeparator()
        self.mainbar.addWidget(self.makeSelection)
        self.mainbar.addSeparator()
        #spacer
        self.mainbar.addWidget(self.mainbar_spacer)
        #spacer

        self.mainbar.addWidget(self.separateNode)

        #spacer
        self.mainbar.addWidget(self.mainbar_spacer2)
        #spacer
        self.mainbar.addWidget(self.newCanvas)
        self.mainbar.addSeparator()
        self.mainbar.addWidget(self.saveCanvas)
        self.mainbar.addSeparator()
        self.mainbar.addWidget(self.loadCanvas)
        self.mainbar.show()
        #----------------------------------------------------------------------------------
        self.painterase = QPushButton("Paint/Erase")
        self.painterase.clicked.connect(lambda: self.mode('Paint'))
        self.painterase.clicked.connect(lambda: self.setButtonDown_releaseOthers(self.painterase))

        self.paintbar = QToolBar(self)
        self.addToolBar(Qt.LeftToolBarArea, self.paintbar)
        self.paintbar.addWidget(self.painterase)
        self.paintbar.show()

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

    #OVERRIDING FUNCTIONS
    def mousePressEvent(self, event): #allows deletion if dragging away using RIGHT BUTTON
        print('pres')
        if event.buttons() == Qt.RightButton and self.mode_handler in ['Regular']:
            for node in self.nodes:
                x1, x2, y1, y2 = self.coords(node)
                if x1 - 10 < event.pos().x() < x2 + 10 and y1 - 10 < event.pos().y() < y2 + 10 and node.hasFocus() and self.node_to_change is None:
                    for nod in self.nodes:
                        if node in nod.connected_to:
                            nod.connected_to.remove(node)
                    self.nodes.remove(node)
                    node.setParent(None)
                    node.close()
                    node.deleteLater()
                    del node
                    self.statusbar.showMessage('deleted node')
                    return
        if event.buttons() == Qt.RightButton and self.mode_handler in ['Regular', 'Arrows', 'Paint']: #add modes FROM MAINBAR here to cancel on right click
            self.mode('none')
            self.setButtonDown_releaseOthers(False)
        elif event.buttons() == Qt.RightButton:
            self.mode('none')
            print('deselected all')
            self.setButtonDown_releaseOthers(False) #Release the select button bug!
            for node in self.selection:
                node.got_deselected()
                node.selected = False
            self.selection.clear()

        #---------------PAINTER---------------
        if self.mode_handler in ['Paint']:
            self.IsPainting = True
            self.ShapeNum += 1
            self.LastPos = Point(0, 0)

    def mouseMoveEvent(self, event):
        if self.mode_handler in ['Regular', 'Select', 'none']:
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
                if self.node_to_move[0].selected == False:
                    if y1 + event.pos().y() - self.node_to_move[2] > self.UPPER_LIMIT:
                        self.node_to_move[0].setGeometry(x1 + event.pos().x() - self.node_to_move[1],
                                                         y1 + event.pos().y() - self.node_to_move[2], width, height)
                    else:
                        self.node_to_move[0].setGeometry(x1 + event.pos().x() - self.node_to_move[1], self.UPPER_LIMIT, width, height)
                else:        #-------------------MOVE SELECTED NODES!-------------------
                    for node in self.selection:
                        node.move(node.pos().x() + (event.x() - x1), node.pos().y() + (event.y() - y1))
                self.node_to_move = (self.node_to_move[0], event.pos().x(), event.pos().y())
                return
            elif event.buttons() == Qt.LeftButton and self.mode_handler not in 'none':
                if self.node_to_change is None:
                    if self.mode_handler in ['Regular']:
                        self.node_to_change = (
                            text_node(self), event.pos().x(), event.pos().y())
                        self.node_to_change[0].setGeometry(event.pos().x(),
                                                           event.pos().y(), 0, 0)
                    elif self.mode_handler in ['Select']:
                        self.node_to_change = (
                            select_node(self), event.pos().x(), event.pos().y())
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
        #-----------------PAINTER--------------------------
        if (self.IsPainting == True):
            self.MouseLoc = Point(event.x(), event.y())
            if ((self.LastPos.X != self.MouseLoc.X) and (self.LastPos.Y != self.MouseLoc.Y)):
                self.LastPos = Point(event.x(), event.y())
                self.DrawingShapes.NewShape(self.LastPos, self.CurrentWidth,
                                                       self.CurrentColour, self.ShapeNum)
            self.repaint()

    def mouseReleaseEvent(self, event):     #contains loops for printing NODES info
        if self.node_to_change is not None:
            if self.mode_handler in ['Select']:
                for node in self.nodes:
                    if node.parent == self.node_to_change[0].parent:
                        if node.selected == False:
                            if node.pos().x() > self.node_to_change[0].pos().x() and node.width() + node.pos().x() < self.node_to_change[0].width() + self.node_to_change[0].pos().x():
                                if node.pos().y() > self.node_to_change[0].pos().y() and node.height() + node.pos().y() < self.node_to_change[0].height() + self.node_to_change[0].pos().y():
                                    self.selection.append(node)
                                    node.selected = True
                                    node.got_selected()
                self.node_to_change[0].deleteLater()
                self.node_to_change = None
                print(self.selection)
            else:
                self.nodes.append(self.node_to_change[0])
                self.node_to_change[0].index = self.node_count
                self.node_to_change[0].handle.move(self.node_to_change[0].width() -20, self.node_to_change[0].height() -20)
                if self.mode_handler in ['Regular']:
                    for node in self.nodes:
                        print(node)
                        for nod in node.connected_to:
                            print(nod)
                self.node_to_change = None
                self.node_count += 1

        if self.node_to_move is not None:
            self.node_to_move = None
        #-----------------PAINTER--------------------------
        if (self.IsPainting == True):
            self.IsPainting = False
            print(self.DrawingShapes.GetShape(5))
            #self.shapeStorage.append(self.DrawingShapes.__Shapes)
            #self.DrawingShapes.__Shapes.clear()
        if (self.IsEraseing == True):
            self.IsEraseing = False

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
        #-----------------PAINTER--------------------------
        painter = QPainter()
        painter.begin(self)
        self.drawLines(event, painter)
        painter.end()

    #OTHER FUNCTIONS
    def coords(self, node):
        return node.x(), node.x() + node.width(), node.y(), node.y() + node.height()

    def mode(self, new_mode):  # sets current mode based off buttons  # , info
        self.mode_handler = new_mode
        self.removeToolBar(self.formatbar)
        self.toolbaropen = 0
        self.node_to_connect = None
        self.statusbar.showMessage(str(new_mode))

    def setButtonDown_releaseOthers(self, button):
        if button is False:
            self.pressedDownButton[0].setDown(False)
        else:
            self.pressedDownButton[0].setDown(False)
            self.pressedDownButton.clear()
            button.setDown(True)
            self.pressedDownButton.append(button)

    def returnFocusToTextAfterToolbarClick(self, node):
        self.removeToolBar(self.formatbar)
        self.initFormatbar(self.x() + node.x(), self.y() + node.y() - 5, node)

    def new_canvas(self, dialog): #creates new file
        print('clicked OK')
        if os.path.exists(dialog + '.db'):
            os.remove(dialog + '.db')
        conn = sqlite3.connect(dialog + '.db')
        conn.commit()
        conn.close()

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
            a = text_node(self)
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
        for node in self.nodes:
            node.setParent(None)
            node.deleteLater()
        print(str(self.nodes))
        self.nodes.clear()  #-------------------------CHECK for GARBAGE COLLECTION!
        del self.nodes
        self.nodes = []
        self.statusbar.showMessage('cleared everything')
        print('cleared everything')

    def refresh_completion_list(self):
        # finds all .db files and presents them without the suffix as autocompletion
        self.canvas_list = []
        for item in os.listdir(os.getcwd()):
            if str(item)[-3::] in ['.db']:
                self.canvas_list.append(str(item)[:-3])
        self.completer = QCompleter(self.canvas_list)

    #--------------PAINTER FUNCTIONS--------------------------

    def drawLines(self, event, painter):
        painter.setRenderHint(QPainter.Antialiasing);

        for i in range(self.DrawingShapes.NumberOfShapes() - 1):

            T = self.DrawingShapes.GetShape(i)
            T1 = self.DrawingShapes.GetShape(i + 1)

            if (T.ShapeNumber == T1.ShapeNumber):
                pen = QPen(QColor(T.Colour.R, T.Colour.G, T.Colour.B), T.Width / 2, Qt.SolidLine)
                painter.setPen(pen)
                painter.drawLine(T.Location.X, T.Location.Y, T1.Location.X, T1.Location.Y)

if __name__ == '__main__':
    counter = 0
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
