import os
import jsonConverter.searchModule as search
import groupingTool.tMatrix.PhaseTool
import groupingTool.tMatrix.groupTestController
import queue
from groupingTool.Bitmap import rasterize as re
from groupingTool.tTopology import topologyJudgement as tj
from groupingTool.tTopology import topologyAssignment as ta
from groupingTool import parseUnicodeControll as puc
import jsonConverter.converter as convert
from rbWindow.Controller.smartSetSearchModule import *
from parseSyllable.configSyllable import *
from mojo.UI import *
from rbWindow.ExtensionSetting.extensionValue import *
from rbWindow.Controller import smartSetFocus as sSF
from mojo.extensions import *

matrixMode = 0
topologyMode = 1

"""
2020/03/35 
modify by Kim Heesup Kim
"""

def cGetMatchGroupByMatrix(standardGlyph, contourIndex, checkSetData):
	"""
	한자버전
	UI와 그룹 방법을 연결시켜주는 함수 (Matrix 방법)
	Args :
		standardGlyph :: RGlyph 
			기준 글리프
		contourIndex ::  int
			컨투어의 번호
		margin :: int
			matrix로 반별시 오차 범위 허용 값(0 ~ 100)
			숫자가 높을수록 허용 범위가 넓어짐
			(20정도가 적당)
		width :: int
			매트릭스의 가로 구획 수
		height :: int
			매트릭스의 세로 구획 수
		checkSetData :: int
			한자를 관리하기 위한 번호
		jsonFileName1 :: String
			시계방향, 반시계방향 정보를 담고 있는 json파일 이름(1차 필터링 결과)
		jsonFileName2 :: String
			음절 분리가 되어 있는 json파일 이름을 반환

	2020/03/23
	스마트셋 이름 규칙은 숫자 번호대로
	"""

	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont
	mode = getExtensionDefault(DefaultKey+".mode")
	jsonFileName1 = getExtensionDefault(DefaultKey+".jsonFileName1")
	jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
	matrix_margin = getExtensionDefault(DefaultKey+".matrix_margin")
	matrix_size = getExtensionDefault(DefaultKey+".matrix_size")
	raster_margin = getExtensionDefault(DefaultKey+".raster_margin")


	contour = standardGlyph.contours[contourIndex]

	standardMatrix = Matrix(contour,matrix_size)
	#k에 대한 마진값 적용하는 부분 넣어 주워야 함
	compareController = groupTestController(standardMatrix,matrix_margin)
	smartSetGlyphs = []
	smartSet = SmartSet()

	#추가부분
	with open(jsonFileName1, 'r') as jsonFile1:
	    resultDict = json.load(jsonFile1)


	standard = resultDict[standardGlyph.name][contourIndex]

	bar = ProgressBar('Matrix Process',len(resultDict),'Grouping...')
	barProcess = 0

	smartGroupDict = {}
	smartContourList = []

	smartSet.name = str(checkSetData[0])+"_Matrix_" + "(" + str(standardGlyph.name) + "-" + str(contourIndex) + ")"
	


	for key, value in resultDict.items():
		barProcess += 1
		smartCheck = 0
		for i,compare in enumerate(value):
			#비교 컨투어 설정
			compareContour = font[key].contours[i]
			#clockWise 1차 필터링
			if (standard['reverse'] == compare['reverse']) and (standard['forword'] == compare['forword']):
				#Matrix 2차 필터링
				result = compareController.conCheckGroup(compareContour)

				#rasterize 3차 필터링
				if result is not None:
					result2 = re.compareBitMap(standardGlyph[contourIndex], compareContour,raster_margin)
				else:
					continue

				if result2 is True:
					smartContourList.append(i)
					smartCheck = 1
				#if result is not None:
					#smartContourList.append(i)
					#smartCheck = 1
				#else:
					#continue

		if smartCheck == 1:
			glyphUniName = font[key].name
			smartGroupDict[glyphUniName] = smartContourList
			smartSetGlyphs.append(glyphUniName)
			smartContourList = []
		if barProcess % 10 == 0:
			bar.tick(barProcess)

	bar.close()


	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)
	updateAllSmartSets()	



