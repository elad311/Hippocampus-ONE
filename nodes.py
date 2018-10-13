from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import sizegrip as sg

#add node template others can inherit from

class select_node(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.parent = parent
        #self.connected_to = []  #----------------------------------MUST!
        self.index = None
        self.setStyleSheet("border: 3px solid blue; border-radius: 10px; border-style: dashed")
        self.setWindowFlags(Qt.SubWindow)
        self.handle = sg.sizegrip(self)

    def focusInEvent(self, event):
        self.setStyleSheet("border: 6px solid cyan; border-radius: 10px; border-style: dashed")


class text_node(QTextEdit):
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.parent = parent
        self.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'""" + self.parent.fontBox.currentFont().family() + """'; font-size:""" + str(self.parent.fontSize.value()) + """pt;"><br /></p></body></html>""")
        self.index = None
        self.connected_to = []  #array for storing connections on EACH NODE

        #self.setFontFamily(self.parent.fontBox.currentFont().family())
        self.setFontPointSize(self.parent.fontSize.value())
        #self.parent.fontBox.currentFontChanged.connect(lambda font: self.setFontFamily(font.family()))
        #self.parent.fontBox.currentFontChanged.connect(self.text_change)
        self.parent.fontSize.valueChanged.connect(lambda size: self.setFontPointSize(size))
        self.parent.fontSize.valueChanged.connect(self.text_change)
        self.textChanged.connect(self.text_change)
        self.selectionChanged.connect(self.cursor_change)
        self.cursorPositionChanged.connect(self.cursor_change)

        self.set_html = False       #currently not in use
        #self.setReadOnly()          #Saved for REVIEW MODE

        self.setting_da_style()

        #SizeGrip
        self.setWindowFlags(Qt.SubWindow)  #important for controlling only the node in sizegrip!
        self.handle = sg.sizegrip(self)

        self.setContextMenuPolicy(Qt.NoContextMenu)   #PREVENTS CONTEXT MENU

        #Selection
        self.selected = False
        self.setAcceptDrops(True)

        self.link = None

    #STYLING
    def setting_da_style(self):
        # STYLING - For setting control
        self.borderWidth = "2"
        self.borderColor = "black"
        self.borderRadius = "8"
        self.setObjectName('info_node')
        # BACKGROUND FILLING
        self.backgroundColor = "rgba(0, 0, 0, 0)"
        # contains specific styling for bottom right! should be changeable to bottom-left!
        self.style_changed()
        # another way:
        # self.viewport().setAutoFillBackground(False)

    def style_changed(self):
        self.styling = "QTextEdit#info_node {background-color: " + self.backgroundColor + " ;border: " + self.borderWidth + "px solid " + self.borderColor + "; border-radius: " + self.borderRadius + "px; border-bottom-right-radius: 30px; border-style: outset; padding: 1px}"
        self.setStyleSheet(self.styling)

    #EVENT OVERRIDE
    def dropEvent(self, event):  #Need to add paste event, not just drop
        cleanDragInfo = event.mimeData().text()
        QTextEdit.dropEvent(self, event)
        cursor = self.textCursor()
        filename = event.mimeData().text()[8::]
        if cleanDragInfo[-3::] in ['png', 'jpg', 'bmp']:
            #print(self.toPlainText().find(dragContents))
            #print(cursor.position())
            cursor.movePosition(QTextCursor.PreviousCharacter, QTextCursor.KeepAnchor, len(cleanDragInfo))
            image = QImage(filename)
            cursor.insertImage(image, filename)
        else:
            print('dropped text')
            #self.cursorForPosition(self.mapFromGlobal((QCursor.pos()))) #get mouse pos on widget viewport

    def mousePressEvent(self, event):
        if event.buttons() == Qt.RightButton and self.selected == False:
            self.selected = True
            self.got_selected()
            self.parent.selection.append(self)
        if self.parent.toolbaropen == 0:
            self.parent.initFormatbar(self.parent.x() + self.x(), self.parent.y() + self.y() - 5, self) #set coords for toolbar
            self.parent.toolbaropen = 1
            self.parent.nodeUnderEdit.append(self)
            self.parent.statusbar.showMessage('Node ' + str(self.index))
        if event.buttons() == Qt.LeftButton and self.parent.mode_handler == 'Arrows':
            if not self.parent.node_to_connect:  # saves node that will be connected
                self.parent.node_to_connect = self
            elif self not in self.parent.node_to_connect.connected_to and self.parent.node_to_connect not in self.connected_to:  # if such a node already exists, and the node that should be connected to it isn't already connected, connect
                self.parent.node_to_connect.connected_to.append(self)
                self.parent.node_to_connect = None
                self.parent.at_least_one_connection = True  # at least one connection was made, so the painter should paint the connections

            else:
                self.parent.node_to_connect = None
        else:
            QTextEdit.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event): #Check for DOUBLECLICK and EMPTY CONTENTS
        QTextEdit.mouseDoubleClickEvent(self, event) #allows text selection while listening to double-click
        if self.toPlainText() == "":
            self.switch_node()

    #ALL FUNCTIONS
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
        print('y[p')
        self.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignJustify)

    def switch_node(self):
        #CREATE NEW NODE part
        x1, x2, y1, y2 = self.parent.coords(self)
        newnode = anki_node(self.parent)
        newnode.setGeometry(x1, y1, x2 - x1, y2 - y1)
        newnode.show()
        newnode.handle.move(newnode.width() - 20, newnode.height() - 20)  # move handle ON LOAD
        self.parent.nodes.append(newnode)
        self.parent.returnFocusToTextAfterToolbarClick(newnode)        #------- REFRESH TOOLBAR FOR NEW NODE
        #DELETION part
        self.parent.nodes.remove(self)
        self.setParent(None)
        self.deleteLater()
        print(self.parent.nodes)
        print(newnode.x())

    def got_selected(self):
        self.setStyleSheet("background-color: "+self.backgroundColor+" ;border: 3px solid black; border-radius: 10px; border-style: dashed; padding: 1px")

    def got_deselected(self):
        self.style_changed()

    def got_linked(self, filename):
        print('linked')
        self.link = str(filename)
        self.backgroundColor = "rgba(0, 255, 0, 50)"
        self.style_changed()

    def got_delinked(self):
        print('delinked')
        self.link = None
        self.backgroundColor = "rgba(0, 0, 0, 0)"
        self.style_changed()

