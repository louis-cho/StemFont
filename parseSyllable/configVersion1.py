from groupingTool.parseUnicodeControll import *

vertical = 0
horizontal = 1
double = 2

exceptCaseOne = -1
exceptCaseTwo = -2

def getConfigureVersion1(RGlyph):
    """
    2020/03/04
    글리프 객체에 대한 초중종 정보를 딕셔너리 형태로 반환한다.
    Args :
        RGlyph : 초중종 정보를 알아내고 싶은 글리프 객체
    """
    unicodeObj = parseUnicodeController(RGlyph.unicode)
    uniCodeIdx = unicodeObj.parseUnicode()
    uniCodeData = unicodeObj.getChars()
    
    check = False
    syllableList = [[],[],[]]
    mode = None
    boundary = getBoundary(RGlyph)

    
    # 종성이 존재하지 않는 경우
    if uniCodeData[2] is None:

            if uniCodeIdx[1] in parseUnicodeController.vowel_vertical:         
                mode = vertical
            
                if uniCodeIdx[1] in parseUnicodeController.vowel_vertical_double:
                    check = True
        
            elif uniCodeIdx[1] in parseUnicodeController.vowel_horizontal:        
                if uniCodeData[0] == 'ㅃ' or uniCodeData[0] == 'ㅂ':
                    check = True
                    if uniCodeIdx[1] in parseUnicodeController.vowel_horizontal_low:
                        check = exceptCaseOne
                mode = horizontal
                
            elif uniCodeIdx[1] in parseUnicodeController.vowel_double:
                if uniCodeData[0] == 'ㅃ' or uniCodeData[0] == 'ㅂ':
                    check = True
                mode = double
            
            lineBoundary = [0]*2
            if mode is vertical:
                lineBoundary = boundary[0:2]
            elif mode is horizontal:
                lineBoundary = boundary[2:4]
            elif mode is double:
                lineBoundary = [0]*4
                lineBoundary = boundary
            
            percentage = getPercentage(mode, check, 1)
            splitLine = getSpiltLine(lineBoundary, percentage, mode) # 글리프 시작점과 끝점 사이 몇 퍼센트 지점에 라인을 긋겠는가
        
            percentage = getPercentage(mode, check, 2)
            for idx, RContour in enumerate(RGlyph):
                if isFirst(RContour, boundary, splitLine, percentage, mode) is True:    # 점의 몇 퍼센트 이상이 포함되어야 초성으로 분류하는가
                    syllableList[0].append(idx)
                else:
                    syllableList[1].append(idx)
        
                
    # 종성이 존재하는 경우    
    elif uniCodeData[2] is not None:
        percentage = [50, 100]
        boundary = getBoundary(RGlyph)
        
        if uniCodeIdx[1] in parseUnicodeController.vowel_horizontal:
            if uniCodeData[2] in ['ㅎ','ㅊ']:
                percentage = [55,100]
            mode = horizontal
        elif uniCodeIdx[1] in parseUnicodeController.vowel_vertical:
            mode = vertical
        
        elif uniCodeIdx[1] in parseUnicodeController.vowel_double:
            percentage = [47,100]
            mode = double
        
            if uniCodeData[0] == 'ㅃ' or uniCodeData[0] == 'ㅂ':
                check = True
        
        newGlyph = []    
        for idx, RContour in enumerate(RGlyph):    
            if isLast(RContour, boundary, percentage, mode):
                syllableList[2].append(idx)
            if idx not in syllableList[2] and mode is horizontal:
                if isFirstwithLast(RContour, boundary, mode) is True:
                    syllableList[0].append(idx)
                else:
                    syllableList[1].append(idx)
    
            #  종성 빼고 초성에서 했던 과정 그대로 반복해보자   
            if idx not in syllableList[2] and mode is not horizontal:
                newGlyph.append(RContour)
        
        if mode is not horizontal:        
                boundary = getBoundary(newGlyph)
        
                lineBoundary = [0]*2
                if mode is vertical:
                    lineBoundary = boundary[0:2]
                elif mode is double:
                    lineBoundary = [0]*4
        
                lineBoundary = boundary
                percentage = getPercentage(mode, check, 1)
                splitLine = getSpiltLine(lineBoundary, percentage, mode)
        
                percentage = getPercentage(mode, check, 2)
                for RContour in newGlyph:
                    if isFirst(RContour, boundary, splitLine, percentage, mode) is True:
                        syllableList[0].append(RContour.index)
                    else:
                        syllableList[1].append(RContour.index)      
    else:
        return None
        
    data = {}
    data[str(RGlyph.unicode)] = syllableList
    return data