def cGetMatchGroupByTopology(standardGlyph, contourIndex,checkSetData):
	"""
	2020/03/25
	modify by Kim heesup
	한자버전
	To get group contours Based on standard Glyph's contour by topology
	Args :
		standardGlyph :: RGlyph 
			기준 글리프
		contourIndex ::  int
			컨투어의 번호
		k : int
			topology의 margin값 설정
		checkSetData :: int
			한자를 관리하기 위한 번호
		jsonFileName1 :: String
			시계방향, 반시계방향 정보를 담고 있는 json파일 이름(1차 필터링 결과)
		jsonFileName2 :: String
			음절 분리가 되어 있는 json파일 이름을 반환

	2020/03/23
	스마트셋 이름 규칙은 숫자 번호대로				
	"""
	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont
	mode = getExtensionDefault(DefaultKey+".mode")
	jsonFileName1 = getExtensionDefault(DefaultKey+".jsonFileName1")
	jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
	topology_margin = getExtensionDefault(DefaultKey+".topology_margin")
	raster_margin = getExtensionDefault(DefaultKey+".raster_margin")

	#추가부분
	with open(jsonFileName1, 'r') as jsonFile1:
		resultDict = json.load(jsonFile1)


	standard = resultDict[standardGlyph.name][contourIndex]

	bar = ProgressBar('Topology Process',len(resultDict),'Grouping...')
	barProcess = 0

	smartSetGlyphs = []
	smartSet = SmartSet()

	smartSet.name = str(checkSetData[0]) + "_Topology_" + "(" + str(standardGlyph.name) + "-" + str(contourIndex) + ")"

	smartGroupDict = {}
	smartContourList = [] 


	for key, value in resultDict.items():
		smartCheck = 0
		barProcess += 1
		for i,compare in enumerate(value):
			#clockWise 1차 필터링
			if (standard['reverse'] == compare['reverse']) and (standard['forword'] == compare['forword']):
				#비교 컨투어 설정
				compareContour = font[key].contours[i]

				#Topology 2차 필터링
				result = topologyJudgementController(standardGlyph.contours[contourIndex],compareContour,topology_margin).topologyJudgement()

				#rasterize 3차 필터링
				if result == None:
					result2 = re.compareBitMap(standardGlyph[contourIndex], compareContour,raster_margin)
				else:
					continue

				if result2 is True:
					smartContourList.append(i)
					smartCheck = 1

		if smartCheck == 1:
			glyphUniName = font[key].name
			smartGroupDict[glyphUniName] = smartContourList
			smartSetGlyphs.append(glyphUniName)
			smartContourList = []
		if barProcess % 10 == 0:
			bar.tick(barProcess)
			
	bar.close()

	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)
	updateAllSmartSets()


def cHandleSearchGlyphList(standardGlyph, contourIndex, groupDict):
	"""
		2020/03/23
		created by H.W. Cho

		Get matching file and update currentWindow's group. If there is no matching file,
		search process will find a new group. Update view is followed at the end of process.

		Args::
			standardGlyph(RGlyph), contourIndex(int) : target object which want to search.
			file(RFont) : search area
			currentWindow(toolMenu object)

		2020/03/25
		modifyed by Kim heesup
		add smart set information

		실질적으로 UI와 컨트롤러를 이어주는 함수

	"""
	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont
	mode = getExtensionDefault(DefaultKey+".mode")


	checkSetData = cSearchGroup(standardGlyph,contourIndex,mode,True)

	if checkSetData[2] == 0:
		groupDict = cFindContoursGroup(checkSetData,mode)
		setExtensionDefault(DefaultKey + ".groupDict", groupDict)

	else:
		if mode is matrixMode:
			cGetMatchGroupByMatrix(standardGlyph, contourIndex,checkSetData)
			groupDict = cFindContoursGroup(checkSetData,mode)
			setExtensionDefault(DefaultKey + ".groupDict", groupDict)

		elif mode is topologyMode:
			cGetMatchGroupByTopology(standardGlyph, contourIndex, checkSetData)
			groupDict = cFindContoursGroup(checkSetData, mode)
			setExtensionDefault(DefaultKey + ".groupDict", groupDict)

	#현재 스마트셋 포커싱
	smartSetIndex = sSF.cGetMatchingSmartSet(checkSetData, standardGlyph, contourIndex)
	
	sSF.updateSmartSetIndex(smartSetIndex)
	
def cFindContoursGroup(checkSetData, mode):
	"""
	json파일과 스마트 셋을 참고하여 이미 그룹화가 진행된 컨투어를 찾아냄
	Args :
		checkSetData :: int
			한자를 관리하기 위한 번호
		mainWindow :: object
			editWindow object
		mode :: int
		0 -> matrix , 1- > topology
	Returns :: Dictionary
		각각의 키는 같은 그룸의 컨투어를 포함하는 글리프, 값은 해당 컨투어의 번호를 저장 :: Dictionary
			key :: RGlyph
			value :: list
	"""

	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont

	ssets = getSmartSets()
	glyphList = list()
	res = dict()
	positionName  = None
	groupSet = None

	if mode == 0:
		modeName = "Matrix"
	else:
		modeName = "Topology"

	for sset in ssets:
		nameInfo = sset.name.split('_')
		#print("nameInfo : ",nameInfo)
		if len(nameInfo) != 3:
			continue

		ChineseIndex = int(nameInfo[0])
		if checkSetData[0] == ChineseIndex:
			groupSet = sset
			break


	for item in groupSet.glyphNames:
		glyphList.append(font[str(item)])

	#기준 컨투어를 뽑아내는 작업
	checkSetName = str(groupSet.name)
	checkSetNameList = checkSetName.split('_')
	standardNameList = checkSetNameList[2].split('-')
	standardGlyphUnicode = int(standardNameList[0][4:])
	standardIdx = int(standardNameList[1][:len(standardNameList[1]) -1])
	matrix_margin = getExtensionDefault(DefaultKey+".matrix_margin")
	matrix_size = getExtensionDefault(DefaultKey+".matrix_size")
	topology_margin = getExtensionDefault(DefaultKey+".topology_margin")



	for g in glyphList:
		searchContours = []
		for i,comc in enumerate(g.contours):
			if mode == 0:
				standardGlyph = font["cid" + str(standardNameList[0][4:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(comc)
				if result is not None:
					searchContours.append(i)
			elif mode == 1:
				standardGlyph = font["cid" + str(standardNameList[0][4:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],comc,topology_margin).topologyJudgement()
				if result is not False:
					searchContours.append(i)
		res[g] = searchContours

	return res