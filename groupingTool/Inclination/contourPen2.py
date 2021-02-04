from fontTools.pens.basePen import BasePen
from mojo.drawingTools import oval, save, translate, rotate, restore

"""
    자세한 원리는 모르나, 컨투어 주변을 색칠하기 위한 클래스
"""
class BroadNibPen2(BasePen):

    def __init__(self, glyphSet, step, width, height, angle, shape):
        BasePen.__init__(self, glyphSet)
        self.step = step
        self.width = width
        self.height = height
        self.angle = angle
        self.shape = shape
        self.firstPoint = None

        self.drawPath = list()

    #firstPoint를 pt점으로 이
    def _moveTo(self, pt):
        
        self.firstPoint = pt

    #현재 점에서 pt점 까지 선 긋기
    def _lineTo(self, pt):
        
        pt0 = self._getCurrentPoint()
        points = getPointsOnLine(self.step, pt0, pt)
        self._drawPoints(points)
    
    # 커브 위의 점을 불러와 _drawPoints 실행
    def _curveToOne(self, pt1, pt2, pt3):
        
        pt0 = self._getCurrentPoint()
        points = getPointsOnCurve((int)(self.step/4), pt0, pt1, pt2, pt3)
        self._drawPoints(points)

    def _closePath(self):
        
        pt0 = self._getCurrentPoint()
        pt = self.firstPoint
        if pt0 != pt:
            points = getPointsOnLine(self.step, pt0, pt)
            self._drawPoints(points)

    # shape에 해당하는 모양으로 색칠
    def _drawPoints(self, points):
        
        for point in points:
            x, y = point
            self.drawPath.append((x,y))
            #self.shape(0, 0, self.width, self.height)   #이동한 위치에서 설정한 모양대로 그림 그리기

    def getDrawPath(self):
        try:
            if len(self.drawPath) == 0:
                raise NoPath
            else:
                return self.drawPath
        except NoPath:
            print("아직 경로가 계산되지 않았습니다")


# 커브 위의 점을 n에 비례한 정밀도를 가지고 표시한다.
def getPointsOnCurve(n, p0, p1, p2, p3):
    x0, y0 = p0
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    points = [(x0, y0)]

    for t in range(1, n):
        t = t/n

        ax = x0 + t * (x1 - x0)
        ay = y0 + t * (y1 - y0)
        bx = x1 + t * (x2 - x1)
        by = y1 + t * (y2 - y1)
        cx = x2 + t * (x3 - x2)
        cy = y2 + t * (y3 - y2)
        dx = ax + t * (bx - ax)
        dy = ay + t * (by - ay)
        ex = bx + t * (cx - bx)
        ey = by + t * (cy - by)
        fx = dx + t * (ex - dx)
        fy = dy + t * (ey - dy)

        points.append((fx, fy))

    return points

# 비례식을 이용해서 p0~p1 사이의 1/n, 2/n, ... n-1/n 점을 추가한다.
def getPointsOnLine(n, p0, p1):
    x0, y0 = p0
    x1, y1 = p1

    points = [(x0, y0)]

    for t in range(1, n):
        t = t/n

        fx = x0 + t * (x1 - x0)
        fy = y0 + t * (y1 - y0)

        points.append((fx, fy))

    return points