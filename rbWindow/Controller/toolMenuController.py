import os
import jsonConverter.searchModule as search
import groupingTool.tMatrix.PhaseTool
import groupingTool.tMatrix.groupTestController
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

margin = 20
width = 100

"""
2020/03/35 
modify by Kim Heesup Kim
"""


def getMatchGroupByMatrix(standardGlyph, contourIndex,checkSetData):
	"""
	UI와 그룹 방법을 연결시켜주는 함수 (Matrix 방법)
	Args :
		standardGlyph :: RGlyph 
			기준 컨투어
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
		checkSetData :: List
			스마트셋 이름을 관리하기 위하여 필요한 checkSetData
			smartSetSearchModule 파일을 이용하여 구함
			[setNumber, syllableNumber]
		jsonFileName1 :: String
			시계방향, 반시계방향 정보를 담고 있는 json파일 이름(1차 필터링 결과)
		jsonFileName2 :: String
			음절 분리가 되어 있는 json파일 이름을 반환
	Returns: Dict
		처음 그룹화 진행시 생성되는 groupDict을 반환

	2020/03/23
	스마트셋 이름 규칙을 정리함
	set name format example
		: ##(number)_##(syllable)_####(mode)
	"""
	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont
	mode = getExtensionDefault(DefaultKey+".mode")
	jsonFileName1 = getExtensionDefault(DefaultKey+".jsonFileName1")
	jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
	matrix_margin = getExtensionDefault(DefaultKey+".matrix_margin")
	matrix_size = getExtensionDefault(DefaultKey+".matrix_size")

	contour = standardGlyph.contours[contourIndex]

	standardMatrix = Matrix(contour,matrix_size)
	#k에 대한 마진값 적용하는 부분 넣어 주워야 함
	compareController = groupTestController(standardMatrix,matrix_margin)
	smartSetGlyphs = []
	smartSet = SmartSet()

	#추가부분
	with open(jsonFileName1, 'r') as jsonFile1:
	    resultDict = json.load(jsonFile1)

	with open(jsonFileName2, 'r') as jsonFile2:
		configDict = json.load(jsonFile2)

	print("checkSetData: ",checkSetData)
	print("~~~~")

	standard = resultDict[standardGlyph.name][contourIndex]
	bar = ProgressBar('Matrix Process',len(resultDict),'Grouping...')
	barProcess = 0

	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Matrix_" + "(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Matrix_" +"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Matrix_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"

	smartGroupDict = {}
	smartContourList = [] 


	for key, value in resultDict.items():
		barProcess += 1
		smartCheck = 0
		for i,compare in enumerate(value):
			if i not in configDict[key][checkSetData[1]]:#초, 중, 종 분리 로직
				continue
			if (standard['reverse'] == compare['reverse']) and (standard['forword'] == compare['forword']):
				compareContour = font[key].contours[i]
				result = compareController.conCheckGroup(compareContour)
				if result is not None:
					smartContourList.append(i)
					smartCheck = 1

		if smartCheck == 1:
			smartGroupDict[font[key]] = smartContourList
			smartSetGlyphs.append(font[key].name)
			smartContourList = []
		if barProcess % 10 == 0:
			bar.tick(barProcess)

	bar.close()


	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)
	updateAllSmartSets()

	return smartGroupDict	


"""
Legacy
"""
def getMatchGroupByTopology(standardGlyph, contourIndex, checkSetData):
	"""
	2020/03/25
	modify by Kim heesup
	To get group contours Based on standard Glyph's contour by topology
	Args :
		standardGlyph :: RGlyph 
			기준 컨투어
		contourIndex ::  int
			컨투어의 번호
		checkSetData :: List
			스마트셋 이름을 관리하기 위하여 필요한 checkSetData
			smartSetSearchModule 파일을 이용하여 구함
			[setNumber, syllableNumber]
		jsonFileName1 :: String
			시계방향, 반시계방향 정보를 담고 있는 json파일 이름(1차 필터링 결과)
		jsonFileName2 :: String
			음절 분리가 되어 있는 json파일 이름을 반환

	2020/03/23
	스마트셋 이름 규칙을 정리함
	set name format example
		: ##(number)_##(syllable)_####(mode)				
	"""
	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont
	mode = getExtensionDefault(DefaultKey+".mode")
	jsonFileName1 = getExtensionDefault(DefaultKey+".jsonFileName1")
	jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
	topology_margin = getExtensionDefault(DefaultKey+".topology_margin")

	#추가부분
	with open(jsonFileName1, 'r') as jsonFile1:
		resultDict = json.load(jsonFile1)

	with open(jsonFileName2, 'r') as jsonFile2:
		configDict = json.load(jsonFile2)

	standard = resultDict[standardGlyph.name][contourIndex]

	bar = ProgressBar('Topology Process',len(resultDict),'Grouping...')
	barProcess = 0

	smartSetGlyphs = []
	smartSet = SmartSet()
	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Topology_" +"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Topology_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Topology_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	smartGroupDict = {}
	smartContourList = [] 


	for key, value in resultDict.items():
		smartCheck = 0
		barProcess += 1
		for i,compare in enumerate(value):
			if i not in configDict[key][checkSetData[1]]:#초, 중, 종 분리 로직
				continue
			if (standard['reverse'] == compare['reverse']) and (standard['forword'] == compare['forword']):
				compareContour = font[key].contours[i]
				result = topologyJudgementController(standardGlyph.contours[contourIndex],compareContour,topology_margin).topologyJudgement()
				if result == True:
					smartContourList.append(i)
					smartCheck = 1

		if smartCheck == 1:
			smartGroupDict[font[key]] = smartContourList
			smartSetGlyphs.append(font[key].name)
			smartContourList = []
		if barProcess % 10 == 0:
			bar.tick(barProcess)
			
	bar.close()

	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)
	updateAllSmartSets()

	return smartGroupDict


