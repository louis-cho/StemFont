from mojo.UI import *
from rbWindow.ExtensionSetting.extensionValue import *
from parseSyllable.configSyllable import *
from groupingTool.tMatrix.PhaseTool import *
from groupingTool.tMatrix.groupTestController import *
from groupingTool.tTopology.topologyJudgement import *
from fontParts.world import CurrentGlyph
from rbWindow.Controller.smartSetSearchModule import *
import sys

from rbWindow.Controller import toolMenuController as tMC
from rbWindow.Controller import toolMenuControllerChinese as ctMC

from mojo.extensions import *


matrixMode = 0
topologyMode = 1

def updateAttributeComponent():
	"""
		2020/05/14 created by Cho H.W.

		사용자의 조작에 의해 찾아놓은 groupDict가 아닌 다른 요소에 대해 속성을 부여하는 과정에서
		필요한 인자들을(ex. matrix, groupDict, standardGlyph, ...) 갱신하기 위한 보조함수

		선택된 컨투어가 기존의 groupDict 내에 포함된 요소라면 갱신하지 않고 메소드가 종료됩니다.
	"""

	count = 0
	selectedContour = None
	currentGlyph = CurrentGlyph()
	prevGlyph = getExtensionDefault(DefaultKey+".standardGlyph")
	prevContour = getExtensionDefault(DefaultKey+".standardContour")
	prevGroupDict = getExtensionDefault(DefaultKey+".groupDict")
	matrix_size = getExtensionDefault(DefaultKey+".matrix_size")
	mode = getExtensionDefault(DefaultKey+".mode")
	font = getExtensionDefault(DefaultKey+".font")

	#현재 선택된 컨투어 알아내기
	for contour in currentGlyph:
		if len(contour.selection) > 0:
			count += 1
			selectedContour = contour

	#하나의 컨투어만을 선택했는지 필터링
	if count != 1:
		Message("하나의 컨투어를 선택해주십시오.")
		return False


	else: 

		# 현재 선택된 컨투어가 그룹딕셔너리에 있나 확인하기
		if selectedContour != prevContour:
			
			try:
				#print("prevGroupDict : ",prevGroupDict)
				if type(prevGroupDict) is not dict:
					#print("prevGroupDict is None")
					raise Exception
				contourList = prevGroupDict[currentGlyph] 
				
				for contourIdx in contourList:

					#현재 선택된 컨투어를 이전 그룹 딕셔너리에서 찾았다면 standard Contour, Glyph, contourNumber 갱신
					if selectedContour.index == contourIdx:
						res = True
						setExtensionDefault(DefaultKey+".standardContour", selectedContour)
						setExtensionDefault(DefaultKey+".standardGlyph", currentGlyph)
						setExtensionDefault(DefaultKey+".contourNumber", selectedContour.index)	

						#매트릭스 관련 설정값 갱신
						if mode is matrixMode:
							matrix = Matrix(selectedContour, matrix_size); 
							setExtensionDefault(DefaultKey+".matrix", matrix)



						#현재 스마트셋 포커싱
						checkSetData = searchGroup(currentGlyph, selectedContour.index, mode)
						index = getMatchingSmartSet(checkSetData, currentGlyph, selectedContour.index)
						
						updateSmartSetIndex(index)

						return True

				# 같은 글리프라도 컨투어가 같은 그룹딕셔너리가 아니라면 익셉션을 raise한다.
				raise Exception

			# 다른 스마트 셋에 있거나 아직 탐색이 완료되지 않은 경우 처리
			except Exception as e:
				#print("selectedContour is ",selectedContour)
				result = updateSmartSetChanged(selectedContour)
				
				if result is False:
					Message("해당되는 그룹 결과가 존재하지 않습니다. 탐색을 먼저 진행해주세요.")
					
				return result

		else:
			return True

