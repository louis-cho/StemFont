from defconAppKit.windows.baseWindow import BaseWindowController
from rbWindow.contourPen import BroadNibPen
from mojo.events import addObserver
from mojo.drawingTools import fill, oval
from parseSyllable.configSyllable import *

COLOR_RED = 1,0,0,1
COLOR_GREEN = 0,1,0,1
COLOR_BLUE = 0,0,1,1

class syllableColor(BaseWindowController):
    """
    2020/03/06

    Get data through getConfigure() and paint current glyph's first, middle, last syllable
    """
    def __init__(self, font):
        self.font = font
        self.currentPen = None
        self.defaultKey = "com.asaumierdemers.BroadNibBackground"
        self.layerName = self.font.layerOrder[0]
        addObserver(self, "drawBroadNibBackground", "drawBackground")
        
    def drawBroadNibBackground(self, info):
       
        if info["glyph"].layerName == self.layerName or not self.currentPen:
            self.currentPen = BroadNibPen(None, 60, 80, 50, 30, oval)
        
        data = getConfigure(info["glyph"])
        print("data : ",data)
     
        for idx, contour in enumerate(info["glyph"]):

            if idx in data[str(info["glyph"].unicode)][0]:
                fill(1,0,0,1)
                contour.draw(self.currentPen)

            elif idx in data[str(info["glyph"].unicode)][1]:
                fill(0,0,1,1)
                contour.draw(self.currentPen)

            elif idx in data[str(info["glyph"].unicode)][2]:
                fill(0,1,0,1)
                contour.draw(self.currentPen)