def handleSearchGlyphList(standardGlyph, contourIndex, groupDict):
	"""
		2020/03/23
		created by H.W. Cho

		Get matching file and update currentWindow's group. If there is no matching file,
		search process will find a new group. Update view is followed at the end of process.

		Args::
			standardGlyph(RGlyph), contourIndex(int) : target object which want to search.
			currentWindow(toolMenu object)

		2020/03/25
		modifyed by Kim heesup
		add smart set information

	"""
	#파라미터 가져옴
	mode = getExtensionDefault(DefaultKey+".mode")

	checkSetData = searchGroup(standardGlyph,contourIndex,mode,True)

	if checkSetData[2] == 0:
		groupDict = findContoursGroup(checkSetData,mode)
		setExtensionDefault(DefaultKey + ".groupDict", groupDict)
		print(Message("이미 그룹화 진행이 되어 있으므로 그룹화 작업을 생략합니다."))

	else:
		if mode is matrixMode:
			#스마트 셋을 만들고 그 이후에 스마트 이름 명을 이용하여 gruopDict를 만듬
			groupDict = getMatchGroupByMatrix(standardGlyph, contourIndex,checkSetData)
			setExtensionDefault(DefaultKey + ".groupDict", groupDict)

		elif mode is topologyMode:
			groupDict = getMatchGroupByTopology(standardGlyph, contourIndex,checkSetData)
			setExtensionDefault(DefaultKey + ".groupDict", groupDict)

	#현재 스마트셋 포커싱
	smartSetIndex = sSF.getMatchingSmartSet(checkSetData, standardGlyph, contourIndex)
	
	sSF.updateSmartSetIndex(smartSetIndex)
	
def findContoursGroup(checkSetData, mode):
	"""
	json파일과 스마트 셋을 참고하여 이미 그룹화가 진행된 컨투어를 찾아냄
	Args :
		checkSetData :: List
			스마트셋 이름을 관리하기 위하여 필요한 checkSetData
			smartSetSearchModule 파일을 이용하여 구함
			[setNumber, syllableNumber,그룹화의 진행 여부]
		mainWindow :: object
			editWindow object
		mode :: int
		0 -> matrix , 1- > topology
	Returns :: Dictionary
		각각의 키는 같은 그룸의 컨투어를 포함하는 글리프, 값은 해당 컨투어의 번호를 저장 :: Dictionary
			key :: RGlyph
			value :: list
	"""
	matrix_margin = getExtensionDefault(DefaultKey+".matrix_margin")
	matrix_size = getExtensionDefault(DefaultKey+".matrix_size")
	topology_margin = getExtensionDefault(DefaultKey+".topology_margin")
	jsonFileName2 = getExtensionDefault(DefaultKey+".jsonFileName2")
	#파라미터를 받아오는 작업
	font = getExtensionDefault(DefaultKey+".font")#RFont

	#초성, 중성, 종성 분리된 딕셔너리 정보를 가져옴
	with open(jsonFileName2, 'r') as jsonFile2:
		configDict = json.load(jsonFile2)

	ssets = getSmartSets()
	glyphList = list()
	res = dict()
	positionName  = None
	groupSet = None

	if mode == 0:
		modeName = "Matrix"
	else:
		modeName = "Topology"

	if checkSetData[1] == 0:
		positionName = "first"
	elif checkSetData[1] == 1:
		positionName = "middle"
	else:
		positionName = "final"


	for sset in ssets:
		nameList = str(sset.name).split('_')
		#한자셋은 고려하지 않음
		if len(nameList) == 3:
			continue
		standardNameList = nameList[3].split('-')
		standardGlyphUnicode = int(standardNameList[0][1:])
		standardIdx = int(standardNameList[1][0:len(standardNameList[1])-1])
		if (nameList[0] == str(checkSetData[0])) and (nameList[1] == positionName) and (nameList[2] == modeName):
			groupSet = sset
			break


	for item in groupSet.glyphNames:
		glyphList.append(font[str(item)])

	for g in glyphList:
		searchContours = []
		for i,comc in enumerate(g.contours):
			if i not in configDict[g.name][checkSetData[1]]:#초, 중, 종 분리 로직
				continue
			if mode == 0:
				standardGlyph = font["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(comc)
				if result is not None:
					searchContours.append(i)
			elif mode == 1:
				standardGlyph = font["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],comc,topology_margin).topologyJudgement()
				if result is not False:
					searchContours.append(i)
		res[g] = searchContours

	return res