def updateSmartSetChanged(selectedContour):
	#print("selectedContour = ",selectedContour)
	"""
		이전 standardContour와 현재 선택된 standardContour의 smartSet이 다른 경우,
		이미 찾아놓은 smartSet이 존재하는 경우에 한하여 속성 부여에 필요한 인자들을 갱신합니다.
		(updateAttributeComponent의 보조함수)

		갱신되는 인자 : (contourNumber, standardContour, standardGlyph, groupDict)

		@param : 
			selectedContour(RContour) : 현재 속성을 부여하려는 point의 parent (RContour)
		
		@return :
			True : 갱신된 컨투어에 해당되는 스마트 셋이 존재하는 경우
			False : 갱신된 컨투어에 해당되는 스마트 셋이 존재하지 않는 경우 
	"""
	matrix_margin = getExtensionDefault(DefaultKey + ".matrix_margin")
	topology_margin = getExtensionDefault(DefaultKey + ".topology_margin")
	matrix_size = getExtensionDefault(DefaultKey + ".matrix_size")
	#print(sys.path)
	KoreanCheck = getExtensionDefault(DefaultKey+".korean")

	contourNumber = selectedContour.index;
	glyph = selectedContour.getParent();
	mode = getExtensionDefault(DefaultKey + ".mode")
	font = getExtensionDefault(DefaultKey + ".font")
	if KoreanCheck == True:
		checkSetData = searchGroup(glyph, contourNumber, mode)
		smartSetIndex = getMatchingSmartSet(checkSetData, glyph, contourNumber)
	else:
		checkSetData = cSearchGroup(glyph, contourNumber, mode)
		smartSetIndex = cGetMatchingSmartSet(checkSetData, glyph, contourNumber)
	
	updateSmartSetIndex(smartSetIndex)

	if checkSetData[2] == 0:
		
		if mode is matrixMode:

			matrix = Matrix(selectedContour, matrix_size); 
			setExtensionDefault(DefaultKey+".matrix", matrix)
		
		#print("checkSetData : ",checkSetData," file : ",file," mode : ",mode)
		if KoreanCheck == True:
			groupDict = tMC.findContoursGroup(checkSetData,mode)
		else:
			groupDict = ctMC.cFindContoursGroup(checkSetData, mode)
		setExtensionDefault(DefaultKey+".groupDict", groupDict)
		setExtensionDefault(DefaultKey+".contourNumber", contourNumber)
		setExtensionDefault(DefaultKey+".standardContour", selectedContour)
		setExtensionDefault(DefaultKey+".standardGlyph", glyph)
		return True
	
	else:
		return False

def cGetMatchingSmartSet(checkSetData, glyph, contourNumber):
	"""
		현재 속성을 부여하려고 시도한 그룹 딕셔너리가 바뀌는 경우 교체하기 위한 메소드(한자 버전)

		Return :: int
			스마트 셋의 인덱스를 반환
	"""
	sSets = getSmartSets()
	mode = getExtensionDefault(DefaultKey + ".mode")
	matrix_margin = getExtensionDefault(DefaultKey + ".matrix_margin")
	topology_margin = getExtensionDefault(DefaultKey + ".topology_margin")
	matrix_size = getExtensionDefault(DefaultKey + ".matrix_size")
	font = getExtensionDefault(DefaultKey + ".font")

	if mode is matrixMode:
		searchMode = "Matrix"
	elif mode is topologyMode:
		searchMode = "Topology"
	else:
		return None


	index = -1
	for sSet in sSets:
		index += 1
		checkSetName = str(sSet.name)
		checkSetNameList = checkSetName.split('_')
		if len(checkSetNameList) != 3:
			continue

		standardNameList = checkSetNameList[2].split('-')
		standardGlyphUnicode = standardNameList[0][1:]
		standardIdx = int(standardNameList[1][0:len(standardNameList)-1])

		for item in sSet.glyphNames:
			if item != glyph.name:
				continue

			if mode == 0:
				standardGlyph = font[standardGlyphUnicode]

				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(glyph[contourNumber])


				if result is not None: 
					return index


			elif mode == 1:
				standardGlyph = font[standardGlyphUnicode]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],glyph[contourNumber],topology_margin).topologyJudgement()

				if result is not False: 
					return index

	return None


