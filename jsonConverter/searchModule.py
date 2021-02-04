import os
from groupingTool.parseUnicodeControll import *
import jsonConverter.converter as convert
from parseSyllable.configSyllable import *
import pathManager.pathSetting as extPath
"""
Data Example :
	data = {'uniB232': [[3], [4,5], [0,1,2]]}
	data = {'uniB12F': [[0], [1,2], [3,4,5]]}

Depend on Data, Destination Dir should be extPath.baseDir + dirPostFix
"""

dirPostFix = ['first', 'middle', 'last']


def getGroupDictFile(RGlyph, idx, fontFile,mode,width,margin):
    """
    2020/03/13
    created by H.W. Cho
    
    Return Matching GroupDict(dict) with RGlyph.contours[idx](RContour) from fontFile(RFont)
    Filenames would like to be extPath.baseDir / dirPostFix / 'ㄱ' / + number.json
    
    Args:
        - RGlyph(RGlyph)
        - idx(int) : RGlyph's contour
        - fontFile(RFont)
    Return
        targetGroupDict(dict) or None
    Variables:
        - configIdx(int) : 0(first) 1(middle) 2(last) -1(None of Them)
        - targetDir(str) : Save Location
        - fileList(list) : targetDir's syllable file list
    """
    targetGroupDict = None
    data = getConfigure(RGlyph)	# Get [first, middle, last] Dictionary Data about RGlyph
    configIdx = -1
    
    # If there's matching index, set configIdx which should be 0(first),1(middle) or 2(last)
    for syllableList in data.values():
        for syllableIdx, syllable in enumerate(syllableList):
            if idx in syllable:
                configIdx = syllableIdx																												
    
    tmpObject = parseUnicodeController(RGlyph.unicode)																			# RGlyph 객체의 컨투어에 대한 이름을 찾아야 함 
    uniCodeData = tmpObject.getChars()[configIdx]																				# ex) 갏 tmpObject.getChars() => ['ㄱ', 'ㅏ', 'ㅀ']

    # 저장 경로는 기본 경로(extPath.baseDir) + 초/중/종 구분 경로 + '음절 구분 경로'
    if mode == 0:
    	targetDir = extPath.baseDir+ 'matrix/' + str(width) +'_' + str(margin)+ '/' + dirPostFix[configIdx] + '/' + str(uniCodeData) + '/'
    else:
    	targetDir = extPath.baseDir+ 'topology/' + dirPostFix[configIdx] + '/' + str(uniCodeData) + '/'
    
    
    try:
        if not os.path.isdir(targetDir):
            os.makedirs(os.path.join(targetDir))
            
    except OSError:
        print("getGroupDictFile(RGlyph, idx) 디렉터리를 만드는데 실패하였습니다...")
        
    fileList = os.listdir(targetDir)																							# target 경로 폴더의 파일들을 불러온다.
    count = len(RGlyph.contours[idx].points)																					# 파일명 [컨투어 점의 개수]-[N번째 그룹].json
    
    for item in fileList:
        filename, fileExtension = os.path.splitext(item) 																		# 파일명(filenamme), 확장자(fileExtension)
        
        # 파일명이 점의 개수와 일치하고, 글리프 객체에 대한 컨투어 인덱스 리스트 안에 idx 값이 있다면 해당 그룹 딕셔너리를 반환한다.
        if filename.startswith(str(count)):
            targetGroupDict = convert.json2groupDict(targetDir + filename + fileExtension, fontFile)
         
            
            if idx in targetGroupDict[RGlyph]:
                return targetGroupDict
                
            else:
                print(str(filename)+"은 카운트로 시작하지 않습니다.") 
                
    # 해당 파일을 찾지 못한 경우
    return None




def getGroupDictPath(groupDict,mode,width,margin):
	"""
		2020/03/13
		created by H.W. Cho

		Get Name of Saved File which Include Path & Extension Name

		Param:
			- groupDict(dict) : target which want to get filename
		Return:
			-targetDir(str) or None
	"""

	RGlyph = list(groupDict.keys())[0]
	data = getConfigure(RGlyph)

	idx = list(groupDict.values())[0][0]
	configIdx = -1
	for syllableList in data.values():
		for syllableIdx, syllable in enumerate(syllableList):
			if idx in syllable:
				configIdx = syllableIdx																
	
	try:
		
		tmpObject = parseUnicodeController(RGlyph.unicode)
		uniCodeData = tmpObject.getChars()[configIdx]
		if mode == 0:
			targetDir = extPath.baseDir+  'matrix/' + str(width) +'_' + str(margin)+ '/' + dirPostFix[configIdx] + '/' + str(uniCodeData) + '/'
		else:
			targetDir = extPath.baseDir+ 'topology/' + dirPostFix[configIdx] + '/' + str(uniCodeData) + '/'

		count = len(RGlyph.contours[idx].points)
	
		
		fileList = os.listdir(targetDir)
		numOfFile = 0
		
		for item in fileList:
			filename, fileExtension = os.path.splitext(item)

			if filename.startswith(str(count)):
				numOfFile += 1

		targetDir = targetDir + str(count) + "_" + str(numOfFile) + ".json"
		return targetDir
			
	except IndexError:
		print("인덱스 에러 발생")
		return None

	# 디렉터리가 존재하지 않는다면 생성 후 해당 파일의 경로를 반환한다.
	except FileNotFoundError:
		os.makedirs(os.path.join(targetDir))
		targetDir = targetDir + str(count) + "_" + str(0) + ".json"
		return targetDir