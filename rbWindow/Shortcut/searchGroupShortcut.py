import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))

import rbWindow.Controller.toolMenuController as tMC
import rbWindow.Controller.toolMenuControllerChinese as ctMC

from fontParts.world import *
from mojo.UI import Message
from uitestcode import *
from rbWindow.ExtensionSetting.extensionValue import *

def searchGroupProcess():

	selectedDict = dict()

	#try:
	standardGlyph = CurrentGlyph()
	setExtensionDefault(DefaultKey+".standardGlyph", standardGlyph)
	for contour in standardGlyph.contours:
		for point in contour.selection:
			if point.selected is True:
				selectedDict[point.getParent().index] = True

	if len(selectedDict) != 1:
		print(Message("글자의 컨투어를 하나만 선택해주세요."))
		return

	contourIndex = list(selectedDict.keys())[0]
	jsonFilePath = getExtensionDefault(DefaultKey+".jsonFilePath")
	mode = getExtensionDefault(DefaultKey+".mode")
	jsonFileName1 = getExtensionDefault(DefaultKey+".jsonFileName1")
	jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
	groupDict = getExtensionDefault(DefaultKey+".groupDict")
	
	KoreanCheck = getExtensionDefault(DefaultKey+".korean")
	print("Short Cut KoreanCheck : ", KoreanCheck)
	
	if KoreanCheck == True:
		tMC.handleSearchGlyphList(standardGlyph, contourIndex, groupDict)
	else:
		ctMC.cHandleSearchGlyphList(standardGlyph, contourIndex, groupDict)

	for contour in standardGlyph.contours:
		contour.selected = False
try:
	CurrentFontWindow().toolbar['Search']
except:
	menuWindow.createUI()
	
searchGroupProcess()