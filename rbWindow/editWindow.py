from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine
from mojo.UI import MultiLineView, SelectGlyph, Message, setScriptingMenuNamingShortKeyForPath, createModifier, HelpWindow
import pathManager.pathSetting as extPath
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval, rect
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
from rbWindow.toolMenu import toolsWindow
from rbWindow.attributeWindow import attributeWindow
from rbWindow.settingWindow import settingWindow
from mojo.UI import CurrentFontWindow
from AppKit import *
from rbWindow.ExtensionSetting.extensionValue import *
from rbWindow.Controller import CircularQueue
from fontParts.world import CurrentFont
from attributeTool.strokeAttribute import *
from rbWindow.Controller.smartSetFocus import *



def getMatchGroupDic(inputText, groupDict):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- inputText(str)
			- groupDict(dict)
		Return:
			groupDict if inputText is in groupDict else None
			Can be used as check whether groupDict contians inputText or not.
	"""
	for key in groupDict.keys():
		if str(ord(inputText)) == str(key.unicode):
			return groupDict

	return None


def getContourListByDic(groupDic):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- groupDict(dict)
		Return:
			- contourList(list) which glyphs' contourList of groupDict.

	"""
	contourList = []

	for glyph in groupDic.keys():
		for idx in groupDic[glyph]:
			contourList.append(glyph.contours[idx])

	return contourList


def getGlyphListByDic(groupDic):
	"""
		2020/03/12
		created by H.W. Cho

		Param:
			- groupDict(dict)
		Return:
			- glyphList(list)
	"""
	glyphList = []

	for glyph in groupDic.keys():
		glpyhList.add[glyph]

	return glyphList