def getBoundary(RGlyph):
    """
        2020/03/04
        글리프 상 점의 존재 범위를 반환하는 함수

        Args:
            RGlyph : 글리프객체 혹은 종성을 제외하고 새로 생성한 컨투어 리스트.
            후자의 경우 except 문을 실행하게 된다.
    """
    boundary = [1e9, -1e9, 1e9, -1e9]
    try:
        for contours in RGlyph.contours:
            for point in contours.points:
                if point.type != 'offcurve':
                    if boundary[0] > point.x:
                        boundary[0] = point.x
                    if boundary[1] < point.x:
                        boundary[1] = point.x
                    if boundary[2] > point.y:
                        boundary[2] = point.y
                    if boundary[3] < point.y:
                        boundary[3] = point.y
    except AttributeError:
            for contours in RGlyph:
                for point in contours.points:
                    if point.type != 'offcurve':
                         if boundary[0] > point.x:
                             boundary[0] = point.x
                         if boundary[1] < point.x:
                             boundary[1] = point.x
                         if boundary[2] > point.y:
                             boundary[2] = point.y
                         if boundary[3] < point.y:
                             boundary[3] = point.y
        # value = [minX, maxX, minY, maxY]
    return boundary

def getPercentage(mode, check, n):
        """
        2020/03/04
            각 모드 별로 해당되는 percentage를 반환하는 함수

            Args:
                mode : 모음이 수직, 수평 혹은 둘 다인지를 나타내는 변수
                check : 모음이 두 줄로 되어있나 확인하는 변수
                n : 1이라면 분할선에 대한 퍼센트를 반환
                    2라면 초/중성 구분에 대한 퍼센트를 반환
                    3이라면 종성이 있는 경우에 대한 분할선 퍼센트 반환
                    4라면 종성이 있는 경우에 대한 초/중성 구분에 대한 퍼센트 반환
        """

        if n == 1:
            if mode is vertical:
                if check is True:
                    return 70
                else:
                    return 80
                
            if mode is horizontal:
                if check is True:
                    return 42
                elif check == exceptCaseOne:
                    return 30       
                else:
                    return 55

            if mode is double:
                if check is True:
                    return [75,45]
                else:
                    return [75,57]


        elif n == 2:
            if mode is vertical:
                if check is True:
                    return 90
                else:
                    return 80

            if mode is horizontal:
                if check is True:
                    return 30           
                elif check == exceptCaseOne:
                    return 30           
                else:
                    return 80

            if mode is double:
                if check is True:
                    return 30
                else:
                    return 30
                
        elif n == 3:
            if mode is vertical:
                if check is exceptCaseOne or check is exceptCaseTwo:
                    return 70
                else:
                    return 80
        elif n == 4:
            if mode is vertical:
                if check is exceptCaseOne:
                    return 90
                else:
                    return 80
                

        else:
            return None

