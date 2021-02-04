from mojo.UI import MultiLineView, SelectGlyph, Message
from AppKit import *
from vanilla import *
from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
import rbWindow.Controller.settingWindowController as sWC
from AppKit import NSCircularSlider, NSColor, NSRegularControlSize
from defconAppKit.windows.baseWindow import BaseWindowController
from fontTools.pens.basePen import BasePen
from mojo.extensions import getExtensionDefault, setExtensionDefault, getExtensionDefaultColor, setExtensionDefaultColor
from mojo.events import addObserver, removeObserver
from mojo.UI import UpdateCurrentGlyphView
from mojo.drawingTools import *
from vanilla import *
from rbWindow.sliderGroup import *
from rbWindow.ExtensionSetting.extensionValue import *

COLOR_GREEN = (0,1,0,0.7)
BroadNibBackgroundDefaultKey = "com.asaumierdemers.BroadNibBackground"

class settingWindow(BaseWindowController):

    def __init__(self, mainWindow):
        self.createUI(self)
        self.mainWindow = mainWindow

    def createUI(self, sender):

        x = 10; y = 10; w = -10; h = 40; space = 5; size = (100, 300); pos = (800,400)
        self.w = HUDFloatingWindow((250,600), "Background Setting")
        stepValue = getExtensionDefault(DefaultKey + ".step")
        self.w.step = SliderGroup((x, y, w, h), "Steps:", 0, 60, stepValue, callback=self.stepChanged)
        y+=h
        
        widthValue = getExtensionDefault("%s.%s" %(DefaultKey, ".width"), 50)
        self.w.width = SliderGroup((x, y, w, h), "Width:", 0, 300, widthValue, callback=self.widthChanged)
        y+=h
        
        heightValue = getExtensionDefault("%s.%s" %(DefaultKey, ".height"), 10)
        self.w.height = SliderGroup((x, y, w, h), "Height:", 0, 300, heightValue, callback=self.heightChanged)
        y+=h

        color = NSColor.colorWithCalibratedRed_green_blue_alpha_(1, 0, 0, .5)
        colorValue = getExtensionDefaultColor("%s.%s" %(DefaultKey, ".color"), color)
        self.w.colortext = TextBox((x, y, -0, 20), "Color:")
        self.w.color = ColorWell((70, y-5, w, 30), callback=self.colorChanged, color=colorValue)
        y+=h + 20

        ############### 탐색 파라미터 설정 #############
        self.w.searchOptionTextBox = TextBox((x,y,w,h), "Search Options")
        y += h + space
        
        rasterMargin = getExtensionDefault(DefaultKey + ".raster_margin")
        self.w.rasterMargin = SliderGroup((x, y, w, h), "Bitmap Margin:", 0, 200, rasterMargin, callback=self.rasterMarginChanged)
        y+=h
        
        matrixSize = getExtensionDefault(DefaultKey + ".matrix_size")
        self.w.matrixSize = SliderGroup((x, y, w, h), "Matrix Size:", 1, 50, matrixSize, callback=self.matrixSizeChanged)
        y+=h
        
        matrixMargin = getExtensionDefault(DefaultKey + ".matrix_margin")
        self.w.matrixMargin = SliderGroup((x, y, w, h), "Matrix Margin:", 0, 100, matrixMargin, callback=self.matrixMarginChanged)
        y+=h

        ###########################################
        y += 30
        self.w.colorContourCheckBox= CheckBox((x,y,w,h), "Apply Contour Color", callback=self.colorContourCallback, value=getExtensionDefault(DefaultKey + ".state"))
        y += h + 20

        self.w.methodRadioGroup = RadioGroup((x,y,w,h), ["Matrix", "Topology"], sizeStyle="small", callback=self.methodChangedCallback)
        y += h + space

        self.w.bind("close", self.close)
        self.w.open()

    def close(self, sender):
        self.w = None
        
    def colorChanged(self, sender):
        color = self.getColor()
        setExtensionDefault(DefaultKey+".color",color)
        self.updateView()

    def stepChanged(self, sender):
        setExtensionDefault(DefaultKey + ".step", int(sender.get()))
        self.updateView()

    def widthChanged(self, sender):
        setExtensionDefault(DefaultKey + ".width", int(sender.get()))
        self.updateView()

    def heightChanged(self, sender):
        setExtensionDefault(DefaultKey + ".height", int(sender.get()))
        self.updateView()

    def rasterMarginChanged(self, sender):
        setExtensionDefault(DefaultKey+".raster_margin", int(sender.get()))
        self.updateView()

    def matrixSizeChanged(self, sender):
        setExtensionDefault(DefaultKey+".matrix_size", int(sender.get()))
        self.updateView()

    def matrixMarginChanged(self, sender):
        setExtensionDefault(DefaultKey+".matrix_margin", int(sender.get()))
        print("margin = ",int(sender.get()))
        self.updateView()
        

    def getColor(self):
        color = self.w.color.get()
        return color.getRed_green_blue_alpha_(None, None, None, None)

    def checkGlyphListCallback(self, sender):
        pass
        """
        print("before : ", self.mainWindow.selectedGlyphs)
        sWC.helpCheckGlyphList(self.w.checkGlyphListCheckBox, self.mainWindow)
        print("after : ", self.mainWindow.selectedGlyphs)"""
    def colorContourCallback(self, sender):
        state = self.w.colorContourCheckBox.get()
        setExtensionDefault(DefaultKey+".state", state)

    def methodChangedCallback(self, sender):
        # select matrix or topology
        setExtensionDefault(DefaultKey+".mode", self.w.methodRadioGroup.get())

    def updateView(self, sender=None):
        UpdateCurrentGlyphView()
