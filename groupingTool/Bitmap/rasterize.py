from mojo.roboFont import *

def rasterize(con, cellSize=50, xMin=None, yMin=None, xMax=None, yMax=None):
    """
    Slice the glyph into a grid based on the given cell size.

    Returns a list of lists containing bool values that indicate the
    black (True) or white (False) value of that particular cell.
    These lists are arranged from top to bottom of the glyph and proceed
    from left to right.

    Warning: This is an expensive operation!

    """

    if xMin is None or yMin is None or xMax is None or yMax is None:
        _xMin, _yMin, _xMax, _yMax = con.bounds
        if xMin is None:
            xMin = _xMin
        if yMin is None:
            yMin = _yMin
        if xMax is None:
            xMax = _xMax
        if yMax is None:
            yMax = _yMax

    hitXMax = False
    hitYMin = False
    xSlice = 0
    ySlice = 0
    halfCellSize = cellSize / 2.0
    bitmap = []

    while not hitYMin:
        bitmap.append([])
        yScan = -(ySlice * cellSize + halfCellSize) + yMax
        if yScan < yMin:
            hitYMin = True
        while not hitXMax:
            xScan = (xSlice * cellSize + halfCellSize) + xMin
            if xScan > xMax:
                hitXMax = True
            test = con.pointInside((xScan, yScan))
            if test:
                bitmap[-1].append(True)
            else:
                bitmap[-1].append(False)
            xSlice = xSlice + 1
        hitXMax = False
        xSlice = 0
        ySlice = ySlice + 1

    return bitmap

def compareBitMap(con1, con2,k):
    """
    한자 버전에서 사용
    두개의 컨투어를 비트맵 형식으로 바꾼 다음 일정 범위를 초과하면 같은 그룹으로 취급하지 않음
    Args :
        con1 :: RContour
            기준 컨투어
        con2 :: RContour
            비교 컨투어
        k :: int
            오차 허용 범위 (True의 갯수 오차 허용 범위)

    Returns :: boolean
        같은 그룹이면 True 아니면 False
    """

    #크기를 비교하기 위하여 복사하여 글리프에 붙혀 준 다음 크기를 늘려 비교
    glyph = CurrentGlyph()

    sxMin1,syMin1,sxMax1,syMax1 = con1.bounds
    sxMin2,syMin2,sxMax2,syMax2 = con2.bounds

    tempDistx1 = sxMax1 - sxMin1
    tempDistx2 = sxMax2 - sxMin2
    tempDisty1 = syMax1 - syMin1
    tempDisty2 = syMax2 - syMin2

    #x길이가 큰 것을 우선으로 잡고 x길이가 같으면 y길이가 큰 것을 기준으로 우선으로 잡기
    if tempDistx1 > tempDistx2:
        con3 = con1.copy()
        con4 = con2.copy()
    elif tempDistx1 < tempDistx2:
        con3 = con2.copy()
        con4 = con1.copy()
    else:
        if tempDisty1 > tempDisty2:
            con3 = con1.copy()
            con4 = con2.copy()
        else:
            con3 = con2.copy()
            con4 = con1.copy()

    glyph.appendContour(con3)
    glyph.appendContour(con4)

    tempContour1 = glyph.contours[len(glyph.contours) -1]
    tempContour2 = glyph.contours[len(glyph.contours) -2]

    #크기를 비교하여서 늘려주어 크기를 같게 함
    xMin1,yMin1,xMax1,yMax1 = tempContour1.bounds
    xMin2,yMin2,xMax2,yMax2 = tempContour2.bounds
    dist_x1 = xMax1 - xMin1
    dist_y1 = yMax1 - yMin1
    dist_x2 = xMax2 - xMin2
    dist_y2 = yMax2 - yMin2

    if dist_x1 > dist_x2:
        dist_x = dist_x1 / dist_x2
    else:
        dist_x = dist_x2 / dist_x1

    if dist_y1 > dist_y2:
        dist_y = dist_y1 / dist_y2
    else:
        dist_y = dist_y2 / dist_y1

    if dist_x1 > dist_x2:
        tempContour2.scaleBy((dist_x,1))
    else:
        tempContour1.scaleBy((dist_x,1))

    if dist_y1 > dist_y2:
        tempContour2.scaleBy((1,dist_y))
    else:
        tempContour1.scaleBy((1,dist_y))

    #기준 컨투어의 비트맵 형식 변환
    standardBitMap = rasterize(tempContour1)

    #비교 컨투어의 비트맵 형식 변환
    compareBitMap =  rasterize(tempContour2)

    #원소 갯수의 차이를 계산
    s_count = 0
    c_count = 0

    for i in range(0,len(standardBitMap)):
        s_count += standardBitMap[i].count(True)
    for i in range(0, len(compareBitMap)):
        c_count += compareBitMap[i].count(True)

    #비트맵 구역 조사가 끝났으면 삭제
    glyph.removeContour(glyph.contours[len(glyph.contours) -1])
    glyph.removeContour(glyph.contours[len(glyph.contours) -1])


    _diff = abs(s_count - c_count)

    if _diff <= k:
        return True
    else:
        return False