def getSpiltLine(boundary, percentage, mode):
    """
        초중종 구분을 위한 경계선을 반환하는 메소드
    
        퍼센트가 주어지면 좌측으로 부터 퍼센트만큼 분할하여 만든 기준선의 x좌표를 반환
        percentage (0~100)
        반환하는 line 값보다 작은 점들이 일정 수준 이상 존재한다면 초성
        아니라면 중성임을 의심해봐야 한다.
    """
    if mode is not double:
        i = 0; j = 1;
    elif mode is double:
        length1 = boundary[1] - boundary[0]
        length2 = boundary[3] - boundary[2]
        line = [[],[]]
        line[0] = int(boundary[0] + length1 * percentage[0] / 100)
        line[1] = int(boundary[2] + length2 * percentage[1] / 100)
        return line
    else:
        return None
    try:
        length = boundary[j] - boundary[i]
        line = boundary[i] + length * percentage / 100
    except IndexError:
        print(i, j)
    return int(line)

def isFirstwithLast(RContour, boundary, mode):
    """
        2020/03/04

        종성이 있는 글리프에서 초성을 구분하는 메소드
        mode가 horizontal일 때만 작동

        Args : 
            RContour : 초/중성 구분의 대상이 되는 컨투어
            boundary : 최대,최소 x,y 값
            mode     : 중성 카테고리


        Return:
            True: 초성
            False: 초성이 아님
    """
    try:
        if mode is vertical or mode is double:
            raise ValueError
        elif mode is horizontal:
            for point in RContour.points:
                if point.type != 'offcurve':
                    if point.x == boundary[0] or point.x == boundary[1]:
                        return False
            return True
    except ValueError:
        print("isFirstwithLast()의 인자가 잘못되었습니다. (mode는 horizontal만 가능)")
        return False

def isFirst(RContour, boundary, line, percentage, mode):
        """
            2020/03/03

            RContour 객체가 초성인지 아닌지 구분해주는 메소드

            Args:
                RContour : 초/중성 구분의 대상이 되는 컨투어
                boundary : 최대,최소 x,y 값
                line     : 구분을 위한 경계값
                percentage : line이란 경계값 내에 존재하여야 하는 점의 비율
                mode     : 중성 카테고리

            Return:
                True: 초성
                False: 초성이 아님
        """
        num = 0
        sumPoint = 0

        if mode is vertical and type(line) is int:
            for point in RContour.points:
                if point.type is not 'offcurve':
                    sumPoint += 1
                    if point.x < line:
                        num += 1

        elif mode is horizontal and type(line) is int:
            for point in RContour.points:
                if point.type != 'offcurve':
                    if point.x == boundary[0] or point.x == boundary[1]:
                        return False
                    sumPoint += 1
                    if point.y < line:
                        num += 1

        elif mode is double and type(line) is list:
            for point in RContour.points:
                if point.type is not 'offcurve':
                    sumPoint += 1
                    if point.x < line[0] and point.y > line[1]:
                        num += 1
                    
        if mode is vertical and int((num*100) / sumPoint) > percentage:
            return True
        
        if mode is horizontal:
            if int((num*100) / sumPoint) < percentage:
                return True
            else:
                return False
            
        if mode is double:
            if int((num*100)/sumPoint)>percentage:
                return True

        return False

def isLast(RContour, boundary, percentage, mode):
    """
        2020/03/03

        RContour 객체가 종성인지 아닌지 구분해주는 메소드

        Args:
            RContour : 종성 구분의 대상이 되는 컨투어
            boundary : 최대,최소 x,y값
            percentage : percentage[0] : 경계 라인이 되는 line 변수를 구하기 위한 값. percentage[1] : 경계 라인 내에 존재하여야 하는 점의 비율
            mode     : 중성 카테고리

        Return:
            True : 종성
            False : 종성이 아님
    """

    # 종성이 존재하며, 모음이 가로배치인 경우
    if mode is horizontal:
        for point in RContour.points:
            if type(point) is not 'offcurve' and (boundary[0] == point.x or boundary[1] == point.x):
                return False
            
    line = boundary[2] + int((boundary[3] - boundary[2])*percentage[0]/100)

    num = 0; sumPoint = 0
    for point in RContour.points:
        if point.type is not 'offcurve':
            if line > point.y:
                num+=1
            sumPoint += 1

    if int((num*100)/sumPoint) >= percentage[1]:
        return True
    else:
        return False