class anki_node(QTextEdit):
    def __init__(self, parent=None):
        QTextEdit.__init__(self, parent)
        self.parent = parent
        #self.setFontFamily(self.parent.fontBox.currentFont().family())
        self.setFontPointSize(self.parent.fontSize.value())
        self.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'""" + self.parent.fontBox.currentFont().family() + """'; font-size:""" + str(self.parent.fontSize.value()) + """pt;"><br /></p></body></html>""")
        #self.parent.fontBox.currentFontChanged.connect(lambda font: self.setFontFamily(font.family()))
        #self.parent.fontBox.currentFontChanged.connect(self.text_change)
        self.parent.fontSize.valueChanged.connect(lambda size: self.setFontPointSize(size))
        self.parent.fontSize.valueChanged.connect(self.text_change)
        self.index = None
        self.connected_to = []  #array for storing connections on EACH NODE
        self.textChanged.connect(self.text_change)
        self.selectionChanged.connect(self.cursor_change)
        self.cursorPositionChanged.connect(self.cursor_change)
        # currently not in use
        self.set_html = False
        self.setStyleSheet("border: 3px solid blue; border-radius: 10px; border-style: outset; padding: 1px")
        self.setWindowFlags(Qt.SubWindow)  #important for controlling only the node!
        self.handle = sg.sizegrip(self)

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
        if self.parent.toolbaropen == 0:
            self.parent.initFormatbar(self.parent.x() + self.x(), self.parent.y() + self.y() - 5, self) #set coords for toolbar
            self.parent.toolbaropen = 1
            self.parent.nodeUnderEdit.append(self)
            self.parent.statusbar.showMessage('Node ' + str(self.index))
        if event.buttons() == Qt.LeftButton and self.parent.mode_handler == 'Arrows':
            if not self.parent.node_to_connect:  # saves node that will be connected
                self.parent.node_to_connect = self
            elif self not in self.parent.node_to_connect.connected_to and self.parent.node_to_connect not in self.connected_to:  # if such a node already exists, and the node that should be connected to it isn't already connected, connect
                self.parent.node_to_connect.connected_to.append(self)
                self.parent.node_to_connect = None
                self.parent.at_least_one_connection = True  # at least one connection was made, so the painter should paint the connections

            else:
                self.parent.node_to_connect = None
        else:
            QTextEdit.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event): #Check for DOUBLECLICK and EMPTY CONTENTS
        QTextEdit.mouseDoubleClickEvent(self, event) #allows text selection while listening to double-click
        if self.toPlainText() == "":
            self.switch_node()


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

    def switch_node(self):
        #CREATE NEW NODE part
        x1, x2, y1, y2 = self.parent.coords(self)
        newnode = linked_node(self.parent)
        newnode.setGeometry(x1, y1, x2 - x1, y2 - y1)
        newnode.show()
        newnode.handle.move(newnode.width() - 20, newnode.height() - 20)  # move handle ON LOAD
        self.parent.nodes.append(newnode)
        self.parent.returnFocusToTextAfterToolbarClick(newnode)        #------- REFRESH TOOLBAR FOR NEW NODE
        #DELETION part
        self.parent.nodes.remove(self)
        self.setParent(None)
        self.deleteLater()
        print(self.parent.nodes)
        print(newnode.x())