def getMatchingSmartSet(checkSetData, glyph, contourNumber):
	"""
		현재 속성을 부여하려고 시도한 그룹 딕셔너리가 바뀌는 경우 교체하기 위한 메소드(한글 버전)
	"""
	sSets = getSmartSets()
	check = 0
	mode = getExtensionDefault(DefaultKey + ".mode")
	glyphConfigure = getConfigure(glyph)
	positionNumber = None
	searchSmartSet = None
	matrix_margin = getExtensionDefault(DefaultKey + ".matrix_margin")
	topology_margin = getExtensionDefault(DefaultKey + ".topology_margin")
	matrix_size = getExtensionDefault(DefaultKey + ".matrix_size")
	font = getExtensionDefault(DefaultKey + ".font")
	
	if mode is matrixMode:
		searchMode = "Matrix"
	elif mode is topologyMode:
		searchMode = "Topology"
	else:
		return None


	for i in range(0,len(glyphConfigure[str(glyph.unicode)])):
		for j in range(0,len(glyphConfigure[str(glyph.unicode)][i])):
			if contourNumber == glyphConfigure[str(glyph.unicode)][i][j]:
				check = 1
				positionNumber = i
				break

		if check == 1:
			break

	syllable = ["first", "middle", "final"]
	positionName = syllable[positionNumber]
	check = 0
	
	index = -1
	for sSet in sSets:
		index += 1
		checkSetName = str(sSet.name)
		checkSetNameList = checkSetName.split('_')

		if checkSetNameList[1] != positionName or checkSetNameList[2] != searchMode:
			continue
		if len(checkSetNameList) == 3:
			continue

		standardNameList = checkSetNameList[3].split('-')
		standardGlyphUnicode = int(standardNameList[0][1:])
		standardIdx = int(standardNameList[1][0:len(standardNameList)-1]) 
		
		for item in sSet.glyphNames:
			if item != glyph.name:
				continue

			if mode == 0:
				standardGlyph = font["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(glyph[contourNumber])

				if result is not None: 
					return index
			elif mode == 1:
				standardGlyph = font["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],glyph[contourNumber],topology_margin).topologyJudgement()

				if result is not False: 
					return index

	return None

def updateSmartSetIndex(index):

	if index is not None:
		smartSetIndexList = list()
		smartSetIndexList.append(index+1)
		selectSmartSets(smartSetIndexList)


def smartSetRefresh():
	"""
	스마트 셋의 글리프를 삭제했을 시 갱신해주는 함수
	"""
	KoreanCheck = getExtensionDefault(DefaultKey+".korean")
	smartSets = getSmartSets()
	font = getExtensionDefault(DefaultKey + ".font")
	groupDict = getExtensionDefault(DefaultKey+".groupDict")

	for smartSet in smartSets:
		check = False	
		if KoreanCheck is True:
			tmp = smartSet.name.split('_')[3][1:-1]
			rawUnicode = tmp.split('-')[0]
			contourNum = tmp.split('-')[1]
			targetGlyph = font["uni"+str(hex(int(rawUnicode)))[2:].upper()]
			for g in groupDict:
				if targetGlyph.name == g.name:
					for groupContourNum in groupDict[targetGlyph]:
						if int(contourNum) == int(groupContourNum):
							check = True
		
		elif KoreanCheck is False:
			tmp = smartSet.name.split('_')[2][1:-1]
			rawCidCode = tmp.split('-')[0]
			contourNum = tmp.split('-')[1]

			print("tmp = ",tmp)
			print("rawUnicode = ", rawCidCode)
			print("contourNum = ", contourNum)

			targetGlyph = font[rawCidCode]
			print("targetGlyph = ",targetGlyph)
			
			for g in groupDict:
				if targetGlyph.name == g.name:
					for groupContourNum in groupDict[targetGlyph]:
						if int(contourNum) == int(groupContourNum):
							check = True

		if check == False:
			continue

		newSmartSet = SmartSet()
		refreshSmartSetGlyphs = list()

		print("smart glyphName: ",smartSet.glyphNames)

		for detectGlyph in smartSet.glyphNames:
			print(font[detectGlyph])
			if font[detectGlyph].selected is False:
				refreshSmartSetGlyphs.append(font[detectGlyph].name)

		print("groupDict: ", groupDict)

		if (len(refreshSmartSetGlyphs) != len(smartSet.glyphNames)) and (len(refreshSmartSetGlyphs) != 0):
			#print("조건문 안")
			#smartSet.glyphNames = refreshSmartSetGlyphs
			contourNumber = groupDict[font[refreshSmartSetGlyphs[0]]][0]
			if KoreanCheck is True:
				newSmartSet.name = smartSet.name.split('_')[0] + '_' + smartSet.name.split('_')[1] + '_' + smartSet.name.split('_')[2] + '_('+str(font[refreshSmartSetGlyphs[0]].unicode)+'-'+str(contourNumber)+')'
			elif KoreanCheck is False:
				newSmartSet.name = smartSet.name.split('_')[0] + '_' + smartSet.name.split('_')[1] + '_'  + '('+str(font[refreshSmartSetGlyphs[0]].name)+'-'+str(contourNumber)+')'
			newSmartSet.glyphNames = refreshSmartSetGlyphs
			removeSmartSet(smartSet.name)
			addSmartSet(newSmartSet)
			updateAllSmartSets()
		elif len(refreshSmartSetGlyphs) == 0:
			removeSmartSet(smartSet.name)
			updateAllSmartSets()








