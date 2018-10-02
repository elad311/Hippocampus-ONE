from PyQt5.QtWidgets import QSizeGrip


#CUSTOM CLASS NEEDED HERE BECAUSE OF MIS-ALIGNMENT NEEDING A FIX
class sizegrip(QSizeGrip):  #attach to any widget to allow RESIZE BY DRAGGING

    def __init__(self, parent=None):
        QSizeGrip.__init__(self, parent)
        self.parent = parent
        self.setStyleSheet("font-size: 0px; line-height: 0%; width: 0px; border-top: 20px solid white; border-right: 20px solid #cccccc;")

    def mouseMoveEvent(self, QMouseEvent):
        QSizeGrip.mouseMoveEvent(self, QMouseEvent) #ACTIVATE THE PROTECTED FUNCTION, then ADD FURTHER CODE
        # width and height represent absolute x,y values!
        self.move(self.parent.width() - 20, self.parent.height() - 20)