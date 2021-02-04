import json

def groupList2Dict(groupList):

    _dict = {}

    for i, g in enumerate(groupList):
        for j, s in enumerate(g):
            for k, e in enumerate(s):
                if k == 0:
                    tmpKey = e
                elif k == 1:
                    tmpValue = s[1].index
                    try:
                        _dict[tmpKey].append(tmpValue)
                    except KeyError:
                        _dict[tmpKey] = [tmpValue]

    return _dict
"""
    인자로 넘어온 groupDic을 filePath이름의 json파일로 저장
"""
"""
    2020/02/20  
    create by hyunwoo Choi

    2020/02/21
    modify by heesup Kim
    
    버그 수정사안 : groupDict를 수정하면서 반복문을 돌면 딕셔너리 길이와 내용이 변동 되어서 버그가 생기는 점을 발견
                 이를 수정함
                 인자 이름 변경 filePath -> jsonFilePath
    Bug fixed : while execut Dictionary, modity the dictionary cause bug so corrected it
"""
def groupDict2JSON(groupDict, jsonFilePath):

    appendDict = {}

    for glyph in groupDict.keys():
        try:
            newKey = str(glyph.unicode)
            appendDict[newKey] = groupDict[glyph]
            
        except KeyError:
            print("glyph : ", glyph, "  newKey : ", newKey)
            continue

    groupDict.clear()

    groupDict.update(appendDict)
    with open(jsonFilePath, 'w') as jsonFile:
        json.dump(groupDict, jsonFile)
"""
    json 파일 복원 후 groupDict 반환
"""
"""
    2020/02/20   
    create by hyunwoo Choi

    2020/02/21
    modify by heesup Kim
    추가부분 : 딕셔너리 반환시 키 값을 RGlyph로 변환하는 작업을 추가
             이를 위한 원본 fontFile을 추가 인자로 넘겨 주웠음
             jsonFilePath - json파일 경로, originFile - 원본파일 
             Added a task to convert key values ​​to RGlyph on dictionary return
"""
def json2groupDict(jsonFilePath,originFile):
    tempDict = {}
    groupDict ={}

    with open(jsonFilePath, 'r') as jsonFile:
        tempDict = json.load(jsonFile)

    for item in tempDict.items():
        tempNum = int(item[0])
        uniNum = hex(tempNum)[2:].upper()
        groupDict[originFile["uni" + uniNum]] = item[1]    
        
    return groupDict



"""
    더 이상 groupList를 사용하지 않고 groupDic을 사용하므로 주석처리하였음.
"""
"""
def gruopList2File(groupList, filePath):

    _dict = {}
    f = open(filePath, 'w')

    for i, g in enumerate(groupList):
        for j, s in enumerate(g):
            for k, e in enumerate(s):
                if k == 0:
                    tmpKey = str(hex(e.unicode))[2:].upper()
                elif k == 1:
                    tmpValue = s[1].index
                    try:
                        _dict[tmpKey].append(tmpValue)
                    except KeyError:
                        _dict[tmpKey] = [tmpValue]


    for k in sorted(_dict.keys()) :
    	f.write("%s:%s\n" % (k, _dict[k]))

    f.close()

def file2groupList(filePath):
    
    f = open(filePath, 'r')
    
    groupList = []
    group = []
    segment = []
    font = CurrentFont()
    
    while True:
        line = f.readline()
        if not line:
            break
        res = line.split(':')
        uniCode = res[0]
        index = res[1][1:-2].split(',')
        #리스트 만들기
        tmpList = []
        for idx in index:
            tmpList.append([font["uni"+uniCode], font["uni"+uniCode].contours[int(idx)]])
            
        
        groupList.append(tmpList)

    return groupList
    """