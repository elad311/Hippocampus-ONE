from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Colour3:
    R = 0
    G = 0
    B = 0
    #CONSTRUCTOR
    def __init__(self):
        self.R = 0
        self.G = 0
        self.B = 0
    #CONSTRUCTOR - with the values to give it
    def __init__(self, nR, nG, nB):
        self.R = nR
        self.G = nG
        self.B = nB

class Point:
    #X Coordinate Value
    X = 0
    #Y Coordinate Value
    Y = 0
    #CONSTRUCTOR
    def __init__(self):
        self.X = 0
        self.Y = 0
    #CONSTRUCTOR - with the values to give it
    def __init__(self, nX, nY):
        self.X = nX
        self.Y = nY
    #So we can set both values at the same time
    def Set(self,nX, nY):
        self.X = nX
        self.Y = nY

class Shape:
    Location = Point(0,0)
    Width = 0.0
    Colour = Colour3(0,0,0)
    ShapeNumber = 0
    #CONSTRUCTOR - with the values to give it
    def __init__(self, L, W, C, S):
        self.Location = L
        self.Width = W
        self.Colour = C
        self.ShapeNumber = S

class Shapes:
    #Stores all the shapes
    __Shapes = []
    def __init__(self):
        self.__Shapes = []
    #Returns the number of shapes being stored.
    def NumberOfShapes(self):
        return len(self.__Shapes)
    #Add a shape to the database, recording its position,
    #width, colour and shape relation information
    def NewShape(self,L,W,C,S):
        Sh = Shape(L,W,C,S)
        self.__Shapes.append(Sh)
    #returns a shape of the requested data.
    def GetShape(self, Index):
        return self.__Shapes[Index]
    #Removes any point data within a certain threshold of a point.
    def RemoveShape(self, L, threshold):
        #do while so we can change the size of the list and it wont come back to bite me in the ass!!
        i = 0
        while True:
            if(i==len(self.__Shapes)):
                break
            #Finds if a point is within a certain distance of the point to remove.
            if((abs(L.X - self.__Shapes[i].Location.X) < threshold) and (abs(L.Y - self.__Shapes[i].Location.Y) < threshold)):
                #removes all data for that number
                del self.__Shapes[i]
                #goes through the rest of the data and adds an extra
                #1 to defined them as a seprate shape and shuffles on the effect.
                for n in range(len(self.__Shapes)-i):
                    self.__Shapes[n+i].ShapeNumber += 1
                #Go back a step so we dont miss a point.
                i -= 1
            i += 1

class CreateUI(): #NOT NEEDED! THIS IS ACTUALLY THE MAIN PROGRAM WINDOW!!!
    Brush = True
    DrawingShapes = Shapes()
    IsPainting = False
    IsEraseing = False

    CurrentColour = Colour3(0,0,0)
    CurrentWidth = 10
    ShapeNum = 0
    IsMouseing = False
    PaintPanel = 0

    def SwitchBrush(self):
        if (self.Brush == True):
            self.Brush = False
        else:
            self.Brush = True

    def ChangeColour(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.CurrentColour = Colour3(col.red(), col.green(), col.blue())

    def ChangeThickness(self, num):
        self.CurrentWidth = num

    def ClearSlate(self):
        self.DrawingShapes = Shapes()
        self.PaintPanel.repaint()



