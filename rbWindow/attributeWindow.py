import pathManager.pathSetting as extPath
from vanilla import FloatingWindow, RadioGroup, Button, HUDFloatingWindow, ImageButton, TextBox, EditText, CheckBox
from groupingTool.tTopology import topologyButtonEvent as tbt
from groupingTool.tMatrix import matrixButtonEvent as mbt
from groupingTool.tMatrix.PhaseTool import *
from mojo.UI import *
from rbWindow.Controller import smartSetSearchModule 
from rbWindow.Controller.toolMenuController import *
from rbWindow.Controller.smartSetFocus import *
from rbWindow.ExtensionSetting.extensionValue import *
from fontParts.world import *
from fontParts.fontshell.contour import *

matrixMode = 0
topologyMode = 1
optionList = ["penPair", "stroke", "innerType", "dependX", "dependY"]

class subAttributeWindow:

	def __init__(self, attributeWindow):
		self.attributeWindow = attributeWindow
		self.createUI()

	def createUI(self):
		x=10;y=10;w=80;h=30;space=5;self.size=(150,300);pos=(1200,300);
		self.w = HUDFloatingWindow((pos[0],pos[1], self.size[0],self.size[1]), "DeleteWindow")
		self.w.deleteRadio = RadioGroup((x, y, w, 190),["penPair", "stroke", "innerFill", "dependX", "dependY"],callback=self.radioGroupCallback)
		y += space + h + 190
		self.w.applyButton = Button((x,y,w,35), "Apply", callback=self.buttonCallback)
		self.deleteOption = None
		self.w.open()


	def radioGroupCallback(self, sender):
		self.deleteOption = optionList[int(sender.get())]

	def buttonCallback(self, sender):
		if self.deleteOption is None:
			return

		if self.attributeWindow.updateAttributeComponent() is False:
			return

		mode = getExtensionDefault(DefaultKey+".mode")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")

		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			print("matrix = ", matrix)
			attribute = self.deleteOption
			print("optionList = ",optionList)
			print("self.option = ", self.deleteOption)
			mbt.mdeleteAttribute(groupDict, matrix, attribute)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			pass
				
		else:
			Message("모드 에러")

		self.w.close()


