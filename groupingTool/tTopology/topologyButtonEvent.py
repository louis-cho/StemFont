from groupingTool.tTopology.topologyJudgement import *
from groupingTool.tTopology.topologyAssignment import *
from jsonConverter.converter import *
from mojo.extensions import *
from mojo.roboFont import CurrentGlyph
from rbWindow.ExtensionSetting import extensionValue
from rbWindow.ExtensionSetting.extensionValue import *
"""
2020/02/20
Created by heesup Kim

2020/03/19
Modify by heesup Kim
파라미터 k와 변수 k가 중첩이 되어져서 잘못된 결과를 생성 -> 이를 수정
"""
def selectAttribute(groupDict,standardContour,num):
	"""
	To select all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	prevPointList = list()
	restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

	g = CurrentGlyph()
	for point in g.selectedPoints:
		tmp = list()
		tmp.append(point); tmp.append(point.name)
		prevPointList.append(tmp)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		if controllerList[i].cCheckCon is not None:
			for j in range(0, len(controllerList[i].sCheckCon.tpPointList)):

				# restoreStack에 필요한 데이터를 넣는 과정
				if(controllerList[i].sCheckCon.tpPointList[j].point.selected == True):
					tmp = list()
					tmp.append(controllerList[i].cCheckCon.tpPointList[j].point); tmp.append(controllerList[i].cCheckCon.tpPointList[j].point.name)
					prevPointList.append(tmp)

		controllerList[i].giveSelected()

	restoreStack.push(prevPointList)
	setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def penPairAttribute(groupDict,standardContour,num):
	"""
	To give penPair attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	prevPointList = list()
	restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

	g = CurrentGlyph()
	for point in g.selectedPoints:
		tmp = list()
		tmp.append(point); tmp.append(point.name)
		prevPointList.append(tmp)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		if controllerList[i].cCheckCon is not None:
			for j in range(0, len(controllerList[i].sCheckCon.tpPointList)):

				# restoreStack에 필요한 데이터를 넣는 과정
				if(controllerList[i].sCheckCon.tpPointList[j].point.selected == True):
					tmp = list()
					tmp.append(controllerList[i].cCheckCon.tpPointList[j].point); tmp.append(controllerList[i].cCheckCon.tpPointList[j].point.name)
					prevPointList.append(tmp)

		controllerList[i].giveAttrPenPair()

	restoreStack.push(prevPointList)
	setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def dependXAttribute(groupDict,standardContour,num):
	"""
	To give dependX attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	prevPointList = list()
	restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

	g = CurrentGlyph()
	for point in g.selectedPoints:
		tmp = list()
		tmp.append(point); tmp.append(point.name)
		prevPointList.append(tmp)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		if controllerList[i].cCheckCon is not None:
			for j in range(0, len(controllerList[i].sCheckCon.tpPointList)):

				# restoreStack에 필요한 데이터를 넣는 과정
				if(controllerList[i].sCheckCon.tpPointList[j].point.selected == True):
					tmp = list()
					tmp.append(controllerList[i].cCheckCon.tpPointList[j].point); tmp.append(controllerList[i].cCheckCon.tpPointList[j].point.name)
					prevPointList.append(tmp)

		controllerList[i].giveDependX()

	restoreStack.push(prevPointList)
	setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def dependYAttribute(groupDict,standardContour,num):
	"""
	To give dependX attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	prevPointList = list()
	restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

	g = CurrentGlyph()
	for point in g.selectedPoints:
		tmp = list()
		tmp.append(point); tmp.append(point.name)
		prevPointList.append(tmp)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		if controllerList[i].cCheckCon is not None:
			for j in range(0, len(controllerList[i].sCheckCon.tpPointList)):

				# restoreStack에 필요한 데이터를 넣는 과정
				if(controllerList[i].sCheckCon.tpPointList[j].point.selected == True):
					tmp = list()
					tmp.append(controllerList[i].cCheckCon.tpPointList[j].point); tmp.append(controllerList[i].cCheckCon.tpPointList[j].point.name)
					prevPointList.append(tmp)

		controllerList[i].giveDependY()

	restoreStack.push(prevPointList)
	setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def innerFillAttribute(groupDict,standardContour,num):
	"""
	To give innerFill attribute all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	prevPointList = list()
	restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

	g = CurrentGlyph()
	for point in g.selectedPoints:
		tmp = list()
		tmp.append(point); tmp.append(point.name)
		prevPointList.append(tmp)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		if(standardContour != contoursList[i]):
			controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		if controllerList[i].cCheckCon is not None:
			for j in range(0, len(controllerList[i].sCheckCon.tpPointList)):

				# restoreStack에 필요한 데이터를 넣는 과정
				if(controllerList[i].sCheckCon.tpPointList[j].point.selected == True):
					tmp = list()
					tmp.append(controllerList[i].cCheckCon.tpPointList[j].point); tmp.append(controllerList[i].cCheckCon.tpPointList[j].point.name)
					prevPointList.append(tmp)

		controllerList[i].giveInnerFill()

	restoreStack.push(prevPointList)
	setExtensionDefault(DefaultKey+".restoreStack", restoreStack)

def deleteAttribute(groupDict,standardContour,attribute,num):
	"""
	To delete attributet all same group's contours point that is same point with standard contour

	Args : 
		groupFile :: str
			file's path that has group contours
		originalFile :: File
			file that has total contours
		standardContour :: RContour
		attribute :: string
			attribute that want to delete
		num :: int
            value of divide(insert None topology at divided position) 
	"""
	controllerList = []
	contoursList = []
	prevPointList = list()
	restoreStack = getExtensionDefault(DefaultKey+".restoreStack")

	g = CurrentGlyph()
	for point in g.selectedPoints:
		tmp = list()
		tmp.append(point); tmp.append(point.name)
		prevPointList.append(tmp)

	#create topologyJudgementController object
	for k in groupDict.keys():
		for i in range(0,len(groupDict[k])):
			contoursList.append(k.contours[groupDict[k][i]])

	for i  in range(0,len(contoursList)):
		controllerList.append(topologyJudgementController(standardContour,contoursList[i],num))

	for i in range(0, len(controllerList)):
		if controllerList[i].cCheckCon is not None:
			for j in range(0, len(controllerList[i].sCheckCon.tpPointList)):

				# restoreStack에 필요한 데이터를 넣는 과정
				if(controllerList[i].sCheckCon.tpPointList[j].point.selected == True):
					tmp = list()
					tmp.append(controllerList[i].cCheckCon.tpPointList[j].point); tmp.append(controllerList[i].cCheckCon.tpPointList[j].point.name)
					prevPointList.append(tmp)

		controllerList[i].deleteAttr(attribute)	

	restoreStack.push(prevPointList)
	setExtensionDefault(DefaultKey+".restoreStack", restoreStack)			