def getMatchGroupDicByGlyph(inputGlyph, groupDict):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- inputGlyph(RGlyph)
			- groupDict(dict)
		Return:
			if exists, groupDict(dict)
			else, None
	"""
	if inputGlyph in groupDict.keys():
		return groupDict
	
	return None

class EditGroupMenu(object):

	def __init__(self,groupDict,jsonFileName1,jsonFileName2):
		
		self.font = getExtensionDefault(DefaultKey + ".font")
		self.groupDict = groupDict
		
		self.defaultKey = "com.asaumierdemers.BroadNibBackground"
		self.markColor = 0.3, 0.4, 0.7, 0.7
		self.layerName = self.font.layerOrder[0]
		self.currentPen = None
		self.window = None		# 현재 띄워져 있는 ufo 윈도우

		self.w = list()
		for i in range(7):
			self.w.append(None)
		
		self.mode = None  		# 연산 방법(matrix, topology)

		self.jsonFileName1 = jsonFileName1
		self.jsonFileName2 = jsonFileName2
		self.createUI()

		self.testPath = getExtensionDefault(DefaultKey+".testPath")
		self.color = None
		self.step = None
		self.width = None
		self.height = None
		self.shape = None
		self.angle = None
		self.keyDict = None



	"""
		UI 컴포넌트 부착
	"""
	def createUI(self):
		self.window = CurrentFontWindow()
		if self.window is None:
			return

		toolbarItems = self.window.getToolbarItems()
		self.newToolbarItems = list()
		newItem1 = dict(itemIdentifier="Search", label="Search", imageNamed=NSImageNameRevealFreestandingTemplate, callback=self.popSearchWindow); self.newToolbarItems.append(newItem1);
		newItem2_1 = dict(itemIdentifier="Rewind", label="Rewind", imageNamed=NSImageNameRefreshFreestandingTemplate, callback=self.restoreAttribute); self.newToolbarItems.append(newItem2_1);
		newItem2_2 = dict(itemIdentifier="Undo", label="Undo", imageNamed=NSImageNameInvalidDataFreestandingTemplate, callback=self.rollbackAttribute); self.newToolbarItems.append(newItem2_2);
		newItem3 = dict(itemIdentifier="Save", label="Save", imageNamed=NSImageNameComputer, callback=None); self.newToolbarItems.append(newItem3);
		newItem4 = dict(itemIdentifier="Exit", label="Exit", imageNamed=NSImageNameStopProgressFreestandingTemplate, callback=self.windowCloseCallback); self.newToolbarItems.append(newItem4);
		newItem5 = dict(itemIdentifier="Settings", label="Settings", imageNamed=NSImageNameAdvanced, callback=self.popSettingWindow); self.newToolbarItems.append(newItem5);
		newItem6 = dict(itemIdentifier="Attribute", label="Attribute", imageNamed=NSImageNameFontPanel, callback=self.popAttributeWindow); self.newToolbarItems.append(newItem6);
		newItem7 = dict(itemIdentifier="Help", label="Help", imageNamed=NSImageNameInfo, callback=self.popManualWindow); self.newToolbarItems.append(newItem7);
		newItem8 = dict(itemIdentifier="Except", label="Except", imageNamed=NSImageNameTrashFull, callback=self.handleRemoveGlyph); self.newToolbarItems.append(newItem8);

		#기존 툴바에 새로운 툴바 아이템 추가
		for i in range(len(self.newToolbarItems)):
			toolbarItems.append(self.newToolbarItems[i])


		# 현재 폰트 창에 toolbarItems를 추가
		vanillaWindow = self.window.window()
		self.window.toolbar = vanillaWindow.addToolbar(toolbarIdentifier="myCustomToolbar", toolbarItems=toolbarItems, addStandardItems=False)

		addObserver(self, "drawBroadNibBackground", "drawBackground")

	def popManualWindow(self,sender):
		manual = extPath.resourcePath + "manual.html"
		HelpWindow(htmlPath=manual)

	def popSettingWindow(self, sender):
		if self.w[5] is not None and self.w[5].w is not None:
			self.w[5].w.close()
		self.w[5] = settingWindow(self)
		
	def popAttributeWindow(self, sender):

		# Window for Assign & Remove Attribute
		mode = getExtensionDefault(DefaultKey + ".mode")
		contourNumber = getExtensionDefault(DefaultKey + ".contourNumber")
		if mode is None or contourNumber is None:
			Message("먼저 속성을 부여할 그룹을 찾아야 합니다.")
			return
		if self.w[3] is not None and self.w[3].w is not None:
			self.w[3].w.close()
			print("self.w[3].w = ", self.w[3].w)
		self.w[3] = attributeWindow()


	def popSearchWindow(self, sender):

		# Window for Matrix & Topology Process
		if self.w[4] is not None and self.w[4].w is not None:
			self.w[4].w.close()
		self.w[4] = toolsWindow()
		print("created")
		
	def handleRemoveGlyph(self, sender):

		"""
			스마트 셋 없이 처리하는 경우
		"""
		smartSetRefresh()
		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		keyList = list(groupDict.keys())
		for glyph in keyList:
			if glyph.selected is True:
				del groupDict[glyph]

		

		setExtensionDefault(DefaultKey+".groupDict", groupDict)


	    

	def windowCloseCallback(self, sender):
	    
	    try:
	    	removeObserver(self, "drawBackground")
	    	super(BroadNibBackground, self).windowCloseCallback(sender)
	    except Exception as e:
	    	print(e)

	    currentToolbarItems = self.window.getToolbarItems()

	    for i in range(len(self.newToolbarItems)):
	    	currentToolbarItems.pop()

	    self.window.setToolbar()

	    for i in range(len(self.w)):
	    	if self.w[i] is not None:
	    		self.w[i].w.close()

	    del self

	def restoreAttribute(self, sender):

		restoreStack = getExtensionDefault(DefaultKey + ".restoreStack")

		
		if restoreStack is None or restoreStack.isEmpty() is True:
			restoreStack.print()
			Message("더 이상 되돌릴 수 없습니다.")
			return

		top = restoreStack.pop()
		if top is None:
			restoreStack.print()
			Message("더 이상 되돌릴 수 없습니다.")
			return

		for element in top:
			element[0].name = element[1]

		restoreStack.print()
		CurrentFont().update()
		CurrentFont().save(self.testPath)

	def rollbackAttribute(self, sender):

		restoreStack = getExtensionDefault(DefaultKey + ".restoreStack")
		
		if restoreStack is None or restoreStack.front == restoreStack.rear:
			restoreStack.print()
			Message("복원할 수 없습니다.")
			return

		target = restoreStack.rollback()
	
		if target is None:
			Message("복원할 수 없습니다.")
			return 

		for element in target:
			element[0].name = element[1]

		restoreStack.print()
		CurrentFont().update()
		CurrentFont().save(self.testPath)


	def drawBroadNibBackground(self, info):
		
		# 칠할 필요가 없다면 종료
		state = getExtensionDefault(DefaultKey+".state")
		if bool(state) is not True:
			return

		# paint current group's contour
		targetGlyph = info["glyph"].getLayer(self.layerName)
		# picks current contours which should be painted from current group
		contourList = []


		try :
			targetIdxList = getExtensionDefault(DefaultKey+".groupDict")[targetGlyph]
			setExtensionDefault(DefaultKey + ".contourNumber", targetIdxList[0])
			
			color = getExtensionDefault(DefaultKey+".color")
			r,g,b,a = color
			fill(r,g,b,a)

			step = getExtensionDefault(DefaultKey+".step"); width = getExtensionDefault(DefaultKey+".width"); height = getExtensionDefault(DefaultKey+".height");


			if info["glyph"].layerName == self.layerName or not self.currentPen:
				self.currentPen = BroadNibPen(None, step, width, height, 0, oval)

			for idx in targetIdxList:
				targetGlyph.contours[idx].draw(self.currentPen)


		except Exception as e:
			setExtensionDefault(DefaultKey + ".contourNumber", None)
			return

def removeSelectedGlyphFromSmartSet(smartSetIndex, groupDict):

	keyList = list(groupDict.keys())
	for glyph in keyList:
		if glyph.selected is True and glyph.name in getSmartSets()[smartSetIndex]:
			del groupDict[glyph]

	setExtensionDefault(DefaultKey+".groupDict", groupDict)