class linked_node(QTextEdit):
    def __init__(self, parent=None):

        QTextEdit.__init__(self, parent)
        self.parent = parent
        #self.setFontFamily(self.parent.fontBox.currentFont().family())
        self.setFontPointSize(self.parent.fontSize.value())
        self.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p align="center" ; style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'""" + self.parent.fontBox.currentFont().family() + """'; font-size:""" + str(self.parent.fontSize.value()) + """pt;"><br /></p></body></html>""")
        #self.parent.fontBox.currentFontChanged.connect(lambda font: self.setFontFamily(font.family()))
        #self.parent.fontBox.currentFontChanged.connect(self.text_change)
        self.parent.fontSize.valueChanged.connect(lambda size: self.setFontPointSize(size))
        self.parent.fontSize.valueChanged.connect(self.text_change)
        self.index = None
        self.connected_to = []  #array for storing connections on EACH NODE
        self.textChanged.connect(self.text_change)
        self.selectionChanged.connect(self.cursor_change)
        self.cursorPositionChanged.connect(self.cursor_change)
        # currently not in use
        self.set_html = False
        self.setStyleSheet("border: 3px solid red; border-radius: 10px; border-style: outset; padding: 1px")
        self.setWindowFlags(Qt.SubWindow)  #important for controlling only the node!
        self.handle = sg.sizegrip(self)

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
        if self.parent.toolbaropen == 0:
            self.parent.initFormatbar(self.parent.x() + self.x(), self.parent.y() + self.y() - 5, self) #set coords for toolbar
            self.parent.toolbaropen = 1
            self.parent.nodeUnderEdit.append(self)
            self.parent.statusbar.showMessage('Node ' + str(self.index))
        if event.buttons() == Qt.LeftButton and self.parent.mode_handler == 'Arrows':
            if not self.parent.node_to_connect:  # saves node that will be connected
                self.parent.node_to_connect = self
            elif self not in self.parent.node_to_connect.connected_to and self.parent.node_to_connect not in self.connected_to:  # if such a node already exists, and the node that should be connected to it isn't already connected, connect
                self.parent.node_to_connect.connected_to.append(self)
                self.parent.node_to_connect = None
                self.parent.at_least_one_connection = True  # at least one connection was made, so the painter should paint the connections

            else:
                self.parent.node_to_connect = None
        else:
            QTextEdit.mousePressEvent(self, event)

    def mouseDoubleClickEvent(self, event): #Check for DOUBLECLICK and EMPTY CONTENTS
        QTextEdit.mouseDoubleClickEvent(self, event) #allows text selection while listening to double-click
        if self.toPlainText() == "":
            self.switch_node()


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
            self.setHtml("""<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd"><html><head><meta name="qrichtext" content="1" /><style type="text/css">p, li { white-space: pre-wrap; }</style></head><body style=" font-family:'MS Shell Dlg 2'; font-size:8.25pt; font-weight:400; font-style:normal;"><p align="center" ; style="-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:'""" + self.parent.fontBox.currentFont().family() + """'; font-size:""" + str(self.parent.fontSize.value()) + """pt;"><br /></p></body></html>""")
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
        self.setAlignment(Qt.AlignLeft)

    def alignRight(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignRight)

    def alignCenter(self):
        print('ypo')
        self.setAlignment(Qt.AlignCenter)

    def alignJustify(self):
        if self.hasFocus():
            self.setAlignment(Qt.AlignJustify)

    def switch_node(self):
        #CREATE NEW NODE part
        x1, x2, y1, y2 = self.parent.coords(self)
        newnode = text_node(self.parent)
        newnode.setGeometry(x1, y1, x2 - x1, y2 - y1)
        newnode.show()
        newnode.handle.move(newnode.width() - 20, newnode.height() - 20)  # move handle ON LOAD
        self.parent.nodes.append(newnode)
        self.parent.returnFocusToTextAfterToolbarClick(newnode)        #------- REFRESH TOOLBAR FOR NEW NODE
        #DELETION part
        self.parent.nodes.remove(self)
        self.setParent(None)
        self.deleteLater()
        print(self.parent.nodes)
        print(newnode.x())