class attributeWindow:

	def __init__(self):
		
		self.createUI()
		self.testPath = getExtensionDefault(DefaultKey+".testPath")
	
	def createUI(self):
		x = 10; y = 10; w = 100; h = 30; space = 5; self.size = (200,450); pos = (1200,300); self.minSize = (50,400);

		self.w = HUDFloatingWindow((pos[0],pos[1],self.size[0],self.size[1]), "ToolsWindow", minSize=(self.minSize[0], self.minSize[1]))
		
		h = 30

		self.w.innerFillButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[0]+".png", callback=self.handleInnerFill)
		self.w.innerFillText = TextBox((x+40,y,w,h), "innerFill")
		y += h + space

		self.w.penPairButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[1]+".png", callback=self.handlePenPair)
		self.w.PenPairText = TextBox((x+40,y,w,h), "penPair")
		y += h + space

		self.w.dependXButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[2]+".png", callback=self.handleDependX)
		self.w.dependXText = TextBox((x+40,y,w,h), "dependX")
		y += h + space

		self.w.dependYButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[3]+".png", callback=self.handleDependY)
		self.w.dependYText = TextBox((x+40,y,w,h), "dependY")
		y += h + space

		self.w.stokeButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[4]+".png", callback=self.handleStroke)
		self.w.strokeText = TextBox((x+40,y,w,h), "stroke")
		y += h + space

		self.w.deleteButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[5]+".png", callback=self.popDelete)
		self.w.deleteText = TextBox((x+40,y,w,h), "delete")
		y += h + space

		self.w.selectButton = ImageButton((x,y,h,h), imagePath=extPath.ImagePath+extPath.attrImgList[6]+".png", callback=self.handleSelect)
		self.w.selectText = TextBox((x+40,y,w,h), "select")
		y += h + space

		self.w.minimizeBox = CheckBox((x,y,80,20), "", callback=self.minimizeCallback, value=False)
		y += h +space

		mode = getExtensionDefault(DefaultKey+".mode")

		self.w.bind("close", self.close)
		self.w.open()

	def close(self, sender):
		self.w = None

	def radioGroupCallback(self,sender):

		self.option = int(sender.get())

	def updateAttributeComponent(self):
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
		mode = getExtensionDefault(DefaultKey+".mode")
		font = getExtensionDefault(DefaultKey+".font")
		matrix = getExtensionDefault(DefaultKey+".matrix")

		print("시작됨")

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
			print("selectedContour = ",selectedContour)
			print("prevContour = ", prevContour)

			# 현재 선택된 컨투어가 그룹딕셔너리에 있나 확인하기
			if selectedContour != prevContour or matrix is None:
				print("이전 컨투어와 현재 컨투어가 다릅니다. try 진행")
				print("현재 선택된 컨투어 인덱스 = ",selectedContour.index)
				
				try:
					contourList = prevGroupDict[currentGlyph] 
					print("contourList = ", prevGroupDict[currentGlyph])
					print("currentGlyph = ", currentGlyph)
					
					for contourIdx in contourList:
						print("<<<<<<<<<< contourIdx = ",contourIdx)
						#현재 선택된 컨투어를 이전 그룹 딕셔너리에서 찾았다면 standard Contour, Glyph, contourNumber 갱신
						if selectedContour.index == contourIdx:
							print("selectedContour.index == contourIdx")
							res = True
							setExtensionDefault(DefaultKey+".standardContour", selectedContour)
							setExtensionDefault(DefaultKey+".standardGlyph", currentGlyph)
							setExtensionDefault(DefaultKey+".contourNumber", selectedContour.index)	

							#매트릭스 관련 설정값 갱신
							if mode is matrixMode:
								matrix = Matrix(selectedContour, matrix_size)
								print("생성된 매트릭스 = ",matrix) 
								setExtensionDefault(DefaultKey+".matrix", matrix)

							#현재 스마트셋 포커싱
							checkSetData = searchGroup(currentGlyph, selectedContour.index, mode, font)
							index = getMatchingSmartSet(checkSetData, currentGlyph, selectedContour.index)
							
							if index is not None : 
								smartSetIndexList = list()
								smartSetIndexList.append(index)
								selectSmartSets(smartSetIndexList)

							return True

					# 같은 글리프라도 컨투어가 같은 그룹딕셔너리가 아니라면 익셉션을 raise한다.
					raise Exception

				# 다른 스마트 셋에 있거나 아직 탐색이 완료되지 않은 경우 처리
				except Exception as e:
					result = updateSmartSetChanged(selectedContour)
					
					if result is False:
						Message("해당되는 그룹 결과가 존재하지 않습니다. 탐색을 먼저 진행해주세요.")
						
					return result

			else:
				print("True 반환")
				return True

	def updateSmartSetChanged(self, selectedContour):
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
		contourNumber = selectedContour.index;
		glyph = selectedContour.getParent();
		mode = getExtensionDefault(DefaultKey + ".mode")
		font = getExtensionDefault(DefaultKey + ".font")
		checkSetData = searchGroup(glyph, contourNumber, mode, font)
		smartSetIndex = getMatchingSmartSet(checkSetData, glyph, contourNumber)
		smartSetIndexList = list()
		smartSetIndexList.append(smartSetIndex+1) # 0번째는 All Glyphs이므로


		#selectSmartSets는 인자로 list가 온다
		if smartSetIndex is not None:
			selectSmartSets(smartSetIndexList)

		if checkSetData[2] == 0:
			
			if mode is matrixMode:

				matrix = Matrix(selectedContour, matrix_size); 
				setExtensionDefault(DefaultKey+".matrix", matrix)
			
			groupDict = findContoursGroup(checkSetData, font, mode)
			setExtensionDefault(DefaultKey+".groupDict", groupDict)
			setExtensionDefault(DefaultKey+".contourNumber", contourNumber)
			setExtensionDefault(DefaultKey+".standardContour", selectedContour)
			setExtensionDefault(DefaultKey+".standardGlyph", glyph)
			return True
		
		else:
			return False


	def getMatchingSmartSet(self, checkSetData, glyph, contourNumber):
		"""
			현재 속성을 부여하려고 시도한 그룹 딕셔너리가 바뀌는 경우 교체하기 위한 메소드
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


		#해당 컨투어가 초성인지 중성인지 종성인지 확인을 해 보아햐함
		#!!
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
		
	"""
		콜백 메소드에 연결할 메소드
	"""
	def handleDependX(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")

		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mdependXAttribute(groupDict, matrix)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			#!!!
			#추가해야함
			#tbt.dependXAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")
			return


		CurrentFont().update()	#로보폰트 업데이트
		CurrentFont().save(self.testPath) 	#XML 업데이트

	def handleDependY(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")

		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mdependYAttribute(groupDict, matrix)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.mdependYAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")
			return


		CurrentFont().update()	#로보폰트 업데이트
		CurrentFont().save(self.testPath) 	#XML 업데이트


	def handlePenPair(self, sender):
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")

		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mpenPairAttribute(groupDict, matrix)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.penPairAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")
			return


		CurrentFont().update()	#로보폰트 업데이트
		CurrentFont().save(self.testPath) 	#XML 업데이트

	def handleInnerFill(self, sender):

		if self.updateAttributeComponent() is False:
			return

		groupDict = getExtensionDefault(DefaultKey+".groupDict")
		mode = getExtensionDefault(DefaultKey+".mode")
		
		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.minnerFillAttribute(groupDict, matrix)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.innerFillAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")
			return


		CurrentFont().update()	#로보폰트 업데이트
		CurrentFont().save(self.testPath) 	#XML 업데이트

	def handleStroke(self, sender):
		
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")

		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			mbt.mgiveStrokeAttribute(groupDict, matrix)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.mgiveStrokeAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")
			return


		CurrentFont().update()	#로보폰트 업데이트
		CurrentFont().save(self.testPath) 	#XML 업데이트


	def handleSelect(self, sender):
		print("!!")
		if self.updateAttributeComponent() is False:
			return
		
		mode = getExtensionDefault(DefaultKey+".mode")
		groupDict = getExtensionDefault(DefaultKey+".groupDict")

		if mode is matrixMode:
			matrix = getExtensionDefault(DefaultKey+".matrix")
			print("matrix = ", matrix)
			mbt.mselectAttribute(groupDict, matrix)

		elif mode is topologyMode:
			standardContour = getExtensionDefault(DefaultKey+".standardContour")
			k = getExtensionDefault(DefaultKey+".k")
			tbt.selectAttribute(groupDict, standardContour, k)
				
		else:
			Message("모드 에러")
			return


	def popDelete(self, sender):
		self.subWindow = subAttributeWindow(self)
			
	def minimizeCallback(self, sender):
		if sender.get() == True:
			self.w.resize(self.minSize[0], self.minSize[1])
			self.w.minimizeBox.setTitle("")
		else:
			self.w.resize(self.size[0], self.size[1])
			self.w.minimizeBox.setTitle("최소화")

	def close(self, sender):
		self.w = None